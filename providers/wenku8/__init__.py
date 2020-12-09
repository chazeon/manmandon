from manmandon.provider import MMDChapterListProvider, MMDChapterProvider
from pathlib import Path
import json
from bs4 import BeautifulSoup

class ManhuaguiChapters(MMDChapterListProvider):

    patterns = [
        r"^https://(www\.)?wenku8\.net/novel/\d+/\d+/index.htm$"
    ]

    def resolve(self, uri):
        self.driver.get(uri)
        res = self.execute(Path(__file__).parent / "chapters.js")
        return json.loads(res)

class ManhuaguiChapter(MMDChapterProvider):

    patterns = [
        r"^https://(www\.)?wenku8\.net/novel/\d+/\d+/\d+.htm$"
    ]

    def resolve(self, uri):

        self.driver.scopes = [
            "picture.wenku8.com"
        ]

        self.driver.get(uri)

        self.sleep(3)

        res = self.execute(Path(__file__).parent / "content.js")
        res = json.loads(res)

        title = self.driver.title
        content = res["content"]

        directory = self.output_directory / title
        directory.mkdir()

        with open(directory / "index.html", "w") as fp:
            fp.write(content)

providers = [
    ManhuaguiChapters,
    ManhuaguiChapter
]
