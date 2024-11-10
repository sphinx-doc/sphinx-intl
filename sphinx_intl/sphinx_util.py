from collections.abc import Iterator


# port from https://github.com/sphinx-doc/sphinx/blob/ad41e0b/sphinx/util/tags.py
class Tags:
    def __init__(self, tags: list[str] = None) -> None:
        self.tags = dict.fromkeys(tags or [], True)

    def has(self, tag: str) -> bool:
        return tag in self.tags

    __contains__ = has

    def __iter__(self) -> Iterator[str]:
        return iter(self.tags)

    def add(self, tag: str) -> None:
        self.tags[tag] = True

    def remove(self, tag: str) -> None:
        self.tags.pop(tag, None)
