from pyramid.view import view_config
from pyramid.response import Response


from remus.models import *

from remus.lib import destiny

from sqlalchemy.orm import eagerload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import tempfile


#from passlib.apps import custom_app_context as pwd_context

import os, shutil
import json
import logging
import datetime

import pandas as pd

log = logging.getLogger(__name__)


def login(context, request):
    
    session = request.db

    student_id = request.params['student_id']
    test_id = request.params['test_id']

    file_name = destiny.getManifest(session, student_id, test_id)
    if file_name != 0:
        file_path = os.path.abspath(os.path.join('remus/manifests/', file_name))
        json_data = open(file_path)
        data = json.loads(json_data)

        result = {'manifest': data}

    else:
        result = {'error': 'No Manifest found'}

    response = Response(content_type='text/json')
    response.body = json.dumps(result)
    return response


def createSession(context, request):

    session = request.db

    student_id = request.params['student_id']
    test_id = request.params['test_id']
    manifest = request.params['manifest']
    
    data = {}
    data['student_id'] = student_id
    data['test_id'] = test_id
    data['manifest'] = manifest

    destiny.createStudentSession(session, data)
    
    result = {'error': 0}
    
    response = Response(content_type='text/json')
    response.body = json.dumps(result)
    return response

def itemStream(context, request):
    current_order = request.params['current_order']

    data = {}
    data['1'] = {
        'js_files': "/ari/js/core.js",
        'identifier': 1598,
        'item_type': "multiple_choice",
        'item_subject': "MATH",
        'item_version': 7,
        'ari_version': 1,
        'order': 1,
        'description': "Cloned from ITS 1490 Community Garden Q1",
        'concept': "What Knowledge Do Students Need to Understand This Concept?",
        'prompt': '<p>Which model of the garden represents four rectangular sections for planting vegetables according to the class plan?</p><p style="">&#xA0;</p><p style="">Each square on the model represents 1 square foot. </p>',
        'answers': [
            {
                'name': "Option A",
                'value': '<p style=""><img id="item_1598_graphics1" src="/ari/images/item_1598_v7_graphics1_png256.png" width="439" height="328" style="vertical-align:baseline;" /></p>',
                'order': 1
            },
            {
                'name': "Option B",
                'value': '<p style=""><img id="item_1598_graphics2" src="/ari/images/item_1598_v7_graphics2_png256.png" width="439" height="328" style="vertical-align:baseline;" /></p>',
                'order': 2
            },
            {
                'name': "Option C",
                'value': '<p style=""><img id="item_1598_graphics3" src="/ari/images/item_1598_v7_graphics3_png256.png" width="439" height="332" style="vertical-align:baseline;" /></p>',
                'order': 3
            },
            {
                'name': "Option D",
                'value': '<p style=""><img id="item_1598_graphics4" src="/ari/images/item_1598_v7_graphics4_png256.png" width="439" height="332" style="vertical-align:baseline;" /></p>',
                'order': 4
            },

        ]
    }
    data['2'] = {
        'js_files': "/ari/js/core.js",
        'send_data': "/api/score",
        'identifier': 1448,
        'div': 'container',
        'item_type': "multiple_choice",
        'item_subject': "MATH",
        'item_version': 8,
        'ari_version': 1,
        'order': 2,
        'description': "Cloned from ITS 766",
        'concept': "What Knowledge Do Students Need to Understand This Concept?",
        'prompt': '<p style="">Coffee costs $2 <span id="item_1448_TAG_5" class="its-tag" data-tag="word" data-tag-boundary="start" data-word-index="1"></span>per<span class="its-tag" data-tag-ref="item_1448_TAG_5" data-tag-boundary="end"></span> pound at a coffee shop. <span id="item_1448_TAG_6" class="its-tag" data-tag="word" data-tag-boundary="start" data-word-index="2"></span>Which<span class="its-tag" data-tag-ref="item_1448_TAG_6" data-tag-boundary="end"></span> graph represents this <span id="item_1448_TAG_7" class="its-tag" data-tag="word" data-tag-boundary="start" data-word-index="3"></span>situation<span class="its-tag" data-tag-ref="item_1448_TAG_7" data-tag-boundary="end"></span>?</p>',
        'answers': [
            {
                'name': "Option A",
                'value': '<p style=""><img id="item_1448_graphics1" src="/ari/images/item_1448_v10_graphics1_png256.png" width="221" height="252" style="vertical-align:baseline;" /></p>',
                'order': 1
            },
            {
                'name': "Option B",
                'value': '<p style=""><img id="item_1448_graphics2" src="/ari/images/item_1448_v10_graphics2_png256.png" width="221" height="252" style="vertical-align:baseline;" /></p>',
                'order': 2
            },
            {
                'name': "Option C",
                'value': '<p style=""><img id="item_1448_graphics3" src="/ari/images/item_1448_v10_graphics3_png256.png" width="221" height="252" style="vertical-align:baseline;" /></p>',
                'order': 3
            },
            {
                'name': "Option D",
                'value': '<p style=""><img id="item_1448_graphics4" src="/ari/images/item_1448_v10_graphics4_png256.png" width="221" height="252" style="vertical-align:baseline;" /></p>',
                'order': 4
            } 
        ]
    }

    response = Response(content_type='text/json')
    response.text = json.dumps(data[current_order])
    return response


