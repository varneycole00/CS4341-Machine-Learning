class Toolbox:

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