##### Instructions to install cython #####
# 1) Install python developer tools: sudo apt-get install python-dev #
# 2) Install cython: easy_install cython

##### Instructions to compile cython file #####
# Run: python setup.py build_ext --inplace #

from distutils.core import setup 
from Cython.Build import cythonize 

setup(
	ext_modules = cythonize("directio.pyx")
)

