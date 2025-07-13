from flask import current_app
import requests


def translate(text, source_language, dest_language):
    if 'SECRETS_MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['SECRETS_MS_TRANSLATOR_KEY']:
        return 'Error: the translation service is not configured.'
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['SECRETS_MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'westeurope'
    }
    r = requests.post(
        'https://api.cognitive.microsofttranslator.com'
        '/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth, json=[{'Text': text}])
    if r.status_code != 200: 
        return 'Error: the translation service failed.'
    return r.json()[0]['translations'][0]['text']
