import re
import toml
import pkg_resources

from urllib.parse import urlparse, unquote
from pathlib import Path
from typing import List, Optional

from seleniumwire import webdriver

from .provider import MMDProvider, MMDChapterProvider, MMDChapterListProvider, MMDProviderType


class MMDEngine:


    def __init__(self, config_filename: str = None):
        self.driver: webdriver.Chrome = None
        self.queue: list = []
        self.config: dict = self.load_config(config_filename) 
    
    def __del__(self):
        self.unload_driver()
    
    @staticmethod
    def load_config(fname: str = None) -> dict:

        default_fname = pkg_resources.resource_filename(__name__, "../default.toml")
        config = toml.load(default_fname)

        if fname:
            config.update(toml.load(fname))

        return config
    
    def load_driver(self):
        if self.driver is None:
            config = self.config
            webdriver_path = config["webdriver"]["path"]
            self.driver = webdriver.Chrome(executable_path=webdriver_path)
    
    def unload_driver(self):
        if self.driver != None:
            self.driver.quit()
            self.driver = None
    
    def load_providers(self) -> List[MMDProvider]:
        import importlib, sys

        config = self.config
        sys.path.append(config["provider"]["path"])
        providers = []
        for name in config["provider"]["providers"]:
            for Provider in importlib.import_module(name).providers:
                provider = Provider(self.config, self.driver)
                providers.append(provider)
        return providers
    
    def resolve(self, uri: str):
        providers = self.load_providers()
        for provider in providers:
            if provider.match(uri):
                if provider.provider_type == MMDProviderType.CHAPTER_LIST_PROVIDER:
                    self.queue.extend(provider.resolve(uri))
                else:
                    provider.resolve(uri)


    def process(self, queue: list = None):

        if queue:
            self.queue.extend(queue)

        self.load_driver()

        i = 0
        while True:
            self.resolve(self.queue[i])
            i += 1
            if i == len(self.queue):
                break
        
        print(self.queue)
        