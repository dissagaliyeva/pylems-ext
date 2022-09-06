import os


TVB_MODELS = {
    'SJHM3D': {'name': 'hindmarshrose',
                                'desc': 'These are the equations to simulate the time series with the '
                                        'Stefanescu-Jirsa 3D (reduced Hindmarsh-Rose model) model.',
                                'params': dict(r=[0.006], a=[1.], b=[3.], c=[1.], d=[5.], s=[1.], xo=[-1.6], K11=[0.5],
                                               K12=[0.1], K21=[0.15], sigma=[0.3], mu=[3.3], x_1=[-1.6], A_ik=None,
                                               B_ik=None,
                                               C_ik=None, a_i=None, b_i=None, c_i=None, d_i=None, e_i=None, f_i=None,
                                               h_i=None,
                                               p_i=None, IE_i=None, II_i=None, m_i=None, n_i=None,
                                               variables_of_interest=['xi', 'eta', 'tau'],
                                               state_variable_range=dict(x=[-4., 4.], y=[-60., 20.], z=[-2., 18.],
                                                                         eta=[-25., 20.0],
                                                                         alpha=[-4., 4.], beta=[-20., 20.],
                                                                         gamma=[2., 10.]))}
}


# open file and prepare the dataset
def open_file(path: str) -> list:
    """

    :param path:
    :return:
    """

    # verify the path exists
    assert os.path.exists(path), f'File at location {path} does not exist'

    # define an array to store line-by-line iteration
    contents = []

    # open file
    with open(path) as file:
        # iterate over lines of code and pick the relevant lines only
        for line in file.readlines():
            # ignore comments, empty lines, and imports
            if not line.startswith('#') and not line.startswith('import') and \
                    not line.startswith('from') and line != '\n':
                # save relevant lines
                contents.append(line.strip('\n').strip())

    return contents


def preprocess_params(dictionary: dict) -> dict:
    temp = {}

    for k, v in dictionary.items():
        if isinstance(v, list) and len(v) == 1:
            temp[k] = v[0]
        else:
            temp[k] = v

    return temp
