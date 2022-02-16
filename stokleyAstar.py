import heapq
import math
import time
from collections import deque
from enum import Enum
import sys

class heuristic(Enum):
    ZERO = 'zero'
    MIN = 'min'
    MAX = 'max'
    SUM = 'sum'
    better_than_sum = 'bet'
    bet_x_three = 'bx3'


class East:
    def __init__(self):
        self.filled = False
        self.cumulative_cost = 0
        self.heuristic = 0
        self.parent_coordinates = (0, 0)
        self.parent_orientation = ''
        self.cumulative_action = 0
        self.depth = 0


class West:
    def __init__(self):
        self.filled = False
        self.cumulative_cost = 0
        self.heuristic = 0
        self.parent_coordinates = (0,  0)
        self.parent_orientation = ''
        self.cumulative_action = 0
        self.depth = 0


class North:
    def __init__(self):
        self.filled = False
        self.cumulative_cost = 0
        self.heuristic = 0
        self.parent_coordinates = (0, 0)
        self.parent_orientation = ''
        self.cumulative_action = 0
        self.depth = 0


class South:
    def __init__(self):
        self.filled = False
        self.cumulative_cost = 0
        self.heuristic = 0
        self.parent_coordinates = (0, 0)
        self.parent_orientation = ''
        self.cumulative_action = 0
        self.depth = 0


class MapCell:
    def __init__(self):
        self.east = East
        self.west = West
        self.north = North
        self.south = South


