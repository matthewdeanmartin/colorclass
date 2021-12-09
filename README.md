#colorclass

Yet another ANSI color text library for Python. Provides "auto colors" for dark/light terminals. Works on Linux, OS X,
and Windows. For Windows support you just need to call ``Windows.enable()`` in your application.

On Linux/OS X ``autocolors`` are toggled by calling ``set_light_background()`` and ``set_dark_background()``. On Windows
this can be done automatically if you call ``Windows.enable(auto_colors=True)``. Even though the latest Windows 10 does
support ANSI color codes natively, you still need to run Windows.enable() to take advantage of automatically detecting
the console's background color.

In Python2.x this library subclasses ``unicode``, while on Python3.x it subclasses ``str``.

* Python 2.6, 2.7, PyPy, PyPy3, 3.3, 3.4, and 3.5 supported on Linux and OS X.
* Python 2.6, 2.7, 3.3, 3.4, and 3.5 supported on Windows (both 32 and 64 bit versions of Python).

.. image:: https://img.shields.io/coveralls/Robpol86/colorclass/master.svg?style=flat-square&label=Coveralls
    :target: https://coveralls.io/github/Robpol86/colorclass
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/colorclass.svg?style=flat-square&label=Latest
    :target: https://pypi.python.org/pypi/colorclass
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/colorclass.svg?style=flat-square&label=PyPI%20Downloads
    :target: https://pypi.python.org/pypi/colorclass
    :alt: Downloads

## Quickstart
Install:
```bash
    pip install colorclass
```

## Piped Command Line
It is possible to pipe curly-bracket tagged (or regular ANSI coded) text to Python in the command line to produce color
text. Some examples:

```bash
    echo "{red}Red{/red}" |python -m colorclass  # Red colored text.
    echo -e "\033[31mRed\033[0m" | COLOR_DISABLE=true python -m colorclass  # Strip colors
    echo -e "\033[31mRed\033[0m" | COLOR_ENABLE=true python -m colorclass &> file.txt  # Force colors.
```
Export these environment variables as "true" to enable/disable some features:

    =============== ============================================
    Env Variable    Description
    =============== ============================================
    COLOR_ENABLE    Force colors even when piping to a file.
    COLOR_DISABLE   Strip all colors from incoming text.
    COLOR_LIGHT     Use light colored text for dark backgrounds.
    COLOR_DARK      Use dark colored text for light backgrounds.
    =============== ============================================

# Example Implementation
======================

![Example Script Screenshot](https://github.com/Robpol86/colorclass/raw/master/example.png?raw=true)

![Example Windows Screenshot](https://github.com/Robpol86/colorclass/raw/master/example_windows.png?raw=true)

Source code for the example code is: [example.py](https://github.com/Robpol86/colorclass/blob/master/example.py)

## Usage

Different colors are chosen using curly-bracket tags, such as ``{red}{/red}``. For a list of available colors, call
``colorclass.list_tags()``.

The available "auto colors" tags are:

* autoblack
* autored
* autogreen
* autoyellow
* autoblue
* automagenta
* autocyan
* autowhite
* autobgblack
* autobgred
* autobggreen
* autobgyellow
* autobgblue
* autobgmagenta
* autobgcyan
* autobgwhite

Methods of Class instances try to return sane data, such as:

```python
    from colorclass import Color
    color_string = Color('{red}Test{/red}')

    >>> color_string
    u'\x1b[31mTest\x1b[39m'

    >>> len(color_string)
    4

    >>> color_string.istitle()
    True
```
There are also a couple of helper attributes for all Color instances:

```python
    >>> color_string.value_colors
    '\x1b[31mTest\x1b[39m'

    >>> color_string.value_no_colors
    'Test'
```

[Change Log](https://github.com/matthewdeanmartin/colorclass/blob/master/CHANGELOG.md)