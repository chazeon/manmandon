from playwright.sync_api import sync_playwright, Playwright, BrowserContext
from typing import ContextManager
from logging import getLogger
from pprint import pformat
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .plugin import MMDPluginBase


logger = getLogger(__file__)


class MMDEngine(ContextManager):

    p: Playwright
    'The playwright context.'

    browser: BrowserContext
    'The running browser.'


    def __init__(self, config: str) -> None:
        '''
        :param config: Path of the configuration file.
        '''

        from .plugin import MMDPluginBase

        self.config = self.load_config(config)
        logger.debug(pformat(config, compact=True))

        for plugin_file in self.config["plugin"]["files"]:
            self.load_plugin_file(plugin_file)
        self.plugins = MMDPluginBase.__subclasses__()

        logger.debug("Loaded plugins: %s." % pformat(self.plugins, compact=True))

        self.playwright = sync_playwright()

    def __enter__(self) -> 'MMDEngine':
        self.p = self.playwright.__enter__()
        self.browser = self.p.chromium.launch(
            **self.config["engine"]["browser"]
        )
        # if (not self.config["engine"]["browser"]["headless"]
        #     not self.config["engine"]["browser"].get("user_dir", None)):
        #     self.browser.wait_for_event("backgroundpage")
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        self.browser.close()
        self.playwright.__exit__()

    @staticmethod
    def load_config(custom_file: str) -> dict:
        '''Load the custom config TOML and deepmerge with the default one.

        :param custom_file: path to the custom TOML file.
        :return: Merged configuration object as a ``dict``.
        '''
        import toml
        from importlib import resources
        from deepmerge import always_merger
        default_file = "default.toml"
        default_config = toml.load(
            resources.open_text('manmandon', default_file))
        custom_config = toml.load(custom_file)
        config = always_merger.merge(default_config, custom_config)
        return config

    @staticmethod
    def load_plugin_file(path: str):
        '''Load and execute a Python script that contains the code for a plugin.
        
        :param path: Path to the Python script.
        '''
        from importlib.util import spec_from_file_location, module_from_spec
        name = Path(path).stem
        spec = spec_from_file_location(name, path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        logger.debug("Plugin from %s loaded as %s." % (path, pformat(module)))
        return module

    def match_plugin(self, url: str) -> Optional['MMDPluginBase']:
        '''Find a matching plugin that handles the URL.

        :param url: URL of the page.
        :return: A matching plugin or ``None`` if there is no match.
        '''
        for PluginClass in self.plugins:
            if PluginClass.match(url):
                return PluginClass(self)
        return None
