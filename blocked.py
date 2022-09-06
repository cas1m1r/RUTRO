import os


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
                alias = ''.join(bad_program.split(' '))
                blocked.append(bad_program)
                blocked.append(alias)
        return list(set(blocked))

    def add_program(self, new_program):
        if new_program not in self.blacklist:
            self.blacklist.append(new_program)
            return True
        else:
            print(f'[!] {new_program} is already blocked')
            return False

    def remove_program(self, program):
        if program not in self.blacklist:
            print(f'[!] Cannot unblock {program} because it is not on blacklist')
            return False
        else:
            self.blacklist.remove(program)
            return True
