from abc import ABC
from typing import List, Tuple, ClassVar, TYPE_CHECKING
import re
if TYPE_CHECKING:
    from .engine import MMDEngine


class MMDPluginBase(ABC):
    '''An abstract base class for implementing plugins.
    All plugins are discovered as subclasses of this class.
    '''

    patterns: ClassVar[List[str]] = []
    'List of regular expressions to be used to match URLs.'

    engine: 'MMDEngine'
    'A running engine context.'

    def __init__(self, engine: 'MMDEngine') -> None:
        self.engine = engine

    # @classmethod
    # def match(cls, url: str) -> bool:
    #     for pattern in cls.patterns:
    #         if urlmatch(pattern, url):
    #             return True
    #     return False

    @classmethod
    def match(cls, url: str) -> bool:
        '''Determine if the page ``url`` match any of the regular expression
        ``patterns`` of this class.

        :param url: The url of the page to be matched.
        '''
        for pattern in cls.patterns:
            if re.search(pattern, url):
                return True
        return False

    def get_chapters(self, url: str) -> List[Tuple[str, str]]:
        '''
        :param url: URL for the "parent" page.
        :return: A list of URLs to be visited next.
        '''
        return []

    def get_assets(self, url: str, title: str = None) -> List[Tuple[str, bytearray]]:
        '''
        :param url: URL for the page that contains media.
        :return: A list of file name/path and `bytearray` pairs.
        '''
        return []