def itemSave(context, request):
    response = Response(content_type='text/json')
    response.text = json.dumps({'status': 1})
    return response

def convertToCSVLegacy(context, request):

    students = json.loads(request.POST['json_data'])

    data = {
            'Student Last Name': [],
            'Student First Name': [],
            'SSID (consistent with TIDE)': [],
            'Grade': [],
            'Educator(s) completing ISAAP': [],
            'Teacher of Record': [],
            'School ID': [],
            'School Name': [],
            'Abacus': [],
            '*Alternate Response Options (including any external devices/assistive technologies)': [],
            'American Sign Language for ELA Listening and Math Items': [],
            'Bilingual Dictionary for ELA Full Writes (ET)': [],
            'Braille': [],
            'Calculator': [],
            'Closed Captioning for ELA Listening Items': [],
            'Color Contrast (EMBEDDED)': [],
            '*Color Contrast (NON-EMBEDDED)': [],
            'Color Overlays': [],
            '*Magnification': [],
            'Masking': [],
            'Multiplication Table': [],
            'Noise Buffers': [],
            '*Print on Demand': [],
            '*Read Aloud for ELA Reading Passages Grades 6-8 and 11': [],
            '*Read Aloud for Math and ELA Items': [],
            '*Scribe': [],
            '*Scribe (for ELA non-writing items and Math items)': [],
            'Separate Setting': [],
            '*Speech-to-text': [],
            '*Stacked Translations for Math': [],
            '*Text-to-speech for ELA Reading Passages Grades 6-8 and 11': [],
            '*Text-to-speech for Math and ELA Items': [],
            'Translated Text Directions': [],
            'Translated Test Directions for Math': [],
            '*Translation Glossaries for Math (ET) (EMBEDDED)': [],
            'Translation Glossaries for Math (ET) (NON-EMBEDDED)': [],
        }

    for el in students:
        data['Student Last Name'].append(el['lastname'])
        data['Student First Name'].append(el['firstname'])
        data['SSID (consistent with TIDE)'].append(el['ssid'])
        data['Grade'].append(el['grade']['selected']['value'])
        data['Educator(s) completing ISAAP'].append('')
        data['Teacher of Record'].append(el['teacher'])
        data['School ID'].append(el['school_id'])
        data['School Name'].append(el['school_name'])

        try:
            data['Abacus'].append(el['accommodations']['11']['selected']['value'])
        except (NameError, TypeError):
            data['Abacus'].append('')

        try:
            data['*Alternate Response Options (including any external devices/assistive technologies)'].append(el['accommodations']['9']['selected']['value'])
        except (NameError, TypeError):
            data['*Alternate Response Options (including any external devices/assistive technologies)'].append('')

        try:
            data['American Sign Language for ELA Listening and Math Items'].append(el['accommodations']['12']['selected']['value'])
        except (NameError, TypeError):
            data['American Sign Language for ELA Listening and Math Items'].append('')


        try:
            data['Bilingual Dictionary for ELA Full Writes (ET)'].append(el['accommodations']['13']['selected']['value'])
        except (NameError, TypeError):
            data['Bilingual Dictionary for ELA Full Writes (ET)'].append('')


        try:
            data['Braille'].append(el['accommodations']['10']['selected']['value'])
        except (NameError, TypeError):
            data['Braille'].append('')


        try:
            data['Calculator'].append(el['accommodations']['5']['selected']['value'])
        except (NameError, TypeError):
            data['Calculator'].append('')


        try:
            data['Closed Captioning for ELA Listening Items'].append(el['accommodations']['13']['selected']['value'])
        except (NameError, TypeError):
            data['Closed Captioning for ELA Listening Items'].append('')


        try:
            data['Color Contrast (EMBEDDED)'].append(el['designated']['1']['selected']['value'])
        except (NameError, TypeError):
            data['Color Contrast (EMBEDDED)'].append('')


        try:
            data['*Color Contrast (NON-EMBEDDED)'].append(el['designated']['5']['selected']['value'])
        except (NameError, TypeError):
            data['*Color Contrast (NON-EMBEDDED)'].append('')

        try:
            data['Color Overlays'].append(el['designated']['6']['selected']['value'])
        except (NameError, TypeError):
            data['Color Overlays'].append('')

        try:
            data['*Magnification'].append(el['designated']['7']['selected']['value'])
        except (NameError, TypeError):
             data['*Magnification'].append('')

        try:
            data['Masking'].append(el['designated']['2']['selected']['value'])
        except (NameError, TypeError):
            data['Masking'].append('')

        try:
            data['Multiplication Table'].append(el['accommodations']['6']['selected']['value'])
        except (NameError, TypeError):
            data['Multiplication Table'].append('')

        try:
            data['Noise Buffers'].append(el['accommodations']['2']['selected']['value'])
        except (NameError, TypeError):
            data['Noise Buffers'].append('')

        try:
            data['*Print on Demand'].append(el['accommodations']['1']['selected']['value'])
        except (NameError, TypeError):
            data['*Print on Demand'].append('')

        try:
            data['*Read Aloud for ELA Reading Passages Grades 6-8 and 11'].append(el['accommodations']['4']['selected']['value'])
        except (NameError, TypeError):
            data['*Read Aloud for ELA Reading Passages Grades 6-8 and 11'].append('')

        try:
            data['*Read Aloud for Math and ELA Items'].append(el['designated']['9']['selected']['value'])
        except (NameError, TypeError):
            data['*Read Aloud for Math and ELA Items'].append('')

        try:
            data['*Scribe'].append(el['accommodations']['8']['selected']['value'])
        except (NameError, TypeError):
            data['*Scribe'].append('')

        try:
            data['*Scribe (for ELA non-writing items and Math items)'].append(el['designated']['15']['selected']['value'])
        except (NameError, TypeError):
            data['*Scribe (for ELA non-writing items and Math items)'].append('')

        try:
            data['Separate Setting'].append(el['designated']['8']['selected']['value'])
        except (NameError, TypeError):
            data['Separate Setting'].append('')

        try:
            data['*Speech-to-text'].append(el['accommodations']['7']['selected']['value'])
        except (NameError, TypeError):
            data['*Speech-to-text'].append('')

        try:
            data['*Stacked Translations for Math'].append(el['designated']['12']['selected']['value'])
        except (NameError, TypeError):
            data['*Stacked Translations for Math'].append('')

        try:
            data['*Text-to-speech for ELA Reading Passages Grades 6-8 and 11'].append(el['accommodations']['3']['selected']['value'])
        except (NameError, TypeError):
            data['*Text-to-speech for ELA Reading Passages Grades 6-8 and 11'].append('')

        try:
            data['*Text-to-speech for Math and ELA Items'].append(el['designated']['3']['selected']['value'])
        except (NameError, TypeError):
            data['*Text-to-speech for Math and ELA Items'].append('')

        try:
            data['Translated Text Directions'].append(el['designated']['16']['selected']['value'])
        except (NameError, TypeError):
            data['Translated Text Directions'].append('')

        try:
            data['Translated Test Directions for Math'].append(el['designated']['10']['selected']['value'])
        except (NameError, TypeError):
            data['Translated Test Directions for Math'].append('')

        try:
            data['*Translation Glossaries for Math (ET) (EMBEDDED)'].append(el['designated']['11']['selected']['value'])
        except (NameError, TypeError):
            data['*Translation Glossaries for Math (ET) (EMBEDDED)'].append('')

        try:
            data['Translation Glossaries for Math (ET) (NON-EMBEDDED)'].append(el['designated']['14']['selected']['value'])
        except (NameError, TypeError):
            data['Translation Glossaries for Math (ET) (NON-EMBEDDED)'].append('')


    col_order = [
            'Student Last Name',
            'Student First Name',
            'SSID (consistent with TIDE)',
            'Grade',
            'Educator(s) completing ISAAP',
            'Teacher of Record',
            'School ID',
            'School Name',
            'Abacus',
            '*Alternate Response Options (including any external devices/assistive technologies)',
            'American Sign Language for ELA Listening and Math Items',
            'Bilingual Dictionary for ELA Full Writes (ET)',
            'Braille',
            'Calculator',
            'Closed Captioning for ELA Listening Items',
            'Color Contrast (EMBEDDED)',
            '*Color Contrast (NON-EMBEDDED)',
            'Color Overlays',
            '*Magnification',
            'Masking',
            'Multiplication Table',
            'Noise Buffers',
            '*Print on Demand',
            '*Read Aloud for ELA Reading Passages Grades 6-8 and 11',
            '*Read Aloud for Math and ELA Items',
            '*Scribe',
            '*Scribe (for ELA non-writing items and Math items)',
            'Separate Setting',
            '*Speech-to-text',
            '*Stacked Translations for Math',
            '*Text-to-speech for ELA Reading Passages Grades 6-8 and 11',
            '*Text-to-speech for Math and ELA Items',
            'Translated Text Directions',
            'Translated Test Directions for Math',
            '*Translation Glossaries for Math (ET) (EMBEDDED)',
            'Translation Glossaries for Math (ET) (NON-EMBEDDED)',
        ]


    df = pd.DataFrame(data)
    df = df[col_order]

    
    response = Response(content_type='application/octet-stream')
    response.headers['Content-Disposition'] = 'attachment; filename="data.csv"'
    response.charset = 'utf8'
    response.body = df.to_csv(index=False).encode(encoding='UTF-8',errors='strict')
    return response


