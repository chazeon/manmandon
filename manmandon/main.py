from .engine import MMDEngine

from pathlib import Path
import click


def resolve_uri(uri):


    queue = []

    if Path(uri).exists():
        with open(uri) as fp:
            lines = fp.readlines()
        for line in lines:
            queue.append(line.strip())
    else:
        queue.append(uri)
    
    MMDEngine(queue).process()


@click.command()
@click.option("--list-providers", is_flag=True)
@click.argument("uri", required=False)
def main(uri: str, **kwargs):

    if kwargs.pop("list_providers"):
        print(MMDEngine([]).load_providers())

    if uri: resolve_uri(uri)

if __name__ == "__main__":
    main()