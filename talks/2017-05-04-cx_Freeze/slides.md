class: center, middle

# Deploying Python Applications with cx_Freeze

Uche Mennel

May 4 2017 — PyZurich

---

# Agenda

1. Why cx_Freeze?
2. Basic Usage
3. How it works

---

# Why cx_Freeze?

 * Makes your Python app available on other machines

 * Minimal requirements on target machine

 * Detects and includes dependecies

 * Hooks for many well known packages

 * Works on any platform you can run Python

 * Compressed code archive

---

# Why cx_Freeze?

## Alternatives? ##

 * Can't I copy my virtual environment?
     - Dependencies outside environment folder
     - pip install -e (development mode)
     - Conflicts with existing Python installations
     - Reacts on certain environment variables (e.g. `PYTHONPATH`)

 * py2exe and py2app?
     - Not platform independent

 * Docker
     - Need docker to run

---

# Basic Usage #

## cxfreeze script ##

  * cxfreeze script is installed with cx_Freeze 

  ```bash
  myenv/bin/cxfreeze hello.py --target-dir dist
  ```

  * Use this only for very simple scripts

  * Check the [documentation](http://cx-freeze.readthedocs.io/en/latest/script.html) for more customization options

---

# Basic Usage #

## distutils setup script ##

  * Create script called `setup.py`

  * Specify `cx_Freeze.Executable` in setup function 

  * cx_Freeze provides distutils commands for creating executables but also installers

  * Check the [documentation](http://cx-freeze.readthedocs.io/en/latest/distutils.html) for more customization options


---

# Basic Usage #

## Example ##

```python
import sys
import os

from cx_Freeze import setup, Executable

build_exe_options = {
    'includes': ['numpy.core._methods', 'numpy.lib.format', 'matplotlib.backends.backend_tkagg', 'tkinter', 'tkinter.filedialog']
}

executables = [Executable(os.path.join(os.path.dirname(__file__), 'shell.py'), 
                          targetName='numpython')]

setup(name='numpython',
      version='0.1',
      description = "An interactive shell to do numerical stuff",
      scripts=['shell.py'],
      options = {"build_exe": build_exe_options},
      executables = executables,
      requires=['numpy', 'matplotlib']
     )
```

---

# Basic Usage #

## Problems ##

* cx_Freeze does not detect:
  - modules imported in functions or conditionally loaded modules
  - runtime linked dependencies (e.g. dlopen, ctypes)
  - data files, config files, images, ...

* Resolve with customizations options:
  - Specify missing modules in `include` or `package` options
  - List binaries in `include_files` option

* Compressing packages does not always work
  - cx_Freeze compresses only a minimal set of code by default

* Look at files in cx_Freeze package:
  - `cx_Freeze/hooks.py`
  - `samples/`

---

# How does it work? #

## C Bootstrapping ##

  1. Base executable is copied into package and renamed
  
  2. It sets up the basic environment
    ```C
    // initialize Python
    Py_NoSiteFlag = 1;
    Py_FrozenFlag = 1;
    Py_IgnoreEnvironmentFlag = 1;
    Py_SetPythonHome(wExecutableDirName);
    Py_SetProgramName(wExecutableName);
    Py_Initialize();
    PySys_SetArgv(argc, wargv);
    ```
  3. It executes the init script
    
    ```C
    module = PyImport_Import(name);
    ```

---

# How does it work? #

## Python Bootstrapping ##

4. The init script copied into the package and renamed

5. It loads the Executable script

   ```Python
      sys.frozen = True

      FILE_NAME = sys.executable
      DIR_NAME = os.path.dirname(sys.executable)

      m = __import__("__main__")
      importer = zipimport.zipimporter(os.path.dirname(os.__file__))
      name, ext = os.path.splitext(os.path.basename(os.path.normcase(FILE_NAME)))
      moduleName = "%s__main__" % name
      code = importer.get_code(moduleName)
      exec(code, m.__dict__)
   ```

---

# How does it work? #

## Loading Extension Modules from Zip Archive ##

```Python
def __bootstrap__():
    import imp, os, sys
    global __bootstrap__, __loader__
    __loader__ = None; del __bootstrap__, __loader__

    found = False
    for p in sys.path:
        if not os.path.isdir(p):
            continue
        f = os.path.join(p, "%s")
        if not os.path.exists(f):
            continue
        m = imp.load_dynamic(__name__, f)
        import sys
        sys.modules[__name__] = m
        found = True
        break
    if not found:
        del sys.modules[__name__]
        raise ImportError("No module named %%s" %% __name__)
```

---

# References #

[https://anthony-tuininga.github.io/cx_Freeze/](https://anthony-tuininga.github.io/cx_Freeze/)

---

class: center, middle

# ? #