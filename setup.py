#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from setuptools import findall
files = findall()
install_requires = []

try:
    __import__('uuid')
except ImportError:
    install_requires.append('uuid')

packages = find_packages(exclude=("core.*", "core", "settings", "conf", "tsktsk", 'example', 'example.*'))

setup(
        name="django-progressable",
        version=".".join(map(str, __import__('progressable').__version__)),
        description="Create celery tasks that can be visible in the admin.",
        author="Jacco Flenter @ Secret Code Machine",
        author_email="jacco(_AT_)secretcodemachine.com",
        dependency_links = [
            "http://github.com/flenter/redisco/tarball/master#egg=redisco-0.1.3-datefix",
        ],
        install_requires = [
            'redisco ==0.1.3-datefix',
            'django-tastypie >=0.9.9',
            'django-celery>=2.5.2',
        ],
        packages = packages,
        include_package_data=True,
        long_description = """
        Create tasks that can show up in the admin interface (with progress information)
        . It assumes redis 
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
          "Operating System :: OS Independent",
        ],
    )

