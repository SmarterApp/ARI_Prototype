from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    VARCHAR,
    Sequence,
    DateTime,
    ForeignKey,
    Boolean
                        
    )

from sqlalchemy.orm import relationship, backref, aliased

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class StudentSession(Base):
    __tablename__ = 'student_session'
    id = Column(Integer, primary_key=True)
    test_id = Column(Text)
    student_id = Column(Text)
    manifest = Column(Text)

