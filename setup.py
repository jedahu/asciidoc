from distutils.core import setup
from glob import glob
from os.path import join, dirname, isdir, isfile, splitext
from os import listdir
import sys
import imp

EXTRA_PATH='asciidoc'
MANIFEST_LIST='MANIFEST.list'

# Is there a better way to do this?
def install_dir():
  '''Return directory where asciidoc.py is installed'''
  return join(
      sys.prefix, 'lib', 'python' + sys.version[:3], 'site-packages', EXTRA_PATH)

# Modified from
# http://wiki.python.org/moin/Distutils/Cookbook/AutoDataDiscovery
def non_python_files(install_prefix, path):
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
            all_results.extend(non_python_files(install_prefix, name))
    if result:
        all_results.append((join(install_prefix, path), result))
    return all_results

def data_files_from_manifest(install_prefix):
  '''Use MANIFEST to generate a list for the data_files parameter'''
  out = []
  with open(MANIFEST_LIST) as manifest:
    for line in manifest:
      for path in glob(line.strip()):
        print 'PATH', path
        if isdir(path):
          out.extend(non_python_files(install_prefix, path))
        else:
          out.append((join(install_prefix, dirname(path)), [path]))
  return out

setup(
    name='AsciiDoc',
    version='8.6.8',
    author='Stuart Rackham',
    author_email='srackham@gmail.com',
    url='http://methods.co.nz/asciidoc/',
    license='GPL license, see COPYING',
    description='Simple blog engine.',
    long_description=open('README.txt').read(),
    scripts=['asciidoc'],

    # If asciidoc(api).py were in a package, the packages, package_dir, and
    # package_data args could be used instead of the three below and that awful
    # install_dir hack.
    py_modules=['asciidoc', 'asciidocapi'],
    extra_path=EXTRA_PATH,
    data_files=data_files_from_manifest(install_dir())
    )
