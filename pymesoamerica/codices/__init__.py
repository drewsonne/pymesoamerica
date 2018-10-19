import abc
import errno
import json
import os
import queue
import threading
from urllib.request import urlretrieve

from pkg_resources import iter_entry_points


class Codex(object):
    PATTERN = '{i:02}'
    RANGE = range(0, 1)

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def images(self):
        return list(map(lambda i: {'href': self.PATTERN.format(i=i)}, self.RANGE))

    def download_images(self, target_directory, number_of_threads=2):

        q = queue.Queue()
        threads = []

        def worker():
            while True:
                item = q.get()
                if item is None:
                    break
                self.download_image(*item)
                q.task_done()

        for i in range(number_of_threads):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        for image in self.images():
            q.put((image, target_directory))

        q.join()

        for i in range(number_of_threads):
            q.put(None)
        for t in threads:
            t.join()

    def download_image(self, image, target_directory):
        destination_dir = os.path.join(
            target_directory,
            self.name)

        try:
            os.makedirs(destination_dir)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(destination_dir):
                pass

        destination = os.path.join(
            destination_dir,
            os.path.basename(image['href'])
        )
        urlretrieve(image['href'], destination)
        print(json.dumps(dict(
            action='downloading',
            codex=self.name,
            source=image['href'],
            destination=destination,
        )))


class AlignmentCodex(Codex):
    PATTERN = '{i:02d}{a}'

    def images(self, urls=[]):
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

    def images(self):
        return super().images([{'href': self.PATTERN.format(i=0, a='0')}])


class TellerianoRemensis(AlignmentCodex):
    PATTERN = 'http://www.famsi.org/research/loubat/Telleriano-Remensis/page_{i:02d}{a}.jpg'
    RANGE = range(1, 51)


class TonalamatlAubin(Codex):
    PATTERN = 'http://www.famsi.org/research/loubat/Tonalamatl/page_{i:02d}.jpg'
    RANGE = range(0, 22)


class Vaticanus3738A(AlignmentCodex):
    PATTERN = 'http://www.famsi.org/research/loubat/Vaticanus%203738/page_{i:02d}{a}.jpg'
    RANGE = range(1, 99)

    def images(self):
        urls = super().images([
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
