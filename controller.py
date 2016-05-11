from pyramid.view import view_config
from remus.models import *
from pyramid.renderers import render
from pyramid.response import Response

from remus.lib import destiny

from sqlalchemy.orm import eagerload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

#from passlib.apps import custom_app_context as pwd_context

import os, shutil
import json
import logging
log = logging.getLogger(__name__)


def controller(context, request):

    manifest = json.dumps({
        'identifier': None,
        'assessment_subject': "MATH",
        'assessment_version': "1",
        'assessment_grade': 5,
        'ari_verion': 1,
        'item_stream': "/api/itemStream",
        'item_save': '/api/itemSave',
        'div': 'container',
    })
    
    result = render('templates/controller.pt',
                              {'manifest': manifest},
                              request=request)
    response = Response(result)
    response.content_type = 'text/html'
    return response

