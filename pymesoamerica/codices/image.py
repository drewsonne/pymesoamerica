import errno
import json
import os
from urllib.request import urlretrieve


class Image(object):
    def __init__(self, codex, href, path):
        self._codex = codex
        self._href = href
        self._path = path

    def download(self):
        destination_dir = os.path.dirname(self._path)
        try:
            os.makedirs(destination_dir)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(destination_dir):
                pass

        urlretrieve(self._href, self._path)
        status = dict(
            action='downloading',
            codex=self._codex.name,
            source=self._href,
            destination=self._path,
        )
        # print(json.dumps(status))
        return status
