from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class GCA(Base):
    __tablename__ = 'GCA'
    id = Column(Integer, primary_key=True)
    accession = Column(String(20), unique=True)
    status = Column(Integer)
    chromosome = relationship("Chromosome")
    records = Column(Integer)
    assembly_level = Column(String(50))


class Chromosome(Base):
    __tablename__ = 'Chromosome'
    id = Column(Integer, primary_key=True)
    GCA_accession = Column(String(20), ForeignKey("GCA.accession"))
    accession = Column(String(20))
    md5 = Column(String(32))
    length = Column(Integer)
    name = Column(String(50))
    status = Column(Integer)


class Jobs(Base):
    __tablename__ = 'Jobs'
    id = Column(Integer, primary_key=True)
    chromosome_accession = Column(String(20))
    job_name = Column(String(20))
    SHA1 = Column(String(40))
    status = Column(Integer)
