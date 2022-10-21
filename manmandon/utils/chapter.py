from typing import Tuple, List, TypeVar, Iterable
from logging import getLogger
from pprint import pformat

from click import prompt, echo
from tabulate import tabulate

logger = getLogger(__file__)

T = TypeVar('T')


def range_expand(txt: str) -> List[int]:
    '''Range expansion.

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
    '''Tabulate chapter name and URL.
    '''
    echo(tabulate(chapters, showindex=True, headers=["#", "Name", "URL"]))


def select_chapters(chapters: Iterable[T]) -> List[T]:
    '''Prompt user to select chapter, then filter out the selected entries.

    :param chapters: List of item to be filtered by user entered indices.

    :return: Filtered entries.
    '''
    selection = prompt("Please enter the chapter you want")
    selection = range_expand(selection)
    logger.debug("Your selected chapters are %s" % pformat(selection))
    selected = []
    for i, chapter in enumerate(chapters):
        if i+1 in selection:
            selected.append(chapter)
    return selected
