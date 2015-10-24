# -*- coding: utf-8 -*-
"""Transliterate Unicode text into plain 7-bit ASCII.

Example usage:
>>> from unidecode import unidecode:
>>> unidecode(u"\u5317\u4EB0")
"Bei Jing "

The transliteration uses a straightforward map, and doesn't have alternatives
for the same character based on language, position, or anything else.

In Python 3, a standard string object will be returned. If you need bytes, use:
>>> unidecode("Κνωσός").encode("ascii")
b'Knosos'
"""
Cache_sections = {}
Cache_chars = {}


def unidecode(string):
    """Transliterate an Unicode object into an ASCII string

    >>> unidecode(u"\u5317\u4EB0")
    "Bei Jing "
    """

    retval = []

    for char in string:
        try:
            retval.append(Cache_chars[char])
        except KeyError:
            codepoint = ord(char)

            if codepoint < 0x80:  # Basic ASCII
                Cache_chars[char] = char
                retval.append(char)
                continue

            if codepoint > 0xeffff:
                continue  # Characters in Private Use Area and above are ignored

            section = codepoint >> 8   # Chop off the last two hex digits
            position = codepoint % 256  # Last two hex digits

            try:
                table = Cache_sections[section]
            except KeyError:
                try:
                    mod = __import__('unidecode.x%03x' % (section), [], [], ['data'])
                except ImportError:
                    Cache_sections[section] = None
                    continue   # No match: ignore this character and carry on.

                Cache_sections[section] = table = mod.data

            if table and len(table) > position:
                Cache_chars[char] = table[position]
                retval.append(table[position])

    return ''.join(retval)
