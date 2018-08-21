"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from base import *
from sqlalchemy import create_engine
import ast
import sys

config_path = sys.argv[1]

with open(config_path) as configfile:
    config = ast.literal_eval(configfile.read())

tony_assembly = config["tony_assembly"]

engine = create_engine(tony_assembly)
Base.metadata.create_all(engine)