# app/main/routes.py

from datetime import datetime, timezone

from urllib.parse import urlsplit
from flask import (render_template, flash, redirect, url_for, request,
                   g, current_app)
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa
import langdetect
#from app import db, get_locale
from app import db
from app.main import bp
from app.main.forms import EditProfileForm
from app.main.forms import EmptyForm
from app.main.forms import PostForm
from app.main.forms import SearchForm
from app.models import User, Post
from app.translate import translate
from app.utils import get_locale


@bp.before_request
def before_request_hook():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())
        
#----------------------------------------------------------------------
# VIEW : INDEX
#----------------------------------------------------------------------

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        try:
            lang = langdetect.detect(form.post.data)
        except langdetect.LangDetectException:
            lang = ''
        post = Post(body=form.post.data, 
                    author=current_user,
                    language=lang)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))

    #posts = db.session.scalars(current_user.following_posts()).all()
    page = request.args.get('page', 1, type=int)
    # paginate returns a paginate-object 
    p = db.paginate(current_user.following_posts(), 
                    page=page, 
                    per_page=current_app.config['APP_POSTS_PER_PAGE'],
                    error_out=False)
    next_url = url_for('main.index', page=p.next_num) if p.has_next else None
    prev_url = url_for('main.index', page=p.prev_num) if p.has_prev else None
    return render_template('index.html', 
                           title=current_app.config.get('APP_WINTITLES_INDEX',
                                                        '___Home Page___'), 
                           form=form, 
                           posts=p.items, next_url=next_url, prev_url=prev_url)

#----------------------------------------------------------------------
# VIEW : USER/<USERNAME> 
#----------------------------------------------------------------------

@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    query = user.posts.select().order_by(Post.timestamp.desc())
    p = db.paginate(query,
                    page=page, 
                    per_page=current_app.config['APP_POSTS_PER_PAGE'],
                    error_out=False)
    next_url = url_for('main.user', username=user.username, page=p.next_num) if p.has_next else None
    prev_url = url_for('main.user', username=user.username, page=p.prev_num) if p.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, form=form, posts=p.items, 
                           next_url=next_url, prev_url=prev_url)

#----------------------------------------------------------------------
# VIEW : EDIT_PROFILE
#----------------------------------------------------------------------

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        # populate the form with db-data 
        form.username.data = current_user.username  
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

#----------------------------------------------------------------------
# VIEW : FOLLOW/<USERNAME>
#----------------------------------------------------------------------

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))

#----------------------------------------------------------------------
# VIEW : UNFOLLOW/USERNAME
#----------------------------------------------------------------------

@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))

#----------------------------------------------------------------------
# VIEW : EXPLORE
#----------------------------------------------------------------------

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    #posts = db.session.scalars(query).all()
    #return render_template('index.html', title='Explore', posts=posts)
    page = request.args.get('page', 1, type=int)
    # paginate returns a paginate-object 
    p = db.paginate(query,
                    page=page, 
                    per_page=current_app.config['APP_POSTS_PER_PAGE'],
                    error_out=False)
    next_url = url_for('main.explore', page=p.next_num) if p.has_next else None
    prev_url = url_for('main.explore', page=p.prev_num) if p.has_prev else None
    # leave out 'form' parameter which is used in index.html (do not need it)
    return render_template('index.html', title='Explore',
                           posts=p.items, next_url=next_url, prev_url=prev_url)

#----------------------------------------------------------------------
# VIEW : TRANSLATE (API CALL) 
#----------------------------------------------------------------------

@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    data = request.get_json()
    return {'text': translate(data['text'], data['source_language'], data['dest_language'])}

#----------------------------------------------------------------------
# VIEW : SEARCH
#----------------------------------------------------------------------

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        # no search terms entered, show all posts
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['APP_POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['APP_POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html',
                           title=current_app.config.get('APP_WINTITLES_SEARCH',
                                                        '___Search Page___'), 
                           posts=posts,
                           next_url=next_url, prev_url=prev_url)  
  
#----------------------------------------------------------------------
# VIEW : /user/<username>/popup
#----------------------------------------------------------------------

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)
