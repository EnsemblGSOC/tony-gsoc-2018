from base import *
from sqlalchemy import create_engine
import ast

with open("../../scripts/config.py") as configfile:
    config = ast.literal_eval(configfile.read())

tony_assembly = config["tony_assembly"]

engine = create_engine(tony_assembly)
Base.metadata.create_all(engine)