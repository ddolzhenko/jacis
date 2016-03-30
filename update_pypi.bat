
rem @echo off

@echo Continue?

python setup.py register -r pypitest
@pause
python setup.py sdist upload -r pypitest
@pause
python setup.py register -r pypi
@pause
python setup.py sdist upload -r pypi
@pause
