#!/usr/bin/env python

#from setuptools import setup
#
#import os
#data_files = []
#
#for dirpath, dirnames, filenames in os.walk('progressable'):
#  for i, dirname in enumerate(dirnames):
#    if dirname.startswith('.'): del dirnames[i]
#  if not '__init__.py' in filenames and filenames:
#    data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
#
try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages, Command

from setuptools import findall
files = findall()
install_requires = []

try:
    __import__('uuid')
except ImportError:
    install_requires.append('uuid')

data_files = find_packages("progressable")
packages = find_packages(exclude=("core.*", "core", "settings", "conf", "tsktsk", 'example', 'example.*'))

#print data_files

setup(
        name="django-progressable",
        version="0.3",
        description="Create celery tasks that can be visible in the admin.",
        author="Jacco Flenter @ Secret Code Machine",
        author_email="jacco(_AT_)secretcodemachine.com",
        dependency_links = [
            "http://github.com/flenter/redisco/tarball/master#egg=redisco-0.1.3-datefix",
        ],
        install_requires = [
            'redisco ==0.1.3-datefix',
            'django-tastypie >=0.9.9',
        ],
        packages = packages,
        #data_files = data_files,
        zip_safe = False,
        package_data={'progressable':['progressable/templates/*']},
        include_package_data=True,
        long_description = """
        Create tasks that can show up in the admin interface. It assumes redis 
        is the backend for celery and provides a restful api to the tasks.

        Note: if you get an exception in the admin (complaining about an index
        out of range), please use the patched version of redisco from github:
        https://github.com/flenter/redisco/

        See the example project for all dependencies
        """,
        license="BSD",
        keywords="redis, celery, django, tastypie, admin, tools, redisco, json",
        url='https://github.com/flenter/django-progressable/',
        classifiers = [
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: BSD License",
        ],
    )

