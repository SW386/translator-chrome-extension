# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
from firebase_admin import credentials, storage

# Cloud functions
from google.cloud import vision, translate_v2 as translate

# Convenience


# All the authentication, passwords, user thingys go here


# initialize_app()
#
#
# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")


# Initialize Firebase
cred = credentials.Certificate('path_to_your_firebase_service_account_file.json')
initialize_app(cred, {
    'storageBucket': 'your-app-id.appspot.com'
})


# Initialize Google Cloud Vision and Translate
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()

def upload_image(image_path):
    '''
    Firebase stuff

    I'm not sure about the exact fireship mechanisms, but this should add all our images into a folder
    '''
    bucket = storage.bucket()
    blob = bucket.blob(image_path)
    blob.upload_from_filename(image_path)
    return blob.public_url


def extract_text_from_image(image_url):
    '''
    Pass in the firebase bucket

    Vision docs
    https://googleapis.dev/nodejs/vision/latest/v1.ImageAnnotatorClient.html
    '''
    image = vision.Image()
    image.source.image_uri = image_url

    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ''


def translate_text(text, target_language="en"):
    '''
    Translate docs
    https://cloud.google.com/python/docs/reference/translate/latest/client
    '''
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']


def main(image_path, target_language="en"):
    '''
    
    '''
    image_url = upload_image(image_path)
    extracted_text = extract_text_from_image(image_url)
    translated_text = translate_text(extracted_text, target_language)
    return translated_text
