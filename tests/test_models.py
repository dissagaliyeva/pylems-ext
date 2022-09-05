import os
import lems.api as lems
import pylems_code.utils as utils
from pylems_code.models import Models


pythonpath = [
    '.',
    'pylems_code'
]


def test_models():
    # test default models with no parameters
    model = Models()
    path = os.path.join('examples', 'default_param.xml')
    check(model, path)

    # check with uid and suffix
    model = Models(uid='delta_times', suffix='50healthy')
    path = os.path.join('examples', 'desc-50healthy_param.xml')
    check(model, path)

    # check with app=True
    model = Models(uid='delta_times', suffix='50healthy', app=True)
    for path in ['desc-50healthy_param.xml', 'desc-50healthy_eq.xml', 'model-SJHM3D_delta_times.xml']:
        check(model, os.path.join('examples', path))


def check(model, path):
    assert model.params == {}, 'No parameters expected'
    assert isinstance(model.model, lems.Model), 'Model must be of lems.api.Model instance'
    assert os.path.exists(path), f'Expected {path} to be present'
    assert model.comp_type in ['SJHM3D', 'WongWang']


if __name__ == '__main__':
    test_models()