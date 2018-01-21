try:
    from setuptools import setup, find_packages
    from setuptools.extension import Extension
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
    from distutils.core import setup, find_packages
    from distutils.extension import Extension

extra_opts = {}

try:
    with open("README.md", "r") as fd:
        extra_opts['long_description'] = fd.read()
except IOError:
    pass        # Install without README.md

packages = ["mongo_connector", "mongo_connector.doc_managers"]
package_metadata = {
    "name": "cosmos-doc-manager",
    "version": "0.0.1",
    "description": "Azure Cosmos DB Doc Manager for Mongo Connector",
    "long_description": "Cosmos Doc Manager is a tool that will import data from MongoDB to " 
                        "Azure Cosmos DB, via Mongo-Connector.",
    "author": "Syed Hassaan Ahmed",
    "author_email": "hassaan.brix@gmail.com",
    "url": "https://github.com/syedhassaanahmed/cosmos_doc_manager.git",
    "entry_points": {
        "console_scripts": [
            'mongo-connector = mongo_connector.connector:main',
        ],
    },
    "packages": packages,
    "install_requires": ['mongo-connector>=2.5.1', 'pydocumentdb>=2.3.1'],
    "license": "MIT License",
    "classifiers": [
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        "Topic :: Database",
        "Topic :: Software Development",
    ],
}

try:
    setup(ext_modules=extensions, **package_metadata)
except:
    setup(**package_metadata)