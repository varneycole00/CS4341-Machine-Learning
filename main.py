import csv
import sys
import psutil, os
from datetime import datetime

from tqdm import tqdm

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


def main(board_number, file):
    file = open(file, "r")
    map = map_generator.file_to_map(file)

    start = datetime.now()
    finderOurHeuristic = PaFinder(map.map, heuristic = determine_heuristic("8"))
    ourHeuristicResult = finderOurHeuristic.iterator()
    endTime =  datetime.now()
    ourHeuristic = ourHeuristicResult[0]
    timeElapsedOurHeuristic = (endTime-start).total_seconds()


    start = datetime.now()
    finderHeuristic5 = PaFinder(map.map, heuristic = determine_heuristic("5"))
    heuristic5Result = finderHeuristic5.iterator()
    heuristic5 = heuristic5Result[0]
    timeElapsedHeuristic5 = (datetime.now()-start).total_seconds()

    start = datetime.now()
    finderHeuristic6 = PaFinder(map.map, heuristic = determine_heuristic("6"))
    heuristic6Result = finderHeuristic6.iterator()
    heuristic6 = heuristic6Result[0]
    timeElapsedHeuristic6 = (datetime.now()-start).total_seconds()


    file_exists = os.path.isfile('experiment.csv')
    with open('experiment.csv', 'a', newline='') as csvFile :
        writer = csv.writer(csvFile)
        if not file_exists :
            writer.writerow(['Board Number', 'Heuristic', 'Number Of Nodes Expanded', 'Cost', 'Branching Factor', 'Time'])
        writer.writerow([board_number, "7", ourHeuristicResult[2], 100-ourHeuristic.cumulative_cost, ourHeuristicResult[1], timeElapsedOurHeuristic])
        writer.writerow([board_number, "5", heuristic5Result[2], 100-heuristic5.cumulative_cost, heuristic5Result[1], timeElapsedHeuristic5])
        writer.writerow([board_number, "6", heuristic6Result[2], 100-heuristic6.cumulative_cost, heuristic6Result[1], timeElapsedHeuristic6])

if __name__ == "__main__":
    for board_number in tqdm(range(10)) :
        file = str("./testBoards/board" + str(board_number) + ".txt")
        main(board_number + 1, file)
