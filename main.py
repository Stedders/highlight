"""Command line interface to compile/run the static site"""
# Tutorial
# https://blog.naveeraashraf.com/posts/make-static-site-generator-with-python-2/
import os

import click
from click_default_group import DefaultGroup

from app.helpers import tailwind_os
from app.load import get_global
from app.server import run
from app.write import generate_site


@click.group(cls=DefaultGroup, default='compile', default_if_no_args=True)
@click.pass_context
def cli(ctx):
    """Command line grouping, handling common functions."""
    if not os.path.exists('site'):
        os.mkdir('site')
    ctx.obj = {'site': get_global()}


@cli.command()
@click.option('--compile-site/--no-compile-site', default=True)
@click.option('--tailwind-compile/--no-tailwind-compile', default=True)
@click.pass_context
def compile(ctx, compile_site, tailwind_compile):
    """Compiles site [default]"""
    site = get_global(compile_site=compile_site, local=True)
    generate_site(site)
    os.system(tailwind_os(compile=tailwind_compile))


@cli.command()
@click.pass_context
def dev(ctx):
    site = ctx.obj['site']
    generate_site(site, False)


@cli.command()
@click.pass_context
def server(ctx):
    """Runs a local web server to host the site"""
    os.system(tailwind_os(False))
    run()


@cli.command()
@click.pass_context
def watch(ctx):
    """Watches the src and rebuilds the site as changes are made"""
    exec(open("./app/watch.py").read())


if __name__ == "__main__":
    cli()
