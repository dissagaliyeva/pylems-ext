import os
import pytest
import pylems_code.utils as utils
from pylems_code.models import Models


class TestModels:
    def setup(self):
        # test default models with no parameters
        self.model = Models()
        path = os.path.join('../examples', 'default_param.xml')

        assert self.model.params is None, 'No parameters expected'
        assert self.model.output == '../examples'
        assert self.model.path == path
        assert os.path.exists(path), f'Expected {path} to be present'

        # open param.xml


