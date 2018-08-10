# Copyright 2018 Tony Zeyu Yang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
