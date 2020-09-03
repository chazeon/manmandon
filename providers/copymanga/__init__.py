from manmandon.provider import MMDChapterListProvider, MMDChapterProvider
from pathlib import Path
import json
import click

class CopyMangaChapters(MMDChapterListProvider):

    patterns = [
        r"^https://(www.)?copymanga.com/comic/[a-z]+/?$"
    ]

    def resolve(self, uri):
        self.driver.get(uri)
        res = self.execute(Path(__file__).parent / "chapters.js")
        return json.loads(res)

class CopyMangaChapter(MMDChapterProvider):

    patterns = [
        r"^https://copymanga.com/comic/[a-z]+/chapter/"
    ]

    scope = []

    def resolve(self, uri):

        self.driver.get(uri)
        res = self.execute(Path(__file__).parent / "images.js")
        img_urls = json.loads(res)
        img_urls = [u for u in img_urls if u != None]
        directory = self.output_directory / self.driver.title
        directory.mkdir(exist_ok=True)

        with click.progressbar(length=len(img_urls), label=self.driver.title, show_pos=True) as bar:
            bar.update(0)
            for i, img_url in enumerate(img_urls):
                fname = directory / f"{i+1:03d}.webp"
                if not fname.exists():
                    self.driver.get(img_url)
                    req = self.driver.wait_for_request(img_url, timeout=60)
                    with open(fname, "wb") as fp:
                        fp.write(req.response.body)
                    self.sleep(3)
                bar.update(1)

        del self.driver.requests 

providers = [
    CopyMangaChapters,
    CopyMangaChapter
]
