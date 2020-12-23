import click
from pathlib import Path
from typing import List

from .engine import MMDEngine
from .provider import MMDProvider


def resolve_uri(engine, uri):


    queue = []

    if Path(uri).exists():
        with open(uri) as fp:
            lines = fp.readlines()
        for line in lines:
            queue.append(line.strip())
    else:
        queue.append(uri)
    
    engine.process(queue)


def print_providers(providers: List[MMDProvider]):

    # Title
    click.echo(click.style("Providers", bold=True))
    click.echo(click.style("=========", bold=True))

    for provider in providers:
        click.echo()
        click.echo("{}".format(provider.__class__))
        for pattern in provider.patterns:
            click.echo("r'{}'".format(pattern))

    click.echo()

@click.command()
@click.option("--list-providers", is_flag=True)
@click.option("-c", "--config", type=click.Path(exists=True, dir_okay=False))
@click.argument("uri", required=False)
def main(uri: str, **kwargs):

    engine = MMDEngine(kwargs.pop("config"))

    if kwargs.pop("list_providers"):
        providers = engine.load_providers()
        print_providers(providers)

    if uri:
        resolve_uri(engine, uri)

if __name__ == "__main__":
    main()