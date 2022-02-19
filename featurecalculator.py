import math


class FeatureCalculator :
    @staticmethod
    def find_costs_horzOrVert(direction, x, y, dominant, secondary1, secondary2, worst, Pal):
        list_of_points = []
        total_terrain_cost = 0
        number_of_points = 0

        if direction == dominant[0]:
            total_terrain_cost += 2 * Pal.get_turn_cost([x,y])
            number_of_points += 2
            list_of_points = [(dominant[1], True)]
        elif direction == secondary1[0]:
            total_terrain_cost += Pal.get_turn_cost([x,y])
            number_of_points += 1
            list_of_points = [(secondary1[1], False)]
        elif direction == secondary2[0]:
            total_terrain_cost += Pal.get_turn_cost([x,y])
            number_of_points += 1
            list_of_points = [(secondary2[1], False)]
        elif direction == worst[0] :
            total_terrain_cost += Pal.get_turn_cost([x,y])
            number_of_points += 1
        return [list_of_points, total_terrain_cost, number_of_points]

    @staticmethod
    def find_costs_diag(direction, x, y, dominant1, dominant2, worst1, worst2, Pal):
        list_of_points = []
        total_terrain_cost = 0
        number_of_points = 0

        if direction == dominant1[0]:
            total_terrain_cost += Pal.get_turn_cost([x,y])
            number_of_points += 1
            list_of_points = [(dominant1[1], True)]
        elif direction == dominant2[0]:
            total_terrain_cost += Pal.get_turn_cost([x,y])
            number_of_points += 1
            list_of_points = [(dominant2[1], True)]
        elif direction == worst1[0] or direction == worst2[0]:
            total_terrain_cost += Pal.get_turn_cost([x,y])
            number_of_points += 1

        return [list_of_points, total_terrain_cost, number_of_points]

    # This is worse than other average
    @staticmethod
    def get_avg_move_toward_goal_wDir(direction, x, y, Pal) :
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
            result = FeatureCalculator.find_costs_horzOrVert(direction, x, y,
                                                             ('South', SouthCoord),
                                                             ('East', EastCoord), ('West', WestCoord),
                                                             ('North'), Pal)

        elif x < gx and y < gy:
            result = FeatureCalculator.find_costs_diag(direction, x, y,
                                                       ('South', SouthCoord), ('East', EastCoord),
                                                       ('West'), ('North'), Pal)
        elif x < gx and y == gy:
            result = FeatureCalculator.find_costs_horzOrVert(direction, x, y,
                                                             ('East', EastCoord),
                                                             ('South', SouthCoord), ('North', NorthCoord),
                                                             ('West'), Pal)
        elif x < gx and y > gy:
            result = FeatureCalculator.find_costs_diag(direction, x, y,
                                                       ('East', EastCoord), ('North', NorthCoord),
                                                       ('West'), ('South'), Pal)
        elif x == gx and y > gy:
            result = FeatureCalculator.find_costs_horzOrVert(direction, x, y,
                                                             ('North', NorthCoord),
                                                             ('East', EastCoord), ('West', WestCoord),
                                                             ('South'), Pal)
        elif x > gx and y > gy:
            result = FeatureCalculator.find_costs_diag(direction, x, y,
                                                       ('West', WestCoord), ('North', NorthCoord),
                                                       ('South'), ('East'), Pal)
        elif x > gx and y == gy:
            result = FeatureCalculator.find_costs_horzOrVert(direction, x, y,
                                                             ('West', WestCoord),
                                                             ('South', SouthCoord), ('North', NorthCoord),
                                                             ('East'), Pal)
        elif x > gx and y < gy:
            result = FeatureCalculator.find_costs_diag(direction, x, y,
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
                if coordiante[1] :
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
            number_of_bashes = 1
        elif x < gx and y == gy:
            list_of_points = [SouthCoord, NorthCoord, EastCoord]
            number_of_bashes = 1
        elif x < gx and y > gy:
            list_of_points = [EastCoord, NorthCoord]
            number_of_bashes = 1
        elif x == gx and y > gy:
            list_of_points = [WestCoord, EastCoord, NorthCoord]
            number_of_bashes = 1
        elif x > gx and y > gy:
            list_of_points = [WestCoord, NorthCoord]
            number_of_bashes = 1
        elif x > gx and y == gy:
            list_of_points = [SouthCoord, NorthCoord, WestCoord]
            number_of_bashes = 1
        elif x > gx and y < gy:
            list_of_points = [WestCoord, SouthCoord]
            number_of_bashes = 1


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



