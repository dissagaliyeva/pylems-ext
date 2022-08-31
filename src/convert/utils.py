import os

TVB_MODELS = {
    'ReducedSetHindmarshRose': {'name': 'hindmarshRose',
                                'desc': 'These are the equations to simulate the time series with the '
                                        'Stefanescu-Jirsa 3D (reduced Hindmarsh-Rose model) model.'}
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
