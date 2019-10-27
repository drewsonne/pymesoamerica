from pymesoamerica.codices import Codex


class Dresden(Codex):
    PATTERN = 'https://digital.slub-dresden.de/data/kitodo/codedrm_280742827/codedrm_280742827_tif/jpegs/{i:08d}.tif.large.jpg'
    RANGE = range(1, 78)
