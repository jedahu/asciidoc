from distutils.core import setup
from glob import glob
from os.path import join, dirname, isdir, isfile, splitext
from os import listdir
import sys
import imp

MANIFEST_LIST='PKG_MANIFEST'

# Modified from
# http://wiki.python.org/moin/Distutils/Cookbook/AutoDataDiscovery
def non_python_files(path):
    """ Return all non-python-file filenames in path """
    result = []
    all_results = []
    module_suffixes = [info[0] for info in imp.get_suffixes()]
    ignore_dirs = ['cvs']
    for item in listdir(path):
        name = join(path, item)
        if (
            isfile(name) and
            splitext(item)[1] not in module_suffixes
            ):
            result.append(name)
        elif isdir(name) and item.lower() not in ignore_dirs:
            all_results.extend(non_python_files(name))
    if result:
        all_results.append((path, result))
    return all_results

def files_from_manifest():
  '''Use MANIFEST to generate a list for the data_files parameter'''
  with open(MANIFEST_LIST) as manifest:
    return [x.strip() for x in manifest.readlines()]

setup(
    name='AsciiDoc',
    version='8.6.8-jedahu-beta',
    author='Stuart Rackham',
    author_email='srackham@gmail.com',
    url='http://methods.co.nz/asciidoc/',
    license='GPL license, see COPYING',
    description='Simple blog engine.',
    long_description=open('README.txt').read(),
    scripts=['scripts/asciidoc'],
    py_modules=['asciidocapi'],
    packages=['asciidoc'],
    package_dir={'asciidoc': 'asciidoc'},
    package_data={'asciidoc': files_from_manifest()},
    include_package_data=True
    )
