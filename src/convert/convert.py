import os
from utils import *
import lems.api as lems


class XML:
    def __init__(self, input_path, output_path, unit):
        self.input_path = input_path
        self.output_path = output_path
        self.unit = unit

        self.content = open_file(input_path)        # get content from the input path
        self.model = lems.Model()                   # define LEMS model




