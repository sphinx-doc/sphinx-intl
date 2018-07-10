# Type annotations for pycompat.py

from typing import Text, Mapping


FS_ENCODING: Text


def convert_with_2to3(filepath: Text) -> Text: ...


def execfile_(filepath: Text,
              _globals:Mapping
              ) -> None: ...

def relpath(path: Text,
            start: Text) -> Text: ...
