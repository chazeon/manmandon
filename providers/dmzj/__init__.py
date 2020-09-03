from manmandon.provider import MMDChapterListProvider, MMDChapterProvider
from pathlib import Path
import json
from urllib.parse import urljoin
from manmandon.util import parse_url_fname
import click

class DMZJChapters(MMDChapterListProvider):

    patterns = [
        r"^https://(www\.)?dmzj\.com/info/[a-z]+/?$"
    ]

    def resolve(self, uri):
        self.driver.get(uri)
        res = self.execute(Path(__file__).parent / "chapters.js")
        return json.loads(res)

class DMZJChapters2(MMDChapterListProvider):

    patterns = [
        r"^https://manhua\.dmzj\.com/[a-z]+/?$"
    ]

    def resolve(self, uri):
        self.driver.get(uri)
        res = self.execute(Path(__file__).parent / "chapters2.js")
        return json.loads(res)

class DMZJChapter(MMDChapterProvider):

    patterns = [
        r"^https://manhua\.dmzj\.com/[a-z]+/\d+\.shtml/?$"
    ]

    scope = []

    def flip(self):
        from selenium.webdriver.common.keys import Keys
        self.driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_RIGHT)

    def resolve(self, uri):

        self.driver.get(uri)
        res = self.execute(Path(__file__).parent / "images.js")
        img_urls = json.loads(res)
        directory = self.output_directory / self.driver.title
        directory.mkdir(exist_ok=True)

        with click.progressbar(length=len(img_urls), label=self.driver.title, show_pos=True) as bar:
            bar.update(0)
            for i, img_url in enumerate(img_urls):
                img_url = urljoin("https://images.dmzj.com/", img_url)
                fname = directory / parse_url_fname(img_url)
                if not fname.exists():
                    req = self.driver.wait_for_request(img_url, timeout=60)
                    with open(fname, "wb") as fp:
                        fp.write(req.response.body)
                    self.sleep(3)
                bar.update(1)
                self.flip()

        del self.driver.requests

providers = [
    DMZJChapters,
    DMZJChapters2,
    DMZJChapter
]
