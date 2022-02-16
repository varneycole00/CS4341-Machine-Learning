import sys
import psutil, os
from datetime import datetime
from map_generation import map_generator,Map
from Pal import PaFinder, heuristic
sys.setrecursionlimit(5000)
process = psutil.Process(os.getpid())


def determine_heuristic(input):
    if input.lower() == '1':
        return heuristic.ZERO
    elif input.lower() == '2':
        return heuristic.MIN
    elif input.lower() == '3':
        return heuristic.MAX
    elif input.lower() == '4':
        return heuristic.SUM
    elif input.lower() == '5':
        return heuristic.better_than_sum
    elif input.lower() == '6':
        return heuristic.bet_x_three
    return heuristic.ZERO


def main():
    if len(sys.argv) > 2:
        file_path = sys.argv[1]
        print('heuristic: ' + str(sys.argv[2]))
        file = open(file_path)
        map = map_generator.file_to_map(file)
        heur = determine_heuristic(sys.argv[2])

    else:
        map = map_generator.generate_random_map(rows=200, cols=200)
        map_generator.map_to_file(map)
        heur = heuristic.ZERO

    print('path to solution:')
    initial_mem = process.memory_info().rss
    start = datetime.now()

    finder = PaFinder(map.map, heuristic=heur)
    finder.iterator()

    print('map size: ' + str(len(map.map)) + ' x ' + str(len(map.map)))
    print('memory used: ' + str((process.memory_info().rss- initial_mem)/((1024)**2)) + ' mb')
    print('time elapsed: ' + str(datetime.now()-start))


if __name__ == "__main__":
    main()
