from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pylems_py2xml',
    version='1.0.0',
    description='Python code traversal to XML',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Dinara Issagaliyeva',
    author_email='dinarissaa@gmail.com',
    url='https://github.com/dissagaliyeva/pylems-ext',
    license='MIT',
    classifiers=classifiers,
    keywords=['pylems', 'xml'],
    packages=['pylems_py2xml'],
    package_dir={'pylems_py2xml': 'src/pylems_py2xml'},
    package_data={'pylems_py2xml': ['data/*.xml']},
    install_requires=['pylems']
)
