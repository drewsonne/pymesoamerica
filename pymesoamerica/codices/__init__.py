import abc
import os
from multiprocessing import Pool
from os.path import abspath, expanduser, expandvars

from pkg_resources import iter_entry_points

from pymesoamerica.codices.image import Image


class Codex(object):
    PATTERN = '{i:02}'
    RANGE = range(0, 1)

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def images(self, target_directory=None):
        images = []
        for i in self.RANGE:
            img = {'href': self.PATTERN.format(i=i)}
            if target_directory is not None:
                img['path'] = self.abs_path(
                    os.path.join(
                        target_directory,
                        self.name,
                        os.path.basename(img['href'])
                    )
                )
            images.append(img)
        return images

    @staticmethod
    def abs_path(path):
        return abspath(expandvars(expanduser(path)))

    def download_images(self, target_directory, number_of_threads=2):
        p = Pool(number_of_threads)

        def img(i):
            Image(self, **i).download()

        map(lambda i: print(i), self.images(target_directory))


class AlignmentCodex(Codex):
    PATTERN = '{i:02d}{a}'

    def images(self, urls=list()):
        for page_num in self.RANGE:
            for alignment in ['r', 'v']:
                urls.append({'href': self.PATTERN.format(i=page_num, a=alignment)})
        return urls


class Borbonicus(Codex):
    PATTERN = 'http://www.famsi.org/research/loubat/Borbonicus/images/Borbonicus_{i:02d}.jpg'
    RANGE = range(3, 39)


class Borgia(Codex):
    PATTERN = 'http://www.famsi.org/research/loubat/Borgia/page_{i:02d}.jpg'
    RANGE = range(0, 78)


class Cospi(Codex):
    PATTERN = 'http://www.famsi.org/research/loubat/Cospi/page_{i:02d}.jpg'
    RANGE = range(0, 40)


class FejevaryMayer(Codex):
    PATTERN = 'http://www.famsi.org/research/loubat/Fejervary/page_{i:02d}.jpg'
    RANGE = range(0, 45)


class Magliabecchiano(AlignmentCodex):
    PATTERN = 'http://www.famsi.org/research/loubat/Magliabecchiano/page_{i:02d}{a}.jpg'
    RANGE = range(0, 93)

    def images(self, urls=list()):
        return super().images(urls + [{'href': self.PATTERN.format(i=0, a='0')}])


class TellerianoRemensis(AlignmentCodex):
    PATTERN = 'http://www.famsi.org/research/loubat/Telleriano-Remensis/page_{i:02d}{a}.jpg'
    RANGE = range(1, 51)


class TonalamatlAubin(Codex):
    PATTERN = 'http://www.famsi.org/research/loubat/Tonalamatl/page_{i:02d}.jpg'
    RANGE = range(0, 22)


class Vaticanus3738A(AlignmentCodex):
    PATTERN = 'http://www.famsi.org/research/loubat/Vaticanus%203738/page_{i:02d}{a}.jpg'
    RANGE = range(1, 99)

    def images(self, urls=list()):
        urls = super().images(urls + [
            {'href': 'http://www.famsi.org/research/loubat/Vaticanus%203738/page_001.jpg'},
            {'href': 'http://www.famsi.org/research/loubat/Vaticanus%203738/page_002.jpg'}
        ])
        urls.append({'href': 'http://www.famsi.org/research/loubat/Vaticanus%203738/page_248.jpg'})
        return urls


class Vaticanus3773B(Codex):
    PATTERN = 'http://www.famsi.org/research/loubat/Vaticanus%203773/page_{i:02d}.jpg'
    RANGE = range(0, 98)


class Catalogue(object):

    def __iter__(self):
        for codex in self._entry_points():
            yield (codex, codex.load()(codex.name))

    def _entry_points(self):
        return iter_entry_points(group='pymesoamerica', name=None)

    def get(self, codex_name):
        for codex in self._entry_points():
            if codex.name == codex_name:
                return codex.load()()
