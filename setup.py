from setuptools import setup, find_packages


setup(

    name         = 'jacis',
    version      = '0.1.1',

    description  = '[STUB ONLY] Just Another Continuous Integration System',
    keywords     = ['ci', 'continuous integration', 'integration', 'build', 'c++'], # arbitrary keywords

    author       = 'Dmitry Dolzhenko',
    author_email = 'd.dolzhenko@gmail.com',

    # scripts      = [ 'bin/jacis'],
    entry_points = {
        'console_scripts': [
            'jacis = jacis.console:main',
        ],
    },
    packages     = find_packages(),
    test_suite   = 'jacis.core.get_tests',

    url          = 'https://github.com/ddolzhenko/jacis', # use the URL to the github repo
    download_url = 'https://github.com/ddolzhenko/jacis/archive/v0.1.tar.gz', # I'll explain this in a second

    classifiers  = [],
    install_requires = [
        "checksumdir==1.0.5",
        "GitPython==3.1.34",
        "svn==0.3.36"
    ],
)
