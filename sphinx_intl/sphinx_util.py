# -*- coding: utf-8 -*-


# port from https://github.com/sphinx-doc/sphinx/blob/ad41e0b/sphinx/util/tags.py
class Tags(object):
    def __init__(self, tags=None):
        self.tags = dict.fromkeys(tags or [], True)

    def has(self, tag):
        return tag in self.tags

    __contains__ = has

    def __iter__(self):
        return iter(self.tags)

    def add(self, tag):
        self.tags[tag] = True

    def remove(self, tag):
        self.tags.pop(tag, None)
