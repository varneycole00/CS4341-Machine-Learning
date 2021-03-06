import csv
import heapq
import math
import os
import time

from featurecalculator import FeatureCalculator
from toolbox import Toolbox
from collections import deque
# import matplotlib.pyplot as plt
from enum import Enum
import copy
import sys

class heuristic(Enum):
    ZERO = 'zero'
    MIN = 'min'
    MAX = 'max'
    SUM = 'sum'
    better_than_sum = 'bet'
    bet_x_three = 'bx3'
    learned_heuristic = 'test'

class Direction :
    def __init__(self):
        self.filled = False
        self.cumulative_cost = 0
        # heuristic is the final heuristic value, the one that is used in the frontier
        self.heuristic5 = 0
        # heuristic_roc is the rate of change of the heuristic from the parent to the child
        # (child.heuristic - parent.heuristic)
        self.heuristic_roc = 0
        # cost_roc is the rate of change of the cumulative cost to get to that node from the parent to the child
        # (child.cost - parent.cost)
        self.cost_roc = 0
        # current_heuristic_estimate is the predicted cost from that point to the goal.
        self.estimated_CTG = 0
        # heuristic_estimate_roc is the rate of change of the predicted cost to the goal from that node, from
        # the parent to the child (child.current_heuristic_estimate - parent.current_heuristic_estimate)
        self.estimated_CTG_roc = 0
        # heuristic_estimate_avg is the running average of the change towards/away from the goal.
        self.estimated_CTG_roc_SUM = 0
        self.parent_coordinates = (0, 0)
        self.current_coordinate = (0, 0)
        self.parent_orientation = ''
        self.cumulative_action = 0
        self.depth = 0
        self.orientation = ''
        self.new_heuristic_final_cost = 0


class East(Direction):
    pass


class West(Direction):
    pass


class North(Direction):
    pass


class South(Direction):
    pass


class MapCell:
    def __init__(self):
        self.east = East
        self.west = West
        self.north = North
        self.south = South


