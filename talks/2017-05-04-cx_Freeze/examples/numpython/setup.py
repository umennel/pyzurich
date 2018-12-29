import sys
import os

from cx_Freeze import setup, Executable

build_exe_options = {
    'includes': ['numpy.core._methods', 
                 'numpy.lib.format',
                 'matplotlib.backends.backend_tkagg',
                 'tkinter',
                 'tkinter.filedialog'],
    'zip_include_packages': '*',
    'zip_exclude_packages': [],
    #'zip_include_packages': ['matplotlib'],
    #'zip_exclude_packages': ['numpy']
}

executables = [Executable(os.path.join(os.path.dirname(__file__), 'shell.py'), 
                          targetName='numpython', initScript='Console')]

setup(name='numpython',
      version='0.1',
      description = "An interactive shell to do numerical stuff",
      scripts=['shell.py'],
      options = {"build_exe": build_exe_options},
      executables = executables,
      requires=['numpy', 'matplotlib']
     )


