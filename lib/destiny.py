from pyramid.view import view_config
from pyramid.response import Response

from remus.models import *

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import *

import transaction
import json
import logging
log = logging.getLogger(__name__)





def getManifest(session, student_id, test_id):
    """get manifest from database"""
    try:
        query = query = session.query(StudentSession).filter(and_(StudentSession.student_id==student_id,StudentSession.test_id==test_id)).one()
        if query != None:
            return query.manifest
        else:
            return 0

    except NoResultFound:
        return 0

def createStudentSession(session, data):
    """store a session with a manifest"""
    try:
        this_student = StudentSession()
        this_student.student_id = data['student_id']
        this_student.test_id = data['test_id']
        this_student.manifest = data['manifest']

        session.add(this_student)
        session.flush()
        session.commit()

    except:
        session.rollback()
        raise

