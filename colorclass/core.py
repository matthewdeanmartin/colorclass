"""String subclass that handles ANSI color codes."""

from typing import Callable, Generator, Iterable, Optional, Union, List

from colorclass.codes import ANSICodeMapping
from colorclass.parse import RE_SPLIT, parse_input
from colorclass.search import build_color_index, find_char_color


def apply_text(incoming: str, func: Callable[[str], str]) -> str:
    """Call `func` on text portions of incoming color string.

    :param iter incoming: Incoming string/ColorStr/string-like object to iterate.
    :param func: Function to call with string portion as first and only parameter.

    :return: Modified string, same class type as incoming string.
    """
    split = RE_SPLIT.split(incoming)
    for i, item in enumerate(split):
        if not item or RE_SPLIT.match(item):
            continue
        split[i] = func(item)
    return incoming.__class__().join(split)


class ColorBytes(bytes):
    """Str (bytes in Python3) subclass, .decode() overridden to return unicode (str in Python3) subclass instance."""

    def __new__(cls, *args, **kwargs) -> "ColorBytes":
        """Save original class so decode() returns an instance of it."""
        original_class = kwargs.pop("original_class")
        combined_args = [cls] + list(args)
        instance = bytes.__new__(*combined_args, **kwargs)
        instance.original_class = original_class
        return instance

    def decode(self, encoding="utf-8", errors="strict"):
        """Decode using the codec registered for encoding. Default encoding is 'utf-8'.

        errors may be given to set a different error handling scheme. Default is 'strict' meaning that encoding errors
        raise a UnicodeDecodeError. Other possible values are 'ignore' and 'replace' as well as any other name
        registered with codecs.register_error that is able to handle UnicodeDecodeErrors.

        :param str encoding: Codec.
        :param str errors: Error handling scheme.
        """
        original_class = getattr(self, "original_class")
        return original_class(super(ColorBytes, self).decode(encoding, errors))


