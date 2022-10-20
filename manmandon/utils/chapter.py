from typing import Tuple, List, TypeVar, Iterable
from click import prompt
from logging import getLogger
from pprint import pformat

logger = getLogger(__file__)

T = TypeVar('T')


def range_expand(txt: str) -> List[int]:
    '''Range expansion

    >>> range_expand('1-3,6,8,10-12')
    [1, 2, 3, 6, 8, 10, 11, 12]

    via: https://rosettacode.org/wiki/Range_expansion
    '''
    lst: List[int] = []
    for r in txt.split(','):
        if '-' in r[1:]:
            r0, r1 = r[1:].split('-', 1)
            lst += range(int(r[0] + r0), int(r1) + 1)
        else:
            lst.append(int(r))
    return lst


def display_chapters(chapters: Iterable[Tuple[str, str]]) -> None:
    for i, (title, url) in enumerate(chapters):
        print(f"{i+1:>4d} {title:<10} {url}")


def select_chapters(chapters: Iterable[T]) -> List[T]:
    selection = prompt("Please enter the chapter you want")
    selection = range_expand(selection)
    logger.debug("Your selected chapters are %s" % pformat(selection))
    selected = []
    for i, chapter in enumerate(chapters):
        if i+1 in selection:
            selected.append(chapter)
    return selected