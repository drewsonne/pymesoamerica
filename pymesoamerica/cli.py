import json

import click

from pymesoamerica.analysis.layouts import AnalyseGrids
from pymesoamerica.codices import Catalogue


def writer(result):
    print(json.dumps(
        result,
        sort_keys=True,
        indent=4,
        separators=(',', ': '),
        ensure_ascii=False
    ))


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['catalogue'] = Catalogue()


@cli.command()
@click.pass_context
def codices(ctx):
    return writer([c.name for c, _ in ctx.obj['catalogue']])


@cli.command()
@click.pass_context
def images(ctx):
    return writer({c.name: ch.images() for c, ch in ctx.obj['catalogue']})


@cli.command()
@click.argument('codex')
@click.option('--prefix', '-P', help='Folder to download to.',
              default='./data/')
@click.option('--number-of-threads', '-t', help='Number of threads.', type=int, default=2)
@click.pass_context
def download(ctx, codex, prefix, number_of_threads):
    for codex_ep, codex_obj in ctx.obj['catalogue']:
        if (codex_ep.name == codex):
            codex_obj.download_images(prefix, number_of_threads)
            break


@cli.command('download-all')
@click.option('--prefix', '-P', help='Folder to download to.',
              default='./')
@click.option('--number-of-threads', '-t', help='Number of threads.', type=int, default=2)
@click.pass_context
def download_all(ctx, prefix, number_of_threads):
    for _, codex in ctx.obj['catalogue']:
        codex.download_images(prefix, number_of_threads)


@cli.command()
@click.option('--codex', '-c', help='Name of the codex to process')
@click.pass_context
def analyse(ctx, codex):
    return writer({
        'codex': codex,
        'grids': AnalyseGrids(codex).run()
    })


if __name__ == '__maine__':
    cli(obj={})
