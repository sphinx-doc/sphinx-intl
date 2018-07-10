# Type annotations for sphinx_util.py

from typing import Text, Mapping, List, Callable, Dict, Optional, Iterable


class Tags(object):
    tags: Dict[Text, bool] = ...
    __contains__: Callable[[Text], bool]

    def __init__(self,
                 tags: Optional[List[Text]] = ...
                 ) -> None: ...

    def __iter__(self) -> Iterable[Mapping[Text, bool]]: ...

    def has(self,
            tag:Text
            ) -> bool: ...

    def add(self,
            tag:Text
            ) -> None: ...

    def remove(self,
            tag:Text
            ) -> None: ...
