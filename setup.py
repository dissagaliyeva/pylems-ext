from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pylems_code',
    version='0.0.1',
    description='Python code traversal to get models',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Dinara Issagaliyeva',
    author_email='dinarissaa@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='pylems',
    packages=find_packages(),
    install_requires=['pylems']
)