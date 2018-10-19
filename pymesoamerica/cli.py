import json
import sys

import cmdln

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


class App(cmdln.Cmdln):
    name = 'mesoamerica-codices'

    def __init__(self):
        super().__init__()
        self._catalogue = Catalogue()

    def do_names(self, subcmd, opts, *paths):
        """${cmd_name}: List all the codices

        ${cmd_usage}
        ${cmd_option_list}
        """
        return writer([c.name for c, _ in self._catalogue])

    def do_images(self, subcmd, opts, *paths):
        """${cmd_name}: List all the images in the codices

        ${cmd_usage}
        ${cmd_option_list}
        """
        return writer({c.name: ch.images() for c, ch in self._catalogue})

    @cmdln.option('-c', '--codex', help='Name of the codex to process', metavar='ARG')
    @cmdln.option('-P', '--prefix', help='Folder to download to', metavar='ARG')
    @cmdln.option('-t', '--number_of_threads', help='Number of threads', metavar='ARG')
    def do_download(self, subcmd, opts, *paths):
        """${cmd_name}: Download a codex

        ${cmd_usage}
        ${cmd_option_list}
        """
        threads = 2 if opts.number_of_threads is None else int(opts.number_of_threads)
        for codex_ep, codex in self._catalogue:
            if (codex_ep.name == opts.codex) or (opts.codex is None):
                codex.download_images(opts.prefix, threads)

    @cmdln.option('-c', '--codex', help='Name of the codex to process', metavar='ARG')
    def do_analyse(self, subcmd, opts, *paths):
        """${cmd_name}: Analyse the codices

        ${cmd_usage}
        ${cmd_option_list}
        """
        return writer({
            'codex': opts.codex,
            'grids': AnalyseGrids(opts.codex).run()
        })


def cli():
    app = App()
    sys.exit(app.main())
