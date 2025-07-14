import os
import json
import pprint
import sys
from app.utils import print_console
from dotenv import load_dotenv
from collections import ChainMap


class Config:
    pass


def build_db_uri(prefix, dirpath, filename):
    if dirpath:
        path = os.path.abspath(os.path.dirname(__file__))
        return prefix + os.path.join(path, filename)
    else:
        return prefix + filename

def chain_maps(dicts):
    """
    The input can be any number of dicts; the first pair are chained together. 
    If there are any sub-dicts with the same keys, then those are chained
    together also.
    Then the process will be repeated with the result and the next dict.
    """
    def chain_recursive(d1, d2):
        chain = ChainMap(d1, d2)
        for k, v in d1.items():
            if isinstance(v, dict) and k in d2:
                chain[k] = chain_recursive(d1[k], d2[k])
        return chain

    if len(dicts) == 0:
        return {}
    elif len(dicts) == 1:
        return dicts[0]
    else:
        chained = chain_recursive(dicts[0], dicts[1])
        for d in dicts[2:]:
            chained = chain_recursive(chained, d)
    return chained

def load_settings(filename):
    # assume file name is 'env-<env>.json'
    print_console(f"parsing file {filename}")
    with open(filename) as f:
        settings = json.load(f)
    return settings

def init_config(*config_filepath):

    def walk_dict_recursive(cfgvars, dict_, grp=""):
        """
        Helper-function to create a list of config vars.
        """
        for k, v in dict_.items():
            if isinstance(v, dict) or isinstance(v, ChainMap) :
                 prev_grp = grp
                 grp += ("_" + k) if grp else k
                 walk_dict_recursive(cfgvars, v, grp=grp)
                 grp = prev_grp 
            else:
                if grp:
                    cfgvars.append( (f"{grp}_{k}", v) ) 
                else:
                    cfgvars.append( (k, v) )

    load_dotenv()
    config_filepaths = os.environ['JSON_CONFIG_FILES'].split(';')

    config_dicts = []
    config_vars = []


    # read all json files in seperat dicts

    for fpath in config_filepaths:
        config_dicts.append(load_settings(fpath))

    chained_configs = chain_maps(config_dicts)

    if not chained_configs:
        raise ValueError("No data parsed from Microblog configuration file(s).")

    walk_dict_recursive(config_vars, chained_configs)

    for k, v in sorted(config_vars):
        print("adding class var: ", k, " -- ", v)
        setattr(Config, k.upper(), v)

    if not Config.SECRETS_DB_URI:
        Config.SECRETS_DB_URI = build_db_uri(prefix=Config.SECRETS_DB_PREFIX, 
                                            dirpath=Config.SECRETS_DB_DIRPATH, 
                                            filename=Config.SECRETS_DB_FILENAME)
        Config.SQLALCHEMY_DATABASE_URI = Config.SECRETS_DB_URI
    else:
        Config.DATBASE_URL=Config.SECRETS_DB_URI
        Config.SQLALCHEMY_DATABASE_URI = Config.SECRETS_DB_URI

    # MANDAORY config variables demandes by Flask, SQLAlchemy , Flask-Mail
    Config.SECRET_KEY = Config.SECRETS_FLASK_KEY
    Config.MAIL_SERVER = Config.SECRETS_MAIL_SERVER
    Config.MAIL_PORT = Config.SECRETS_MAIL_PORT
    Config.MAIL_USERNAME = Config.SECRETS_MAIL_USERNAME
    Config.MAIL_PASSWORD = Config.SECRETS_MAIL_PASSWORD
    Config.MAIL_USE_TLS = Config.SECRETS_MAIL_USE_TLS


# init the config during loading
print_console("running config.py")
init_config()

