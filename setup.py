from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pylems_codext',
    version='0.0.4',
    description='Python code traversal to XML',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    author='Dinara Issagaliyeva',
    author_email='dinarissaa@gmail.com',
    url='https://github.com/dissagaliyeva/pylems-ext',
    license='MIT',
    classifiers=classifiers,
    keywords='pylems',
    packages=find_packages(),
    data_files=[('pylems_codext', ['templates/hindmarshrose.txt'])],
    include_package_data=True,
    install_requires=['pylems']
)
