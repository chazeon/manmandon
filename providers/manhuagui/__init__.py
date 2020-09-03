from manmandon.provider import MMDChapterListProvider, MMDChapterProvider
from pathlib import Path
import json
import click
from manmandon.util import parse_url_fname

class ManhuaguiChapters(MMDChapterListProvider):

    patterns = [
        r"^https://(www\.)?manhuagui\.com/comic/\d+/?$"
    ]

    def resolve(self, uri):
        self.driver.get(uri)
        res = self.execute(Path(__file__).parent / "chapters.js")
        return json.loads(res)


class ManhuaguiChapter(MMDChapterProvider):

    patterns = [
        r"^https://(www\.)?manhuagui\.com/comic/\d+/\d+\.html$"
    ]

    scope = []

    def flip(self):
        from selenium.webdriver.common.keys import Keys
        self.driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_RIGHT)

    def resolve(self, uri):

        import copy

        del self.driver.requests
        self.driver.scopes = [
            '.*hamreus.com',
        ]

        self.driver.get(uri)
        self.sleep(3)
        num_pages = self.execute(Path(__file__).parent / "num_pages.js")

        directory = self.output_directory / self.driver.title
        directory.mkdir(exist_ok=True)
        if len(list(directory.glob("*"))) >= num_pages: return

        img_urls = []
        with click.progressbar(length=num_pages, label=self.driver.title, show_pos=True) as bar:
            bar.update(1)
            for i in range(num_pages - 1):
                img_url = self.execute(Path(__file__).parent / "image_url.js")
                img_urls.append(img_url)
                self.driver.wait_for_request("hamreus.com")
                self.sleep(3)
                bar.update(1)
                self.flip()

        for req in self.driver.requests:
            if req.url not in img_urls: continue
            img_url = req.url
            fname = directory / parse_url_fname(img_url)
            if not fname.exists():
                with open(fname, "wb") as fp:
                    fp.write(req.response.body)
        

        del self.driver.requests
        del self.driver.scopes

providers = [
    ManhuaguiChapters,
    ManhuaguiChapter
]
