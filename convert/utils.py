# TVB_MODELS = ['BASE_MODEL', 'COOMBES_BYRNE', 'COOMBES_BYRNE_2D', 'DUMONT_GUTKIN', 'EPILEPTOR', 'EPILEPTOR_2D',
#               'EPILEPTOR_CODIM_3', 'EPILEPTOR_CODIM_3_SLOW', 'EPILEPTOR_RS', 'GAST_SCHMIDT_KNOSCHE_SD',
#               'GAST_SCHMIDT_KNOSCHE_SF ', 'GENERIC_2D_OSCILLATOR', 'HOPFIELD', 'JANSEN_RIT', 'KURAMOTO',
#               'LARTER_BREAKSPEAR', 'LINEAR', 'MONTBRIO_PAZO_ROXIN', 'REDUCED_SET_FITZ_HUGH_NAGUMO',
#               'REDUCED_SET_HINDMARSH_ROSE', 'REDUCED_WONG_WANG', 'REDUCED_WONG_WANG_EXCH_INH', 'SUP_HOPF ',
#               'WILSON_COWAN', 'ZERLAUT_FIRST_ORDER', 'ZERLAUT_SECOND_ORDER', 'ZETTERBERG_JANSEN']
import os.path

TVB_MODELS = {
    'ReducedSetHindmarshRose': 'hindmarshRose'
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
