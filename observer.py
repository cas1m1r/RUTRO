import winreg
import ctypes
import time
import os 

# class for holding names of programs to block (maybe could have things added, etc..) 
class Blacklist:
    def __init__(self):
        self.blacklist = self.load_black_list()

    def load_black_list(self):
        blocked = []
        if not os.path.isfile('blacklist.txt'):
            print(f'[!] Missing blacklist.txt')
            exit()
        for bad_program in open('blacklist.txt', 'r').read().split('\n'):
            if len(bad_program):
                alias = ''.join(bad_program.split(' ')) # Team Viewer removes the space
                alias2 = f'.{bad_program.lower()}'      # anydesk appears as .anydesk
                blocked.append(bad_program)
                blocked.append(alias)
                # TODO: only alert once per alias! 
        return list(set(blocked))

## class for enumerating windows registry
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


## main class for watching system for changes
class Observer:
    def __init__(self):
        # We are WATCHING you
        self.monitoring = True
        self.alerted = False
        # Check initial registry entries
        self.registry = Registry()
        # Load list of blocked applications
        self.blocked = Blacklist().blacklist
        # TODO: Check if any programs from the blacklist are already installed!
        self.bad_applications = self.check_for_blocked_programs()
        # TODO: Continuously check registry to see if any blocked programs were added
        try:
            self.monitor()
        except KeyboardInterrupt:
            print(f'[KILLING OBSERVER]')
            self.monitoring = False
            pass

    def check_for_blocked_programs(self):
        badones = []
        # update registery entries
        self.registry = Registry()
        for location in self.registry.keynames['user']:
            for application in self.registry.keynames['user'][location]:
                if application in self.blocked:
                    self.alert(application)     # this can be modified to throw a popup, send email, etc.
                    badones.append(application)
        return badones

    def monitor(self, timeout=30):
        if len(self.blocked):
            print(f'*** WARNING*** Already Have following blocked applications installed:')
            for app in self.blocked:
                if app in self.bad_applications:
                    print(f'\t-{app}')
        while self.monitoring:
            self.registry = Registry() # update list in case new things are installed/removed
            for badapp in self.check_for_blocked_programs():
                self.bad_applications.append(badapp)
                time.sleep(timeout)

    def alert(self, application):
        msg = u"[X] BLOCKED APPLICATION " +application+u" IS INSTALLED"
        title = u"*** Scam Alert! ***"
        ctypes.windll.user32.MessageBoxW(None, msg, title, 0)
        self.alerted = True

## utility methods 
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


def main():
    watcher = Observer()


if __name__ == '__main__':
    main()
