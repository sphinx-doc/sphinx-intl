# -*- coding: utf-8 -*-
if False:
    from typing import Iterator, List


# port from https://github.com/sphinx-doc/sphinx/blob/ad41e0b/sphinx/util/tags.py
class Tags(object):
    def __init__(self, tags=None):
        # type: (List[str]) -> None
        self.tags = dict.fromkeys(tags or [], True)

    def has(self, tag):
        # type: (str) -> bool
        return tag in self.tags

    __contains__ = has

    def __iter__(self):
        # type: () -> Iterator[str]
        return iter(self.tags)

    def add(self, tag):
        # type: (str) -> None
        self.tags[tag] = True

    def remove(self, tag):
        # type: (str) -> None
        self.tags.pop(tag, None)
