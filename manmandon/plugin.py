from abc import ABC
from typing import List, Tuple, TYPE_CHECKING
import re
if TYPE_CHECKING:
    from .engine import MMDEngine


class MMDPluginBase(ABC):
    # '''
    # Attributes:
    #     patterns: in google format. see... <>
    # '''

    patterns: List[str] = []

    def __init__(self, engine: 'MMDEngine') -> None:
        self.engine = engine

    # @classmethod
    # def match(cls, url: str) -> bool:
    #     for pattern in cls.patterns:
    #         if urlmatch(pattern, url):
    #             return True
    #     return False

    @classmethod
    def match(cls, url: str):
        for pattern in cls.patterns:
            if re.search(pattern, url): return True
        return False

    def get_chapters(self, url: str) -> List[Tuple[str, str]]:
        return []

    def get_assets(self, url: str, title: str = None) -> List[Tuple[str, bytearray]]:
        return []