def convertToCSV(context, request):

    students = json.loads(request.POST['json_data'])

    data = {
            'StudentIdentifier': [],
            'StateAbbreviation': [],
            'Subject': [],
            'AmericanSignLanguage': [],
            'ColorContrast': [],
            'ClosedCaptioning': [],
            'Language': [],
            'Masking': [],
            'PermissiveMode': [],
            'PrintOnDemand': [],
            'Zoom': [],
            'StreamlinedInterface': [],
            'TexttoSpeech': [],
            'Translation': [],
            'NonEmbeddedDesignatedSupports': [],
            'NonEmbeddedAccommodations': [],
            'Other': [],
        }

    for el in students:

        data['StudentIdentifier'].append(el['ssid'])
        data['StateAbbreviation'].append(el['state'])
        data['Subject'].append(el['subject']['selected']['value'])

        
        try:
            data['AmericanSignLanguage'].append(el['accommodations']['12']['selected']['value'])
        except (NameError, TypeError):
            data['AmericanSignLanguage'].append('')

        try:
            data['ColorContrast'].append(el['designated']['1']['selected']['value'])
        except (NameError, TypeError):
            data['ColorContrast'].append('')

        try:
            data['ClosedCaptioning'].append(el['accommodations']['13']['selected']['value'])
        except (NameError, TypeError):
            data['ClosedCaptioning'].append('')

        try:
            data['Language'].append(el['language']['selected']['value'])
        except (NameError, TypeError):
            data['Language'].append('')


        try:
            data['Masking'].append(el['designated']['2']['selected']['value'])
        except (NameError, TypeError):
            data['Masking'].append('')

        try:
            data['PermissiveMode'].append(el['permissive_mode']['selected']['value'])
        except (NameError, TypeError):
            data['PermissiveMode'].append('')

        try:
            data['PrintOnDemand'].append(el['accommodations']['1']['selected']['value'])
        except (NameError, TypeError):
            data['PrintOnDemand'].append('')

        try:
            data['Zoom'].append(el['designated']['18']['selected']['value'])
        except (NameError, TypeError):
            data['Zoom'].append('')

        try:
            data['StreamlinedInterface'].append(el['designated']['17']['selected']['value'])
        except (NameError, TypeError):
            data['StreamlinedInterface'].append('')

        try:
            data['TexttoSpeech'].append(el['designated']['3']['selected']['value'])
        except (NameError, TypeError):
            data['TexttoSpeech'].append('')

        try:
            data['Translation'].append(el['designated']['11']['selected']['value'])
        except (NameError, TypeError):
            data['Translation'].append('')

        non_des = ''
        # Bilingual Dictionary
        try:
            bil = el['designated']['13']['selected']['value']
            if bil == None:
                raise TypeError
            non_des += bil + ";"
        except (NameError, TypeError):
            pass
        # Color Contrast
        try:
            color_contrast = el['designated']['5']['selected']['value']
            if color_contrast == None:
                raise TypeError
            non_des += color_contrast + ";"
        except (NameError, TypeError):
            pass
        # Color Overlay
        try:
            color_overlay = el['designated']['6']['selected']['value']
            if color_overlay == None:
                raise TypeError
            non_des += color_overlay + ";"
        except (NameError, TypeError):
            pass
        # Magnification
        try:
            mag = el['designated']['7']['selected']['value']
            if mag == None:
                raise TypeError
            non_des += mag + ";"
        except (NameError, TypeError):
            pass
        # Noise Buffers
        try:
            noise_buff = el['accommodations']['2']['selected']['value']
            if noise_buff == None:
                raise TypeError
            if noise_buff == 'NEA_NoiseBuf':
                noise_buff = 'NEDS_NoiseBuf'
            non_des += noise_buff + ";"
        except (NameError, TypeError):
            pass
        # Read Aloud
        try:
            read_aloud = el['designated']['9']['selected']['value']
            if read_aloud == None:
                raise TypeError
            non_des += read_aloud + ";"
        except (NameError, TypeError):
            pass
        # Read Aloud in Spanish
        try:
            non_des += ''
        except (NameError, TypeError):
            pass
        # Separate Setting
        try:
            seperate_setting = el['designated']['8']['selected']['value']
            if seperate_setting == None:
                raise TypeError
            non_des += seperate_setting + ";"
        except (NameError, TypeError):
            pass
        # Translated Test Directions
        try:
            translated = el['designated']['16']['selected']['value']
            if translated == None:
                raise TypeError
            non_des += translated + ";"
        except (NameError, TypeError):
            pass
        # Translation (Glossary) 
        try:
            translation = el['designated']['14']['selected']['value']
            if translation == None:
                raise TypeError
            if translation == 'English':
                translation = 'TDS_WL_Glossary'
            non_des += translation + ";"
        except (NameError, TypeError):
            pass

        non_des = non_des.replace(';;', ';')
        data['NonEmbeddedDesignatedSupports'].append(non_des)


        non_accom = ''
        # Abacus
        try:
            abacus = el['accommodations']['11']['selected']['value']
            if abacus == None:
                raise TypeError
            if abacus == 'NEA_Abacus (Math only)':
                abacus = 'NEA_Abacus'
            non_accom += abacus + ";"
        except (NameError, TypeError):
            pass
        # *Alternate Response Options (including any external devices/assistive technologies)
        try:
            alt = el['accommodations']['9']['selected']['value']
            if alt == None:
                raise TypeError
            non_accom += alt + ";"
        except (NameError, TypeError):
            pass
        # Calculator
        try:
            calc = el['accommodations']['5']['selected']['value']
            if calc == None:
                raise TypeError
            if calc == 'NEA_Calc (Math only)':
                calc = 'NEA_Calc'
            non_accom += calc + ";"
        except (NameError, TypeError):
            pass
        # Multiplication Table
        try:
            mult = el['accommodations']['6']['selected']['value']
            if mult == None:
                raise TypeError
            if multi == 'NEA_MT (Math only)':
                multi = 'NEA_MT'
            non_accom += multi + ";"
        except (NameError, TypeError):
            pass
        # Print on Demand
        #try:
        #    non_accom += el['accommodations']['1']['selected']['value'] + ";"
        #except (NameError, TypeError):
        #    pass
        # Read Aloud - *Read Aloud for ELA Reading Passages Grades 6-8 and 11
        try:
            read = el['accommodations']['4']['selected']['value']
            if read == None:
                raise TypeError
            if read == 'NEA_RA_Stimuli (ELA only)':
                read = 'NEA_RA_Stimuli'
            non_accom += read + ";"
        except (NameError, TypeError):
            pass
        # Scribe
        try:
            scribe = el['accommodations']['8']['selected']['value']
            if scibe == None:
                raise TypeError
            if scribe == 'NEA_SC_WritItems (ELA only)':
                scribe = 'NEA_SC_WritItems'
            non_accom += scribe + ";"
        except (NameError, TypeError):
            pass
        # Speech-to-text
        try:
            speech = el['accommodations']['7']['selected']['value']
            if speech == None:
                raise TypeError
            non_accom += speech + ";"
        except (NameError, TypeError):
            pass

        non_accom = non_accom.replace(';;', ';')
        data['NonEmbeddedAccommodations'].append(non_accom)


        try:
            data['Other'].append('')
        except (NameError, TypeError):
            data['Other'].append('')



    col_order = [
            'StudentIdentifier',
            'StateAbbreviation',
            'Subject',
            'AmericanSignLanguage',
            'ColorContrast',
            'ClosedCaptioning',
            'Language',
            'Masking',
            'PermissiveMode',
            'PrintOnDemand',
            'Zoom',
            'StreamlinedInterface',
            'TexttoSpeech',
            'Translation',
            'NonEmbeddedDesignatedSupports',
            'NonEmbeddedAccommodations',
            'Other',
        ]


    df = pd.DataFrame(data)
    df = df[col_order]

    
    response = Response(content_type='application/octet-stream')
    response.headers['Content-Disposition'] = 'attachment; filename="data.csv"'
    response.charset = 'utf8'
    response.body = df.to_csv(index=False).encode(encoding='UTF-8',errors='strict')
    return response