class PaFinder:

    def __init__(self, map, heuristic = heuristic.better_than_sum):
        self.map = map
        self.heuristic = heuristic
        self.goal = [0, 0]
        self.frontier = []
        self.exploring = []
        self.counter = 0
        self.total = 0
        self.goal_reached = False
        self.goal_node = []
        self.goal_area =[]
        self.start = []

        heapq.heapify(self.frontier)

        # Initialization step for everything, looks through each row for the start and the goal.
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == "S":
                    # Once the start has been found, the starting node is added to the frontier.
                    heapq.heappush(self.frontier, (0, [x, y], "north"))
                    self.exploring = [x, y]
                    self.start = [x, y]
                elif self.map[y][x] == "G":
                    # setting spaces around the goal
                    self.goal_area.append([[x - 1, y + 1], [x, y + 1], [x + 1, y + 1]])
                    self.goal_area.append([[x - 1, y], [x, y], [x + 1, y]])
                    self.goal_area.append([[x - 1, y - 1], [x, y - 1], [x + 1, y - 1]])
                    # Setting the goal coordinates once it is found.
                    self.goal = [x, y]
        # Initializing the marked_map. The marked map is used to store the four nodes that are possible at each
        # coordinate position (i.e. facing, North, South, East, West). The values that are stored for each orientation
        # can be seen in the class definitions.
        self.marked_map = self.map_map()
        # Initializing the visited matrix, a binary matrix where all coordinates are initially set to False. This is
        # used to simplify calculations in the expand_frontier process. If a node has not been visited, then there
        # is no reason to run any calculations checking for best heuristic at that position.
        self.visited = self.visited_function()

    # Making the visited matrix.
    def visited_function(self):
        new_visited = []
        for y in range(len(self.map)):
            temp_row = []
            for x in range(len(self.map[y])):
                new_cell = False
                temp_row.append(new_cell)
            new_visited.append(temp_row)
        return new_visited

    # Making the marked_map ~ function is called map_map because I ran out of ideas.
    def map_map(self):
        new_map = []
        for y in range(len(self.map)):
            temp_row = []
            for x in range(len(self.map[y])):
                # Each coordinate position contains a MapCell.
                new_cell = MapCell()
                # Each MapCell contains the four coordinate positions.
                new_cell.north = North()
                new_cell.south = South()
                new_cell.east = East()
                new_cell.west = West()
                # Appending to the x-row of the y number.
                temp_row.append(new_cell)
            # Appending the x-row to the y-row.
            new_map.append(temp_row)
        # Setting origin location.
        origin = new_map[self.start[1]][self.start[0]]

        return new_map

    # Cost of turning on any given cell.
    def get_turn_cost(self, coordinates):
        # This is the cost of the cell itself.
        turn_cost = self.map[coordinates[1]][coordinates[0]]
        # If the cell is the start, then it costs 1 to turn.
        if turn_cost == 'S':
            turn_cost = 1
        # Actual calculation of turn cost (half cell cost rounder up).
        turn_cost = math.ceil((turn_cost/2))
        # If the cell is the goal, it costs nothing to turn, the only reason that this needs to be here is that due
        # to the nature of A*, it does not check to see if it is the goal until after all calculations, once it knows
        # it is the least expensive path, so the algorithm will attempt to calculate the turn cost on the goal.
        if turn_cost == 'G':
            turn_cost = 0
        return turn_cost

    # Cost of moving forward given a destination cell (i.e. the cost of the destination).
    def forward_cost(self, new_coordinates):
        forward_cost = self.map[new_coordinates[1]][new_coordinates[0]]
        # Cost of the goal is given as 1, and although the cost of moving into the start would be the value of the
        # start, there is never an instance in which a move into the start would be beneficial
        if forward_cost == 'S' or forward_cost == 'G':
            forward_cost = 1
        return int(forward_cost)

    # Heuristic calculator will only calculate the better_than_sum heuristic (per Assignment 3 guidelines)
    def get_classic_heuristic(self, current_x, current_y):
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
        else:
            return better_than_sum

    def heuristic_calculator(self, current_x, current_y, orientation, estm_avg):
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
        elif self.heuristic == heuristic.learned_heuristic: # the one with the cost
            return 1.1233 * better_than_sum + -1.0043 * FeatureCalculator.get_avg_move_toward_goal_wDir(orientation, True, current_x, current_y, self) \
                   + 1.4142 * FeatureCalculator.estimate_cost_with_knowledge(orientation, current_x, current_y, better_than_sum, self) - 6.6042


