import sys
import psutil, os
from datetime import datetime
from ancillary.map_generation import map_generator
from Pal import PaFinder
sys.setrecursionlimit(5000)
process = psutil.Process(os.getpid())

def main():
    if len(sys.argv) > 2:
        file_path = sys.argv[1]
        file = open(file_path)
        map = map_generator.file_to_map(file)

    else:
        map = map_generator.generate_random_map(rows=200, cols=200)
        map_generator.map_to_file(map)

    print('path to solution:')
    initial_mem = process.memory_info().rss
    start = datetime.now()

    finder = PaFinder(map.map)
    finder.iterator()

    print('map size: ' + str(len(map.map)) + ' x ' + str(len(map.map)))
    print('memory used: ' + str((process.memory_info().rss- initial_mem)/((1024)**2)) + ' mb')
    print('time elapsed: ' + str(datetime.now()-start))


if __name__ == "__main__":
    main()
