import click



def resolve_uri(uri):

    from pathlib import Path
    from .engine import MMDEngine

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
@click.argument("uri")
def main(uri: str):
    resolve_uri(uri)

if __name__ == "__main__":
    main()