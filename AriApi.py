from pyramid.view import view_config
from pyramid.response import Response


from remus.models import *

from remus.lib import destiny

from sqlalchemy.orm import eagerload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import tempfile
from pyramid.session import signed_serialize, signed_deserialize


#from passlib.apps import custom_app_context as pwd_context

import os, shutil
import json
import logging
import datetime

import pandas as pd

log = logging.getLogger(__name__)
json_path = os.path.dirname(os.path.realpath(__file__)) + '/static/ari3/json/'
item_path = os.path.dirname(os.path.realpath(__file__)) + '/static/ari3/items/'


def getAssessment(context, request):

    json_file = json_path + 'assessment.json'
    with open(json_file, 'r') as myfile:
        json_data = myfile.read()

    return json_data

def getItem(context, request):

    response = Response(content_type='application/json')

    json_files = ['/q1/item.json', '/q2/item.json', '/q3/item.json', '/q4/item.json', '/q5/item.json']

    try:
        # get cookies
        cookieval = request.cookies['signed_cookie']
        cookies = signed_deserialize(cookieval, 'secret')
        count = cookies['c']

        # set next one
        next_count = count + 1
        cookieval = signed_serialize({'c': next_count}, 'secret')
        response.set_cookie('signed_cookie', cookieval)

    except KeyError:
        cookieval = signed_serialize({'c': 0}, 'secret')
        response.set_cookie('signed_cookie', cookieval)
        count = 0

    json_file = item_path + json_files[count]

    with open(json_file, 'r') as myfile:
        json_data = myfile.read()

    response.charset = 'utf8'
    response.text = json_data
    return response


