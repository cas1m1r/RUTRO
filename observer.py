from registry import Registry
from blocked import Blacklist
import ctypes
import time


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


def main():
    watcher = Observer()


if __name__ == '__main__':
    main()
