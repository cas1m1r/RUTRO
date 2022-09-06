import winreg


class Registry:
    def __init__(self):
        self.user = winreg.HKEY_CURRENT_USER
        self.root = winreg.HKEY_CLASSES_ROOT
        self.comp = winreg.HKEY_LOCAL_MACHINE
        self.acct = {'root': self.root, 'user': self.user, 'comp': self.comp}
        self.common_paths = {'root': [r"SOFTWARE"],
                             'user': [r"SOFTWARE"],
                             'comp': [r"SOFTWARE"]}

        self.keynames = {'user': {}, 'comp': {}, 'root': {}}
        for user in self.common_paths.keys():
            for location in self.common_paths[user]:
                vals_found = enumerate_registry(self.acct[user], location)
                self.keynames[user][location] = vals_found[location]


def enumerate_registry(registry, key_path):
    access = winreg.ConnectRegistry(None, registry)
    reg_key = winreg.OpenKey(access, key_path)
    entries = list_keys(reg_key, key_path)
    return entries


def list_keys(registry, location: str):
    entries = {location: []}
    depth = 0
    haskeys = True
    while haskeys:
        try:
            entries[location].append(winreg.EnumKey(registry, depth))
            depth += 1
        except OSError:
            haskeys = False
            pass
    return entries