def convertToCSV2(context, request):

    session = request.db

    students = json.loads(request.POST['json_data'])

    #students = request.json_body['students']

    fp = ''

    for el in students:
        fp += el['firstname']+','+el['lastname']+','+el['ssid']+','+el['school']+','+el['grade']+','+el['teacher']

        this_item = el['universal_tools']
        this_list = (
                'Breaks', 
                'Calculator', 
                'Digital Notes' , 
                'English Dictionary', 
                'English Glossary', 
                'Expandable Passages', 
                'Global Notes', 
                'Highlighter', 
                'Keyboard Navigation', 
                'Mark for Review', 
                'Math Tools', 
                'Spell Check', 
                'Strikethrough', 
                'Writing Tools', 
                'Zoom'
                )
        for el2 in this_list:
            x = list(filter(lambda x: x['text'] == el2, this_item))[0]
            if (x['select'] == True):
                fp += ','+x['text']
            else:
                fp += ',,'



        this_item = el['universal_tools_ne']
        this_list = (
                'Breaks', 
                'Scratch Paper', 
                'Thesaurus' , 
                'English Dictionary', 
                )
        for el2 in this_list:
            x = list(filter(lambda x: x['text'] == el2, this_item))[0]
            if (x['select'] == True):
                fp += ','+x['text']
            else:
                fp += ',,'


        this_item = el['ident_student_needs']
        this_list = (
                'Individualized Education Program', 
                '504 Plan', 
                'Educator(s) Recommendation', 
                )
        for el2 in this_list:
            x = list(filter(lambda x: x['text'] == el2, this_item))[0]
            if (x['select'] == True):
                fp += ','+x['text']
            else:
                fp += ',,'


        fp += '\n'

    response = Response(content_type='application/octet-stream')
    response.headers['Content-Disposition'] = 'attachment; filename="data.csv"'
    response.charset = 'utf8'
    response.body = fp.encode(encoding='UTF-8',errors='strict')
    return response


def saveToJSON(context, request):

    #students = request.POST['json_data']
    students = request.json_body['students']

    #response = Response(content_type='application/octet-stream')
    #response = Response(content_type='text/plain;charset=utf-8')
    #date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #response.headers['Content-Disposition'] = 'attachment; filename="save-'+date+'.json"'
    #response.charset = 'utf8'
    #response.body = json.dumps(students).encode(encoding='UTF-8',errors='strict')
    #response.text = students
    return students







