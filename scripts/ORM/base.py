from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class GCA(Base):
    __tablename__ = 'GCA'
    id = Column(Integer, primary_key=True)
    accession = Column(String, unique=True)
    status = Column(Boolean)
    chromosome = relationship("Chromosome")
    records = Column(Integer)


class Chromosome(Base):
    __tablename__ = 'Chromosome'
    id = Column(Integer, primary_key=True)
    GCA_accession = Column(String, ForeignKey("GCA.accession"))
    accession = Column(String)
    md5 = Column(String)
    length = Column(Integer)
    name = Column(String)
    status = Column(Boolean)


class Jobs(Base):
    __tablename__ = 'Jobs'
    id = Column(Integer, primary_key=True)
    chromosome_accession = Column(String)
    job_name = Column(String)
    status = Column(Boolean)