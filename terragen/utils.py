import time
import datetime
from colored import fore, style

def log(string):
    string = string.replace('\n', '\n'.ljust(15, ' '))
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    print(('[' + fore.BLUE + '%s' + style.RESET + '] %s') %
          (current_time, string))

class Timer:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        print(('[' + fore.BLUE + '%s' + \
              style.RESET + '] %s ' + \
              style.BOLD + '%.03f'+style.RESET + \
              ' seconds') % (current_time, (self.name+':').ljust(80), self.interval))


def elevation_at_percent_surface(world, percent):
    return round(world['avg_height'] * (percent * 2 / 100))
