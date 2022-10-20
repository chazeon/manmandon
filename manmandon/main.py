from pathlib import Path
from pprint import pformat
import click
import logging
from logging import getLogger

logger = getLogger(__file__)


@click.command()
@click.argument("url")
@click.option("-c", "--config", default="config.toml", type=click.Path(exists=True))
@click.option("-v", "--verbosity", default="INFO")
def main(url: str, config: str, verbosity: str):

    logging.basicConfig(level=verbosity)

    from .engine import MMDEngine
    from collections import deque

    with MMDEngine(config) as e:

        queue = deque([("", url)])

        while queue:
            name, link = queue.popleft()
            plugin = e.match_plugin(link)
            logging.debug("Processing %s at %s." % (str(name), link))
            if not plugin:
                logger.error("Url %s cannot be resolved." % link)
                raise RuntimeError("Url %s cannot be resolved." % link)
            logging.debug("Matched plugin %s for %s." %
                          (pformat(plugin), link))

            chapters = plugin.get_chapters(link)
            if chapters:
                from .utils.chapter import select_chapters, display_chapters
                display_chapters(chapters)
                chapters = select_chapters(chapters)
                display_chapters(chapters)
                for _name, _link in chapters:
                    queue.append((_name, _link))

            outdir = Path(e.config["output"]["directory"])

            for _path, _payload in plugin.get_assets(link, title=name):
                file_path = outdir / _path
                from os import makedirs
                makedirs(file_path.parent, exist_ok=True)
                with open(outdir / _path, "wb") as fp:
                    fp.write(_payload)


if __name__ == "__main__":
    main()