# return better_than_sum
    # Dictionary of the all possible turns and movements.
    def dictionary_holder(self, action_needed, creation, coordinates):
        # There is a different list for "creation" because at the start (i.e. when on the start node) it is possible to
        # move in reverse. This is the only time that a reverse move would make sense, so this is the only time the
        # algorithm is allowed to make a reverse move.
        if action_needed == "TURNING" and creation is True:
            return {
                "None": 0,
                "Left": self.get_turn_cost(coordinates),
                "Right": self.get_turn_cost(coordinates),
                "Reverse": (2 * self.get_turn_cost(coordinates)),
            }
        if action_needed == "TURNING" and not creation:
            return {
                "None": 0,
                "Left": self.get_turn_cost(coordinates),
                "Right": self.get_turn_cost(coordinates),
            }
        if action_needed == "MOVE":
            return {
                "Forward": self.forward_cost(coordinates),
                "Bash": (self.forward_cost(coordinates) + 3),
            }

    # Because of the way that dictionaries update, there needed to be an empty dictionary for the initial iterations,
    # or else the self functions would never update.
    def dictionary_holder_empty(self, action_needed, creation):
        # Same reverse as the other dictionary.
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

    def get_move(self, child_coordinates, parent_x, parent_y):
        if (abs(child_coordinates[0] - parent_x) > 1) or \
                (abs(child_coordinates[1] - parent_y) > 1):
            return 'Bash'
        else:
            return 'Forward'

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

    def expand_frontier(self, coordinates, orientation):
        # cumulative_cost is the cost of the path to this node, the cumulative cost is taken from the marked_map cell
        # at the coordinates, and the specific orientation of the node that is being expanded.
        parent = (getattr(self.marked_map[coordinates[1]][coordinates[0]], orientation))
        cumulative_cost = parent.cumulative_cost
        # Number of actions leading to this point.
        cumulative_action = parent.cumulative_action
        # Depth counts the number of nodes that it took to get to this node.
        depth = (getattr(self.marked_map[coordinates[1]][coordinates[0]], orientation)).depth
        # If this is the first time through (i.e. if we are at the start) then true so that the special starting
        # dictionary can be used.
        if self.counter == 0:
            first = True
        else:
            first = False
        self.counter += 1

        # Iterate through each combo of turn and move in the dictionary. .keys() returns the keys of the dictionary.
        for turn in self.dictionary_holder_empty("TURNING", first).keys():
            for move in self.dictionary_holder_empty("MOVE", first).keys():
                result_holder = []
                new_orientation = []
                final_cost = 0
                # Gives a new coordinates and orientation given the turn and move taken as well as the coordinates
                # and orientation of the parent.
                result_holder = Toolbox.result(coordinates, turn, move, orientation)
                # New x and y values.
                newx, newy = result_holder[0]
                # New orientation
                new_orientation = result_holder[1]

                # Only proceeds if the new coordinates is within the range of the map, and has not been expanded.
                # The self.visited is the binary matrix of true and false.
                if newy in range(len(self.map)) and newx in range(len(self.map[newy])) and not self.visited[newy][newx]:
                    # Counts the total number of nodes that have been expanded. Now that we know this node is legal,
                    # we will expand it, so we increment the counter by 1.
                    self.total += 1
                    # Gets the cost of the proposed turn and move.
                    temp_cost = self.dictionary_holder("TURNING", first, coordinates)[turn] \
                        + self.dictionary_holder("MOVE", first, [newx, newy])[move]

                    new_cell = copy.deepcopy(getattr(self.marked_map[newy][newx], new_orientation)) # TODO : does this copy?

                    better_than_sum = self.get_classic_heuristic(newx, newy)
                    new_cell.estimated_CTG = better_than_sum
                    new_cell.heuristic5 = better_than_sum + cumulative_cost + temp_cost
                    # Set the cost of the cell in the marked map to the final cost.
                    new_cell.cumulative_cost = cumulative_cost + temp_cost
                    # ~~~~~~~~~~~~~~~~~~~~
                    # For the purpose of training function
                    if first:
                        new_cell.heuristic_roc = 0
                        new_cell.cost_roc = 0
                        new_cell.estimated_CTG_roc = 0
                        new_cell.estimated_CTG_roc_SUM = 0
                    if not first:
                        new_cell.heuristic_roc = new_cell.heuristic5 - parent.heuristic5
                        new_cell.cost_roc = new_cell.cumulative_cost - parent.cumulative_cost
                        new_cell.estimated_CTG_roc = new_cell.estimated_CTG - parent.estimated_CTG
                        new_cell.estimated_CTG_roc_SUM = (parent.estimated_CTG_roc_SUM + new_cell.estimated_CTG_roc)
                    # ~~~~~~~~~~~~~~~~~~~~

                    new_heuristic_cost = self.heuristic_calculator(newx, newy, new_orientation, new_cell.estimated_CTG_roc_SUM / (depth + 1) )
                    # Adds the cost of the proposed move to the cost of the heuristic calculated at the cell x, y.
                    new_heuristic_temp_cost = temp_cost + new_heuristic_cost
                    # Adds the heuristic cost to the cumulative cost that it took to get here.
                    new_heuristic_final_cost = new_heuristic_temp_cost + cumulative_cost
                    old_cell = getattr(self.marked_map[newy][newx], new_orientation)
                    # If the new cell is empty, go right ahead, and if the heuristic of the new cell is greater than
                    # the new heuristic that we just calculated, then we cna move ahead.
                    if not old_cell.filled or old_cell.new_heuristic_final_cost > new_heuristic_final_cost:
                        # Add the coordinates and orientation that we just found to the frontier. The frontier is a min
                        # heap sorted by the heuristic.
                        heapq.heappush(self.frontier, (new_heuristic_final_cost, [newx, newy], new_orientation))
                        # added so we can find other spaces around it
                        new_cell.current_coordinate = [newx, newy]
                        # Set the heuristic to the final heuristic.
                        new_cell.orientation = new_orientation
                        new_cell.new_heuristic_final_cost = new_heuristic_final_cost

                        # Denote that the cell has been visited.
                        new_cell.filled = True
                        # Add the parent coordinates and orientation and add the depth.
                        new_cell.parent_coordinates = coordinates
                        new_cell.parent_orientation = orientation
                        new_cell.depth = depth + 1
                        # Set the visited binary matrix to true.
                        self.visited[coordinates[1]][coordinates[0]] = True
                        # Adding to the number of actions taken, if there has been no turn, do not add an action for it.
                        if turn == "None":
                            new_cell.cumulative_action = cumulative_action + 1
                        else:
                            new_cell.cumulative_action = cumulative_action + 2

                        setattr(self.marked_map[newy][newx], new_orientation, new_cell)


