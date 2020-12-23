import re
import time
from enum import Enum, auto
from typing import List
from string import Template
from pathlib import Path
from urllib.parse import urlparse, unquote
from functools import lru_cache
from selenium.webdriver import Chrome

class MMDProviderType(Enum):
    CHAPTER_PROVIDER = auto()
    CHAPTER_LIST_PROVIDER = auto()

class MMDProvider:
    provider_type: MMDProviderType
    patterns: List[str]

    def __init__(self, config: dict, driver: Chrome):
        self.config = config
        self.driver = driver

    @classmethod
    def match(cls, uri):
        for pattern in cls.patterns:
            if re.search(pattern, uri): return True
        return False
    
    def resolve(self, uri):
        raise NotImplementedError()

    def go(self, uri):
        self.driver.go(uri)
    
    def back(self):
        self.driver.back()
    
    @staticmethod
    def get_url_fname(url: str):
        return unquote(Path(urlparse(url).path).name)
    
    def execute(self, fname, substr: dict = None):
        with open(fname) as fp:
            script = fp.read()
        if substr:
            script = Template(script).substitute(substr)
        return self.driver.execute_async_script(script)

    def sleep(self, secs: float):
        return time.sleep(secs)
    
class MMDChapterListProvider(MMDProvider):
    provider_type = MMDProviderType.CHAPTER_LIST_PROVIDER

class MMDChapterProvider(MMDProvider):
    provider_type = MMDProviderType.CHAPTER_PROVIDER

    @property
    @lru_cache
    def output_directory(self) -> Path:
        directory = Path(self.config["output"]["directory"])
        if not directory.exists():
            directory.mkdir()
        return directory