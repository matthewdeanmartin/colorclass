Changelog
=========

This project adheres to `Semantic Versioning <http://semver.org/>`_.

2.2.1 - 2021-12-08
------------------

Added
    * Publishin wheels

2.2.0 - 2016-05-14
------------------

Added
    * ``disable_if_no_tty()`` function to conditionally disable colors when STDERR and STDOUT are not streams.

Changed
    * Colors enabled by default always, like it was before v2.0.0.

2.1.1 - 2016-05-10
------------------

Fixed
    * Printing box drawing characters on Windows from Python 2.6.

2.1.0 - 2016-05-07
------------------

Added
    * ``keep_tags`` boolean keyword argument to Color(). Prevents colorclass from parsing curly brackets.
    * Automatically skip replacing stderr/stdout streams on latest Windows 10 versions with native ANSI color support.

Changed
    * Refactored most of windows.py.
    * Background color determined from either stderr or stdout, instead of just one stream (e.g. piping stderr to file).

Fixed
    * https://github.com/Robpol86/colorclass/issues/16
    * https://github.com/Robpol86/colorclass/issues/18

2.0.0 - 2016-04-10
------------------

Added
    * Python 3.5 support.
    * ``enable_all_colors()``, ``is_enabled()``, and ``is_light()`` toggle functions.
    * Library can be used as a script (e.g. ``echo "{red}Red{/red}" |python -m colorclass``).
    * Ability to add/multiply Color instances just like str.
    * Ability to iterate a Color instance and have each character keep its color codes.

Changed
    * Converted library from Python module to a package.
    * ``set_light_background()`` and ``set_dark_background()`` no longer enable colors. Use ``enable_all_colors()``.
    * Colors are disabled by default when STDERR and STDOUT are not streams (piped to files/null). Similar to ``grep``.
    * Reduce size of ANSI escape sequences by removing codes that have no effect. e.g. ``\033[31;35m`` to ``\033[35m``.
    * Color methods that return strings now return Color instances instead of str instances.

Fixed
    * https://github.com/Robpol86/colorclass/issues/15
    * https://github.com/Robpol86/colorclass/issues/17

1.2.0 - 2015-03-19
------------------

Added
    * Convenience single-color methods by `Marc Abramowitz <https://github.com/msabramo>`_.

1.1.2 - 2015-01-07
------------------

Fixed
    * Maintaining ``Color`` type through ``.encode()`` and ``.decode()`` chains.

1.1.1 - 2014-11-03
------------------

Fixed
    * Python 2.7 64-bit original colors bug on Windows.
    * resetting colors when ``reset_atexit`` is True.
    * Improved sorting of ``list_tags()``.

1.1.0 - 2014-11-01
------------------

Added
    * Native Windows support and automatic background colors.

1.0.2 - 2014-10-20
------------------

Added
    * Ability to disable/strip out all colors.

1.0.1 - 2014-09-11
------------------

Fixed
    * ``splitlines()`` method.

1.0.0 - 2014-09-01
------------------

* Initial release.
