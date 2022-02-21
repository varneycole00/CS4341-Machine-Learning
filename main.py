import sys
import psutil, os
from datetime import datetime
from ancillary.map_generation import map_generator
from Pal import PaFinder, heuristic

sys.setrecursionlimit(5000)
process = psutil.Process(os.getpid())

def determine_heuristic(input):
    if input.lower() == '5':
        return heuristic.better_than_sum
    elif input.lower() == '6':
        return heuristic.bet_x_three
    elif input.lower() == '7':
        return heuristic.test
    elif input.lower() == '8':
        return heuristic.test2
    return heuristic.ZERO


def main():
    if len(sys.argv) > 2:
        file_path = sys.argv[1]
        file = open(file_path)
        map = map_generator.file_to_map(file)

    else:
        map = map_generator.generate_random_map(rows=500, cols=500)
        map_generator.map_to_file(map)

    print('path to solution: test1')
    initial_mem = process.memory_info().rss
    start = datetime.now()

    finder = PaFinder(map.map, heuristic = determine_heuristic("7"))
    finder.iterator()
    print('map size: ' + str(len(map.map)) + ' x ' + str(len(map.map)))
    print('memory used: ' + str((process.memory_info().rss- initial_mem)/((1024)**2)) + ' mb')
    print('time elapsed: ' + str(datetime.now()-start))


    print('\npath to solution: test2')
    initial_mem = process.memory_info().rss
    start = datetime.now()

    finder = PaFinder(map.map, heuristic = determine_heuristic("8"))
    finder.iterator()
    print('map size: ' + str(len(map.map)) + ' x ' + str(len(map.map)))
    print('memory used: ' + str((process.memory_info().rss- initial_mem)/((1024)**2)) + ' mb')
    print('time elapsed: ' + str(datetime.now()-start))

    print('\npath to solution: for Heuristc 5 (Custom Heruistic)')
    initial_mem = process.memory_info().rss
    start = datetime.now()

    finder = PaFinder(map.map, heuristic = determine_heuristic("5"))
    finder.iterator()
    print('map size: ' + str(len(map.map)) + ' x ' + str(len(map.map)))
    print('memory used: ' + str((process.memory_info().rss- initial_mem)/((1024)**2)) + ' mb')
    print('time elapsed: ' + str(datetime.now()-start))

    print('\npath to solution: for Heuristc 5 (Custom Heruistic * 3)')
    initial_mem = process.memory_info().rss
    start = datetime.now()

    finder = PaFinder(map.map, heuristic = determine_heuristic("6"))
    finder.iterator()
    print('map size: ' + str(len(map.map)) + ' x ' + str(len(map.map)))
    print('memory used: ' + str((process.memory_info().rss- initial_mem)/((1024)**2)) + ' mb')
    print('time elapsed: ' + str(datetime.now()-start))


if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     main()