class ColorStr(str):
    """Core color class."""

    def __new__(cls, *args, **kwargs) -> None:
        """Parse color markup and instantiate."""
        keep_tags = kwargs.pop("keep_tags", False)

        # Parse string.
        value_markup = args[0] if args else str()  # e.g. '{red}test{/red}'
        value_colors, value_no_colors = parse_input(
            value_markup, ANSICodeMapping.DISABLE_COLORS, keep_tags
        )
        color_index = build_color_index(value_colors)

        # Instantiate.
        color_args = [cls, value_colors] + list(args[1:])
        instance = str.__new__(*color_args, **kwargs)

        # Add additional attributes and return.
        instance.value_colors = value_colors
        instance.value_no_colors = value_no_colors
        instance.has_colors = value_colors != value_no_colors
        instance.color_index = color_index
        return instance

    def __add__(self, other) -> Optional[Union["ColorStr", str]]:
        """Concatenate."""
        return self.__class__(self.value_colors + other, keep_tags=True)

    def __getitem__(self, item: int) -> Optional[Union["ColorStr", str]]:
        """Retrieve character."""
        try:
            color_pos = self.color_index[int(item)]
        except TypeError:  # slice
            return super(ColorStr, self).__getitem__(item)
        return self.__class__(
            find_char_color(self.value_colors, color_pos), keep_tags=True
        )

    def __iter__(self) -> Generator["ColorStr", None, None]:
        """Yield one color-coded character at a time."""
        for color_pos in self.color_index:
            yield self.__class__(find_char_color(self.value_colors, color_pos))

    def __len__(self) -> int:
        """Length of string without color codes (what users expect)."""
        return self.value_no_colors.__len__()

    def __mod__(
            self, other: Optional[Union["ColorStr", str]]
    ) -> Optional[Union["ColorStr", str]]:
        """String substitution (like printf)."""
        return self.__class__(self.value_colors % other, keep_tags=True)

    def __mul__(
            self, other: Optional[Union["ColorStr", str]]
    ) -> Optional[Union["ColorStr", str]]:
        """Multiply string."""
        return self.__class__(self.value_colors * other, keep_tags=True)

    def __repr__(self) -> str:
        """Representation of a class instance (like datetime.datetime.now())."""
        return "{name}({value})".format(
            name=self.__class__.__name__, value=repr(self.value_colors)
        )

    def capitalize(self) -> str:
        """Return a copy of the string with only its first character capitalized."""
        return apply_text(self, lambda s: s.capitalize())

    def center(
            self, width: int, fillchar: Optional[str] = None
    ) -> Optional[Union["ColorStr", str]]:
        """Return centered in a string of length width. Padding is done using the specified fill character or space.

        :param int width: Length of output string.
        :param str fillchar: Use this character instead of spaces.
        """
        if fillchar is not None:
            result = self.value_no_colors.center(width, fillchar)
        else:
            result = self.value_no_colors.center(width)
        return self.__class__(
            result.replace(self.value_no_colors, self.value_colors), keep_tags=True
        )

    def count(self, sub: str, start: int = 0, end: int = -1) -> int:
        """Return the number of non-overlapping occurrences of substring sub in string[start:end].

        Optional arguments start and end are interpreted as in slice notation.

        :param str sub: Substring to search.
        :param int start: Beginning position.
        :param int end: Stop comparison at this position.
        """
        return self.value_no_colors.count(sub, start, end)

    def endswith(self, suffix: str, start: int = 0, end: Optional[int] = None) -> bool:
        """Return True if ends with the specified suffix, False otherwise.

        With optional start, test beginning at that position. With optional end, stop comparing at that position.
        suffix can also be a tuple of strings to try.

        :param str suffix: Suffix to search.
        :param int start: Beginning position.
        :param int end: Stop comparison at this position.
        """
        args = [suffix, start] + ([] if end is None else [end])
        return self.value_no_colors.endswith(*args)

    def encode(
            self, encoding: Optional[str] = None, errors: str = "strict"
    ) -> ColorBytes:
        """Encode using the codec registered for encoding. encoding defaults to the default encoding.

        errors may be given to set a different error handling scheme. Default is 'strict' meaning that encoding errors
        raise a UnicodeEncodeError. Other possible values are 'ignore', 'replace' and 'xmlcharrefreplace' as well as any
        other name registered with codecs.register_error that is able to handle UnicodeEncodeErrors.

        :param str encoding: Codec.
        :param str errors: Error handling scheme.
        """
        return ColorBytes(
            super(ColorStr, self).encode(encoding, errors),
            original_class=self.__class__,
        )

    def decode(
            self, encoding: Optional[str] = None, errors: str = "strict"
    ) -> Optional[Union["ColorStr", str]]:
        """Decode using the codec registered for encoding. encoding defaults to the default encoding.

        errors may be given to set a different error handling scheme. Default is 'strict' meaning that encoding errors
        raise a UnicodeDecodeError. Other possible values are 'ignore' and 'replace' as well as any other name
        registered with codecs.register_error that is able to handle UnicodeDecodeErrors.

        :param str encoding: Codec.
        :param str errors: Error handling scheme.
        """
        return self.__class__(
            super(ColorStr, self).decode(encoding, errors), keep_tags=True
        )

    def find(
            self, sub: str, start: Optional[int] = None, end: Optional[int] = None
    ) -> int:
        """Return the lowest index where substring sub is found, such that sub is contained within string[start:end].

        Optional arguments start and end are interpreted as in slice notation.

        :param str sub: Substring to search.
        :param int start: Beginning position.
        :param int end: Stop comparison at this position.
        """
        return self.value_no_colors.find(sub, start, end)

    def format(self, *args, **kwargs) -> Optional[Union["ColorStr", str]]:
        """Return a formatted version, using substitutions from args and kwargs.

        The substitutions are identified by braces ('{' and '}').
        """
        return self.__class__(
            super(ColorStr, self).format(*args, **kwargs), keep_tags=True
        )

    def index(
            self, sub: str, start: Optional[int] = None, end: Optional[int] = None
    ) -> int:
        """Like S.find() but raise ValueError when the substring is not found.

        :param str sub: Substring to search.
        :param int start: Beginning position.
        :param int end: Stop comparison at this position.
        """
        return self.value_no_colors.index(sub, start, end)

    def isalnum(self) -> bool:
        """Return True if all characters in string are alphanumeric and there is at least one character in it."""
        return self.value_no_colors.isalnum()

    def isalpha(self) -> bool:
        """Return True if all characters in string are alphabetic and there is at least one character in it."""
        return self.value_no_colors.isalpha()

    def isdecimal(self) -> bool:
        """Return True if there are only decimal characters in string, False otherwise."""
        return self.value_no_colors.isdecimal()

    def isdigit(self) -> bool:
        """Return True if all characters in string are digits and there is at least one character in it."""
        return self.value_no_colors.isdigit()

    def isnumeric(self) -> bool:
        """Return True if there are only numeric characters in string, False otherwise."""
        return self.value_no_colors.isnumeric()

    def isspace(self) -> bool:
        """Return True if all characters in string are whitespace and there is at least one character in it."""
        return self.value_no_colors.isspace()

    def istitle(self) -> bool:
        """Return True if string is a titlecased string and there is at least one character in it.

        That is uppercase characters may only follow uncased characters and lowercase characters only cased ones. Return
        False otherwise.
        """
        return self.value_no_colors.istitle()

    def isupper(self) -> bool:
        """Return True if all cased characters are uppercase and there is at least one cased character in it."""
        return self.value_no_colors.isupper()

    def join(self, iterable: Iterable) -> Optional[Union["ColorStr", str]]:
        """Return a string which is the concatenation of the strings in the iterable.

        :param iterable: Join items in this iterable.
        """
        return self.__class__(super(ColorStr, self).join(iterable), keep_tags=True)

    def ljust(
            self, width: int, fillchar: Optional[str] = None
    ) -> Optional[Union["ColorStr", str]]:
        """Return left-justified string of length width. Padding is done using the specified fill character or space.

        :param int width: Length of output string.
        :param str fillchar: Use this character instead of spaces.
        """
        if fillchar is not None:
            result = self.value_no_colors.ljust(width, fillchar)
        else:
            result = self.value_no_colors.ljust(width)
        return self.__class__(
            result.replace(self.value_no_colors, self.value_colors), keep_tags=True
        )

    def rfind(
            self, sub: str, start: Optional[int] = None, end: Optional[int] = None
    ) -> int:
        """Return the highest index where substring sub is found, such that sub is contained within string[start:end].

        Optional arguments start and end are interpreted as in slice notation.

        :param str sub: Substring to search.
        :param int start: Beginning position.
        :param int end: Stop comparison at this position.
        """
        return self.value_no_colors.rfind(sub, start, end)

    def rindex(
            self, sub: str, start: Optional[int] = None, end: Optional[int] = None
    ) -> int:
        """Like .rfind() but raise ValueError when the substring is not found.

        :param str sub: Substring to search.
        :param int start: Beginning position.
        :param int end: Stop comparison at this position.
        """
        return self.value_no_colors.rindex(sub, start, end)

    def rjust(
            self, width: int, fillchar: Optional[str] = None
    ) -> Optional[Union["ColorStr", str]]:
        """Return right-justified string of length width. Padding is done using the specified fill character or space.

        :param int width: Length of output string.
        :param str fillchar: Use this character instead of spaces.
        """
        if fillchar is not None:
            result = self.value_no_colors.rjust(width, fillchar)
        else:
            result = self.value_no_colors.rjust(width)
        return self.__class__(
            result.replace(self.value_no_colors, self.value_colors), keep_tags=True
        )

    def splitlines(
            self, keepends: bool = False
    ) -> List[Optional[Union["ColorStr", str]]]:
        """Return a list of the lines in the string, breaking at line boundaries.

        Line breaks are not included in the resulting list unless keepends is given and True.

        :param bool keepends: Include linebreaks.
        """
        return [self.__class__(line) for line in self.value_colors.splitlines(keepends)]

    def startswith(self, prefix: str, start: int = 0, end: int = -1) -> bool:
        """Return True if string starts with the specified prefix, False otherwise.

        With optional start, test beginning at that position. With optional end, stop comparing at that position. prefix
        can also be a tuple of strings to try.

        :param str prefix: Prefix to search.
        :param int start: Beginning position.
        :param int end: Stop comparison at this position.
        """
        return self.value_no_colors.startswith(prefix, start, end)

    def swapcase(self) -> str:
        """Return a copy of the string with uppercase characters converted to lowercase and vice versa."""
        return apply_text(self, lambda s: s.swapcase())

    def title(self) -> str:
        """Return a titlecased version of the string.

        That is words start with uppercase characters, all remaining cased characters have lowercase.
        """
        return apply_text(self, lambda s: s.title())

    def translate(self, table) -> str:
        """Return a copy of the string, where all characters have been mapped through the given translation table.

        Table must be a mapping of Unicode ordinals to Unicode ordinals, strings, or None. Unmapped characters are left
        untouched. Characters mapped to None are deleted.

        :param table: Translation table.
        """
        return apply_text(self, lambda s: s.translate(table))

    def upper(self) -> str:
        """Return a copy of the string converted to uppercase."""
        return apply_text(self, lambda s: s.upper())

    def zfill(self, width: int) -> Optional[Union["ColorStr", str]]:
        """Pad a numeric string with zeros on the left, to fill a field of the specified width.

        The string is never truncated.

        :param int width: Length of output string.
        """
        if not self.value_no_colors:
            result = self.value_no_colors.zfill(width)
        else:
            result = self.value_colors.replace(
                self.value_no_colors, self.value_no_colors.zfill(width)
            )
        return self.__class__(result, keep_tags=True)


if __name__ == '__main__':
    print(str.__new__(str, "abc"))
