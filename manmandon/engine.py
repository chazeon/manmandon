from seleniumwire import webdriver
import json
from urllib.parse import urlparse, unquote
from pathlib import Path
import re
from .provider import MMDProvider, MMDChapterProvider, MMDChapterListProvider, MMDProviderType
from typing import List

import toml

class MMDEngine:
    def __init__(self, queue):
        self.config = self.load_config() 
        self.driver = self.load_driver(self.config)
        self.queue = queue
    
    def __del__(self):
        self.unload_driver(self.driver)
    
    @staticmethod
    def load_config(fname: str = None):
        config = toml.load("default.toml")
        if fname:
            config.update(toml.load(fname))
        return config
    
    @staticmethod
    def load_driver(config):
        webdriver_path = config["webdriver"]["path"]
        return webdriver.Chrome(executable_path=webdriver_path)
    
    @staticmethod
    def unload_driver(driver):
        return driver.quit()
    
    def load_providers(self) -> List[MMDProvider]:
        import importlib, sys

        config = self.config
        sys.path.append(config["directories"]["providers"])
        providers = []
        for name in config["providers"]:
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


    def process(self):

        i = 0
        while True:
            self.resolve(self.queue[i])
            i += 1
            if i == len(self.queue):
                break
        
        print(self.queue)
        