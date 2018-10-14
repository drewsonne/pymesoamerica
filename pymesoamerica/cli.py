from pkg_resources import iter_entry_points


def codices():
    for codex in iter_entry_points(group='pymesoamerica', name=None):
        print(codex)
