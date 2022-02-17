import math


class Toolbox:

    @staticmethod
    def get_avg_move_toward_goal(x, y, gx, gy, map) :
        list_of_points = []
        total_terrain_cost = 0
        number_of_points = 0
        # !!does not take into account directionality <- we could make this better
        # Each if statement accounts for one of the eight directions the goal can be from the current point
        #   with this it calculates the average terrain cost of spaces that the piece is likely to take
        if   x == gx and y < gy:
            list_of_points = [(x, y+1), (x - 1, y),(x + 1, y) ]
        elif x < gx and y < gy:
            list_of_points = [(x, y + 1), (x + 1, y)]
        elif x < gx and y == gy:
            list_of_points = [(x, y + 1), (x, y - 1), (x + 1, y)]
        elif x < gx and y > gy:
            list_of_points = [(x + 1, y), (x, y - 1)]
        elif x == gx and y > gy:
            list_of_points = [(x - 1, y), (x + 1, y), (x, y - 1)]
        elif x > gx and y > gy:
            list_of_points = [(x - 1, y, x - 1, y + 1), (x, y + 1, x - 1, y + 1)]
        elif x > gx and y == gy:
            list_of_points = [(x, y + 1), (x, y - 1), (x - 1, y)]
        elif x > gx and y < gy:
            list_of_points = [(x - 1, y), (x, y - 1)]

        # sums the terrain cost of all forward moves if the goal is directly horizontal or vertical to the current point
        for coordiante in list_of_points :
            x1 = coordiante[0]
            y1 = coordiante[1]

            if x1 in range(len(map[0])) and y1 in range(len(map)):
                terrain_cost = map[y1][x1]
                total_terrain_cost += terrain_cost if isinstance(terrain_cost, int) else 1
                number_of_points += 1  # one forward move and one bash

        # numbers were messed with to get an answer
        # supposed to account for bashes
        total_terrain_cost += 6  # gives best results
        turn_cost = map[y][x]
        total_terrain_cost += 2 * math.ceil(turn_cost if isinstance(turn_cost, int) else 1)
        # 2 turns 1 bash? Even though the 6 from before accounts for two bashes this seems to work better
        # maybe bashes are less likely?
        number_of_points += 3


        return total_terrain_cost / number_of_points if number_of_points != 0 else 0









    @staticmethod
    def turn_decoder(parent, child):
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

    @staticmethod
    def orientation_finder(turn, orientation):
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

    @staticmethod
    def result(position, turn, move, orientation):
        x, y = position
        new_orientation = []
        holder = []
        turn = turn
        orientation = orientation
        new_orientation = Toolbox.orientation_finder(turn, orientation)
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

    @staticmethod
    def get_move(child_coordinates, parent_x, parent_y):
        if (abs(child_coordinates[0] - parent_x) > 1) or \
                (abs(child_coordinates[1] - parent_y) > 1):
            return 'Bash'
        else:
            return 'Forward'