# Returns the moves taken in order take.
    def back_tracking(self, child_coordinates, orientation, back_tracking_list):
        # If the start coordinates are equal to teh coordinates currently being investigated, then it is over.
        if child_coordinates == self.start:
            # While there is still something left in the back_tracking_list, pop it off and print it.
            while len(back_tracking_list) > 0:
                print(back_tracking_list.pop())

        else:
            # child_node is the node that we are currently looking at.
            child_node = getattr(self.marked_map[child_coordinates[1]][child_coordinates[0]], orientation)
            # Get the parent coordinates from the marked map.
            parent_y = child_node.parent_coordinates[1]
            parent_x = child_node.parent_coordinates[0]

            # Toolbox.get_move and Toolbox.turn_decoder get the move that would have to have been made given the child
            # coordinates and orientation and the parent coordinates. get_move determines the distance that would need
            # to be traveled to get from the parent coordinates to the child coordinates, determining forward or bash,
            # and turn_decoder determines which turn the parent would have needed to make to get their orientation to
            # match the orientation of the child.
            parent_node = getattr(self.marked_map[parent_y][parent_x], child_node.parent_orientation)
            move = self.get_move(child_coordinates, parent_x, parent_y)
            turn = self.turn_decoder(child_node.parent_orientation,orientation)
            # As in the expand_frontier function, no turn is not counted.
            if turn == "None":
                back_tracking_list.append(move)
            else:
                back_tracking_list.append(turn)
                back_tracking_list.append(move)

            # recursive call to the back_tracking function. The parent coordinates and orientation are now used.
            self.back_tracking([parent_x, parent_y], child_node.parent_orientation, back_tracking_list)

    # Call the iterator on the class object to actually run the algorithm.
    def iterator(self):
        # While loop is used here to make this a tail recursion so that it does not overflow the stack.
        while True:
            # The cheapest node is the popped from the frontier.
            cheapest_node = heapq.heappop(self.frontier)
            # Getting the x and y coordinates of the cheapest node.
            cheapest_x = cheapest_node[1][0]
            cheapest_y = cheapest_node[1][1]
            # If the cheapest node is the goal, then it is all over.
            if cheapest_node[1] == self.goal:
                back_tracking_list = deque()
                # Gets whatever the current node is from the marked_map. cheapest_y and cheapest_x are reversed due to
                # the way that matrices are written (rows before columns). cheapest_node[2] is the orientation.
                best_node = getattr(self.marked_map[cheapest_y][cheapest_x], cheapest_node[2])
                # the backtracking function takes the coordinates and orientation and returns a list of moves made in
                # order. The reason that this is not done within the node itself is to cut down on the size of the
                # objects that are being manipulated.
                self.back_tracking(cheapest_node[1], cheapest_node[2], back_tracking_list)
                print('Path depth =', best_node.depth, ', Actions taken =', best_node.cumulative_action, ', Score =',
                      100-best_node.cumulative_cost, ', Nodes explored =', self.counter, ', Branching = ',
                      round((self.total-1)/self.counter, 2))

                return best_node, round((self.total-1)/self.counter, 2), self.counter, self.marked_map, self.visited
                break
            else:
                # Expand the frontier on the coordinates (cheapest_node[1]) and orientation (cheapest_node[2]) of the
                # cheapest node.
                self.expand_frontier(cheapest_node[1], cheapest_node[2])
