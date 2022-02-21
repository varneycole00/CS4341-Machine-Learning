import math


class FeatureCalculator :

    @staticmethod
    def total_terrain_cost_to_goal_horzOrVert(dir_goal_to_robot,  Pal):
        # add 1 for going to all for going forward to goal
        above_left, above_right, left_side, center, right_side = [], [], [], [], []
        goal_area = Pal.goal_area
        if dir_goal_to_robot == 'N' :
            above_left, above_right = goal_area[1][0], goal_area[1][2]
            left_side, center, right_side = goal_area[2][0], goal_area[2][1], goal_area[2][2]
        elif dir_goal_to_robot == 'W' :
            above_left, above_right = goal_area[0][1], goal_area[2][1]
            left_side, center, right_side = goal_area[0][0], goal_area[1][0], goal_area[2][0]
        elif dir_goal_to_robot == 'S' :
            above_left, above_right = goal_area[1][2],goal_area[1][0]
            left_side, center, right_side = goal_area[0][2], goal_area[0][1], goal_area[0][0]
        elif dir_goal_to_robot == 'E' :
            above_left, above_right = goal_area[2][1], goal_area[0][1]
            left_side, center, right_side = goal_area[2][2], goal_area[1][2], goal_area[0][2]

        num_points = 0
        sum = 0
        # path 1 thru center
        if center[0] in range(len(Pal.map[0])) and center[1] in range(len(Pal.map)):
            sum += Pal.map[center[1]][center[0]] + 1
            num_points += 1
        # path 2 thru left side,
        #   involves forward, forward, turn
        if left_side[0] in range(len(Pal.map[0])) and left_side[1] in range(len(Pal.map)) and above_left[0] in range(len(Pal.map[0])) and above_left[1] in range(len(Pal.map)) :
            sum += Pal.map[left_side[1]][left_side[0]] + Pal.map[above_left[1]][above_left[0]] \
                    + Pal.get_turn_cost(above_left) + 1 + 3 # 3 represents turn sequence needed to approach l/r side
            num_points += 1
        # path 3 thru right side,
        #   involves forward, forward, turn
        if right_side[0] in range(len(Pal.map[0])) and right_side[1] in range(len(Pal.map)) and above_right[0] in range(len(Pal.map[0])) and above_right[1] in range(len(Pal.map)) :
            sum += Pal.map[right_side[1]][right_side[0]] + Pal.map[above_right[1]][above_right[0]] \
                    + Pal.get_turn_cost(above_right) + 1 + 3 # 3 represents turn sequence needed to approach l/r side
            num_points += 1



        return [sum, num_points]



    @staticmethod
    def total_terrain_cost_to_goal_diag(dir_goal_to_robot, Pal):
        result1 = []
        result2 = []
        if dir_goal_to_robot == 'SE' :
            result1 = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('S', Pal)
            result2 = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('E', Pal)
        elif dir_goal_to_robot == 'NE' :
            result1 = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('N', Pal)
            result2 = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('E', Pal)
        elif dir_goal_to_robot == 'NW' :
            result1 = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('N', Pal)
            result2 = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('W', Pal)
        elif dir_goal_to_robot == 'SW' :
            result1 = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('S', Pal)
            result2 = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('W', Pal)

        return (result1[0] + result2[0]) / (result1[1] + result2[1])



    @staticmethod
    def estimate_cost_with_knowledge(direction, x, y, heuristic5, Pal):

        gx = Pal.goal[0]
        gy = Pal.goal[1]

        if x == gx and y == gy : return 0

        # get direction of robot relative to goal
        avg_move_from_cur = FeatureCalculator.get_avg_move_toward_goal_wDir(direction, False, x, y, Pal)
        # find average move without turns in that direction
        avg_goal_cost = 0

        if   x == gx and y < gy: # South
            result = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('N', Pal)
        elif x < gx and y < gy: # South East
            result = FeatureCalculator.total_terrain_cost_to_goal_diag('NW', Pal)
        elif x < gx and y == gy: # East
            result = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('W', Pal)
        elif x < gx and y > gy: # North East
            result = FeatureCalculator.total_terrain_cost_to_goal_diag('SW', Pal)
        elif x == gx and y > gy: # North
            result = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('S', Pal)
        elif x > gx and y > gy: # North WEst
            result = FeatureCalculator.total_terrain_cost_to_goal_diag('SE', Pal)
        elif x > gx and y == gy: # west
            result = FeatureCalculator.total_terrain_cost_to_goal_horzOrVert('E', Pal)
        elif x > gx and y < gy: # South West
            result = FeatureCalculator.total_terrain_cost_to_goal_diag('NE', Pal)


        # if distance is less than 2 return avg_goal_cost
        # if distance is less than 5 return avg_move_cur + avg_goal_cost
        linear_distance = math.sqrt(math.pow(x - gx, 2) + math.pow(y - gy, 2))
        if linear_distance < 2 :
            return FeatureCalculator.get_avg_move_toward_goal_wDir_no_bash(direction, False, x, y, Pal)
        elif linear_distance < 8 :
            return avg_move_from_cur + heuristic5
        else:
            return avg_move_from_cur + (heuristic5 - 2) + (result[0] / result[1])




    @staticmethod
    def find_costs_horzOrVert(direction, x, y, includesTurns, dominant, secondary1, secondary2, worst, Pal):
        list_of_points = []
        total_terrain_cost = 0
        number_of_points = 0

        if direction == dominant[0]:
            if includesTurns :
                total_terrain_cost += 2 * Pal.get_turn_cost([x,y])
                number_of_points += 2
            list_of_points = [(dominant[1], True)]
        elif direction == secondary1[0]:
            if includesTurns :
                total_terrain_cost += Pal.get_turn_cost([x,y])
                number_of_points += 1
            list_of_points = [(secondary1[1], False)]
        elif direction == secondary2[0]:
            if includesTurns :
                total_terrain_cost += Pal.get_turn_cost([x,y])
                number_of_points += 1
            list_of_points = [(secondary2[1], False)]
        elif direction == worst[0] :
            if includesTurns :
                total_terrain_cost += Pal.get_turn_cost([x,y])
                number_of_points += 1
        return [list_of_points, total_terrain_cost, number_of_points]

    @staticmethod
    def find_costs_diag(direction, x, y, includesTurns, dominant1, dominant2, worst1, worst2, Pal):
        list_of_points = []
        total_terrain_cost = 0
        number_of_points = 0

        if direction == dominant1[0]:
            if includesTurns :
                total_terrain_cost += Pal.get_turn_cost([x,y])
                number_of_points += 1
            list_of_points = [(dominant1[1], True)]
        elif direction == dominant2[0]:
            if includesTurns :
                total_terrain_cost += Pal.get_turn_cost([x,y])
                number_of_points += 1
            list_of_points = [(dominant2[1], True)]
        elif direction == worst1[0] or direction == worst2[0]:
            if includesTurns :
                total_terrain_cost += Pal.get_turn_cost([x,y])
                number_of_points += 1

        return [list_of_points, total_terrain_cost, number_of_points]

    # This is worse than other average
    @staticmethod
    def get_avg_move_toward_goal_wDir_no_bash(direction, includesTurns, x, y, Pal) :
        return FeatureCalculator.get_avg_move_toward_goal_wDir(direction, includesTurns, x, y, Pal, False)

    @staticmethod
    def get_avg_move_toward_goal_wDir(direction, includesTurns, x, y, Pal, includesBash = True) :
        # !!does not take into account directionality <- we could make this better
        # Each if statement accounts for one of the eight directions the goal can be from the current point
        #   with this it calculates the average terrain cost of spaces that the piece is likely to take
        gx = Pal.goal[0]
        gy = Pal.goal[1]

        if x == gx and y == gy : return 0
        result = []
        NorthCoord = (x, y - 1)
        SouthCoord = (x, y + 1)
        EastCoord = (x + 1, y)
        WestCoord = (x - 1, y)



        if   x == gx and y < gy:
            result = FeatureCalculator.find_costs_horzOrVert(direction, x, y, includesTurns,
                                                   ('South', SouthCoord),
                                                   ('East', EastCoord), ('West', WestCoord),
                                                   ('North'), Pal)

        elif x < gx and y < gy:
            result = FeatureCalculator.find_costs_diag(direction, x, y, includesTurns,
                                             ('South', SouthCoord), ('East', EastCoord),
                                             ('West'), ('North'), Pal)
        elif x < gx and y == gy:
            result = FeatureCalculator.find_costs_horzOrVert(direction, x, y, includesTurns,
                                                   ('East', EastCoord),
                                                   ('South', SouthCoord), ('North', NorthCoord),
                                                   ('West'), Pal)
        elif x < gx and y > gy:
            result = FeatureCalculator.find_costs_diag(direction, x, y, includesTurns,
                                             ('East', EastCoord), ('North', NorthCoord),
                                             ('West'), ('South'), Pal)
        elif x == gx and y > gy:
            result = FeatureCalculator.find_costs_horzOrVert(direction, x, y, includesTurns,
                                                   ('North', NorthCoord),
                                                   ('East', EastCoord), ('West', WestCoord),
                                                   ('South'), Pal)
        elif x > gx and y > gy:
            result = FeatureCalculator.find_costs_diag(direction, x, y, includesTurns,
                                             ('West', WestCoord), ('North', NorthCoord),
                                             ('South'), ('East'), Pal)
        elif x > gx and y == gy:
            result = FeatureCalculator.find_costs_horzOrVert(direction, x, y, includesTurns,
                                                   ('West', WestCoord),
                                                   ('South', SouthCoord), ('North', NorthCoord),
                                                   ('East'), Pal)
        elif x > gx and y < gy:
            result = FeatureCalculator.find_costs_diag(direction, x, y, includesTurns,
                                             ('South', SouthCoord), ('West', WestCoord),
                                             ('North'), ('East'), Pal)

        list_of_points = result[0]
        total_terrain_cost = result[1]
        number_of_points = result[2]

        # sums the terrain cost of all forward moves if the goal is directly horizontal or vertical to the current point
        for coordiante in list_of_points :
            x1 = coordiante[0][0]
            y1 = coordiante[0][1]

            if x1 in range(len(Pal.map[0])) and y1 in range(len(Pal.map)):
                terrain_cost = Pal.map[y1][x1]
                if includesBash and coordiante[1] :
                    total_terrain_cost += 3
                    number_of_points += 1
                total_terrain_cost += terrain_cost if isinstance(terrain_cost, int) else 1
                number_of_points += 1

        return total_terrain_cost / number_of_points if number_of_points != 0 else 0


    # This is better than other average
    @staticmethod
    def get_avg_move_toward_goal(x, y, gx, gy, map) :
        if x == gx and y == gy : return 0
        list_of_points = []
        total_terrain_cost = 0
        number_of_points = 0
        number_of_bashes = 0
        NorthCoord = (x, y - 1)
        SouthCoord = (x, y + 1)
        EastCoord = (x + 1, y)
        WestCoord = (x - 1, y)

        # !!does not take into account directionality <- we could make this better
        # Each if statement accounts for one of the eight directions the goal can be from the current point
        #   with this it calculates the average terrain cost of spaces that the piece is likely to take
        if   x == gx and y < gy:
            list_of_points = [SouthCoord, WestCoord, EastCoord ]
            number_of_bashes = 1
        elif x < gx and y < gy:
            list_of_points = [SouthCoord, EastCoord]
            number_of_bashes = 2
        elif x < gx and y == gy:
            list_of_points = [SouthCoord, NorthCoord, EastCoord]
            number_of_bashes = 1
        elif x < gx and y > gy:
            list_of_points = [EastCoord, NorthCoord]
            number_of_bashes = 2
        elif x == gx and y > gy:
            list_of_points = [WestCoord, EastCoord, NorthCoord]
            number_of_bashes = 1
        elif x > gx and y > gy:
            list_of_points = [WestCoord, NorthCoord]
            number_of_bashes = 2
        elif x > gx and y == gy:
            list_of_points = [SouthCoord, NorthCoord, WestCoord]
            number_of_bashes = 1
        elif x > gx and y < gy:
            list_of_points = [WestCoord, SouthCoord]
            number_of_bashes = 2


        # sums the terrain cost of all forward moves if the goal is directly horizontal or vertical to the current point
        for coordiante in list_of_points :
            x1 = coordiante[0]
            y1 = coordiante[1]

            if x1 in range(len(map[0])) and y1 in range(len(map)):
                terrain_cost = map[y1][x1]
                total_terrain_cost += terrain_cost if isinstance(terrain_cost, int) else 1
                number_of_points += 1  # one forward move and one bash

        number_of_points += number_of_bashes
        total_terrain_cost += 3 * number_of_bashes
        turn_cost = map[y][x]
        total_terrain_cost += 2 *  math.ceil(turn_cost if isinstance(turn_cost, int) else 1)
        number_of_points += 2


        return total_terrain_cost / number_of_points if number_of_points != 0 else 0