class PaFinder:

    def __init__(self, map, heuristic = heuristic.ZERO):
        self.map = map
        self.heuristic = heuristic
        self.goal = [0, 0]
        # PriorityQueue will store a set of coordinates and a direction
        self.frontier = []
        self.exploring = []
        self.counter = 0
        self.total = 0
        self.current = [0, 0]
        self.goal_reached = False
        self.goal_node = []
        self.start = []


        heapq.heapify(self.frontier)

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == "S":
                    heapq.heappush(self.frontier, (0, [x, y], "north"))
                    self.exploring = [x, y]
                    self.current = [x, y]
                    self.start = [x, y]
                elif self.map[y][x] == "G":
                    self.goal = [x, y]

        self.marked_map = self.map_map()
        self.visited = self.visited_function()

    def visited_function(self):
        new_visited = []
        for y in range(len(self.map)):
            temp_row = []
            for x in range(len(self.map[y])):
                new_cell = False
                temp_row.append(new_cell)
            new_visited.append(temp_row)
        return new_visited

    def map_map(self):
        new_map = []
        for y in range(len(self.map)):
            temp_row = []
            for x in range(len(self.map[y])):
                new_cell = MapCell()
                new_cell.north = North()
                new_cell.south = South()
                new_cell.east = East()
                new_cell.west = West()
                temp_row.append(new_cell)
            new_map.append(temp_row)
        origin = new_map[self.start[1]][self.start[0]]
        origin.north.parent_coordinates = ['x', 'y']
        origin.south.parent_coordinates = ['x', 'y']
        origin.east.parent_coordinates = ['x', 'y']
        origin.west.parent_coordinates = ['x', 'y']

        return new_map

    def get_turn_cost(self):
        turn_cost = self.map[self.current[1]][self.current[0]]
        if turn_cost == 'S':
            turn_cost = 1
        turn_cost = math.ceil((turn_cost/2))
        if turn_cost == 'G':
            turn_cost = 0
        return turn_cost

    def forward_cost(self):
        forward_cost = self.map[self.exploring[1]][self.exploring[0]]
        if forward_cost == 'S' or forward_cost == 'G':
            forward_cost = 1
        return int(forward_cost)

    def heuristic_calculator(self, current_x, current_y):
        goal_x = self.goal[0]
        goal_y = self.goal[1]
        hor_dist = abs(goal_x-current_x)
        vert_dist = abs(goal_y - current_y)

        better_than_sum = hor_dist + vert_dist
        if (hor_dist > 0):
            better_than_sum += 1
        if (vert_dist > 0):
            better_than_sum += 1

        if self.heuristic == heuristic.ZERO:
            return 0
        elif self.heuristic == heuristic.MIN:
            return min(hor_dist, vert_dist)
        elif self.heuristic == heuristic.MAX:
            return max(hor_dist, vert_dist)
        elif self.heuristic == heuristic.SUM:
            return hor_dist + vert_dist
        elif self.heuristic == heuristic.better_than_sum:
            return better_than_sum
        elif self.heuristic == heuristic.bet_x_three:
            return better_than_sum * 3

    def dictionary_holder(self, action_needed, creation):
        if action_needed == "TURNING" and creation is True:
            return {
                "None": 0,
                "Left": self.get_turn_cost(),
                "Right": self.get_turn_cost(),
                "Reverse": (2 * self.get_turn_cost()),
            }
        if action_needed == "TURNING" and not creation:
            return {
                "None": 0,
                "Left": self.get_turn_cost(),
                "Right": self.get_turn_cost(),
            }
        if action_needed == "MOVE":
            return {
                "Forward": self.forward_cost(),
                "Bash": (self.forward_cost() + 3),
            }

    def dictionary_holder_empty(self, action_needed, creation):
        if action_needed == "TURNING" and creation is True:
            return {
                "None": 0,
                "Left": 0,
                "Right": 0,
                "Reverse": 0,
            }
        if action_needed == "TURNING" and not creation:
            return {
                "None": 0,
                "Left": 0,
                "Right": 0,
            }
        if action_needed == "MOVE":
            return {
                "Forward": 0,
                "Bash": 0,
            }

    def orientation_finder(self, turn, orientation):
        if turn.count("Right"):
            if orientation.count("south"):
                return "west"
            if orientation.count("north"):
                return "east"
            if orientation.count("west"):
                return "north"
            if orientation.count("east"):
                return "south"
        if turn.count("Left"):
            if orientation.count("south"):
                return "east"
            if orientation.count("north"):
                return "west"
            if orientation.count("west"):
                return "south"
            if orientation.count("east"):
                return "north"
        if turn.count("None"):
            return orientation
        if turn.count("Reverse"):
            if orientation.count("south"):
                return "north"
            if orientation.count("north"):
                return "south"
            if orientation.count("west"):
                return "east"
            if orientation.count("east"):
                return "west"

    def turn_decoder(self, parent, child):
        if child.count("west"):
            if parent.count("south"):
                return "Right"
            if parent.count("north"):
                return "Left"
            if parent.count("west"):
                return "None"
            if parent.count("east"):
                return "Reverse"
        if child.count("east"):
            if parent.count("south"):
                return "Left"
            if parent.count("north"):
                return "Right"
            if parent.count("west"):
                return "Reverse"
            if parent.count("east"):
                return "None"
        if child.count("south"):
            if parent.count("south"):
                return "None"
            if parent.count("north"):
                return "Reverse"
            if parent.count("west"):
                return "Left"
            if parent.count("east"):
                return "Right"
        if child.count("north"):
            if parent.count("south"):
                return "Reverse"
            if parent.count("north"):
                return "None"
            if parent.count("west"):
                return "Right"
            if parent.count("east"):
                return "Left"

    def result(self, position, turn, move, orientation):
        x, y = position
        new_orientation = []
        holder = []
        turn = turn
        orientation = orientation
        new_orientation = self.orientation_finder(turn, orientation)
        if new_orientation == "north":
            if move.count("Forward"):
                y -= 1
            if move.count("Bash"):
                y -= 2
        if new_orientation == "south":
            if move.count("Forward"):
                y += 1
            if move.count("Bash"):
                y += 2
        if new_orientation == "east":
            if move.count("Forward"):
                x += 1
            if move.count("Bash"):
                x += 2
        if new_orientation == "west":
            if move.count("Forward"):
                x -= 1
            if move.count("Bash"):
                x -= 2
        new_position = (x, y)
        holder = [new_position, new_orientation]
        return holder

    def expand_frontier(self, heuristic, coordinates, orientation):
        cumulative_cost = (getattr(self.marked_map[coordinates[1]][coordinates[0]], orientation)).cumulative_cost
        cumulative_action = (getattr(self.marked_map[coordinates[1]][coordinates[0]], orientation)).cumulative_action
        depth = (getattr(self.marked_map[coordinates[1]][coordinates[0]], orientation)).depth
        if self.counter == 0:
            first = True
        else:
            first = False
        self.counter += 1

        for turn in self.dictionary_holder_empty("TURNING", first).keys():
            for move in self.dictionary_holder_empty("MOVE", first).keys():
                result_holder = []
                new_orientation = []
                final_cost = 0
                self.exploring = []
                result_holder = self.result(coordinates, turn, move, orientation)
                newx, newy = result_holder[0]
                new_orientation = result_holder[1]

                if newy in range(len(self.map)) and newx in range(len(self.map[newy])) and not self.visited[newy][newx]:
                    self.total += 1
                    self.exploring = [newx, newy]
                    temp_cost = self.dictionary_holder("TURNING", first)[turn] \
                        + self.dictionary_holder("MOVE", first)[move]
                    heuristic_temp_cost = temp_cost + self.heuristic_calculator(newx, newy)

                    heuristic_final_cost = heuristic_temp_cost + cumulative_cost
                    final_cost = temp_cost + cumulative_cost

                    new_cell = getattr(self.marked_map[newy][newx], new_orientation)
                    if not new_cell.filled or new_cell.heuristic > heuristic_final_cost:
                        heapq.heappush(self.frontier, (heuristic_final_cost, [newx, newy], new_orientation))
                        new_cell.cumulative_cost = final_cost
                        new_cell.heuristic = heuristic_final_cost
                        new_cell.filled = True
                        new_cell.parent_coordinates = coordinates
                        new_cell.parent_orientation = orientation
                        new_cell.depth = depth + 1
                        self.visited[coordinates[1]][coordinates[0]] = True
                        if turn == "None":
                            new_cell.cumulative_action = cumulative_action + 1
                        else:
                            new_cell.cumulative_action = cumulative_action + 2


    def get_move(self, child_coordinates, parent_x, parent_y):
        if (abs(child_coordinates[0] - parent_x) > 1) or \
                (abs(child_coordinates[1] - parent_y) > 1):
            return 'Bash'
        else:
            return 'forward'


    def back_tracking(self, child_coordinates, orientation, back_tracking_list):
        if child_coordinates == self.start:
            while len(back_tracking_list) > 0:
                print(back_tracking_list.pop())
        else:
            child_node = getattr(self.marked_map[child_coordinates[1]][child_coordinates[0]], orientation)
            parent_y = child_node.parent_coordinates[1]
            parent_x = child_node.parent_coordinates[0]
            parent_node = getattr(self.marked_map[parent_y][parent_x], child_node.parent_orientation)
            move = self.get_move(child_coordinates, parent_x, parent_y)
            turn = self.turn_decoder(child_node.parent_orientation,orientation)
            if turn == "None":
                back_tracking_list.append(move)
            else:
                back_tracking_list.append(turn)
                back_tracking_list.append(move)
            self.back_tracking([parent_x, parent_y], child_node.parent_orientation, back_tracking_list)


    def iterator(self):
        while True:
            cheapest_node = heapq.heappop(self.frontier)
            cheapest_x = cheapest_node[1][0]
            cheapest_y = cheapest_node[1][1]
            if cheapest_node[1] == self.goal:
                back_tracking_list = deque()
                best_node = getattr(self.marked_map[cheapest_y][cheapest_x], cheapest_node[2])
                self.back_tracking(cheapest_node[1], cheapest_node[2], back_tracking_list)
                print('Path depth =', best_node.depth, ', Actions taken =', best_node.cumulative_action, ', Score =',
                      100-best_node.cumulative_cost, ', Nodes explored =', self.counter, ', Branching = ', round((self.total-1)/self.counter,2))
                break
            else:
                self.current = cheapest_node[1]
                self.expand_frontier(cheapest_node[0], cheapest_node[1], cheapest_node[2])
