import search
import random
import math
import itertools
from itertools import product




class HarryPotterProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):
        self.map = initial['map']
        self.num_rows = len(self.map)
        self.num_columns = len(self.map[0])
        self.wizards = initial['wizards']
        self.death_eaters = initial['death_eaters']
        self.horcruxes = initial['horcruxes']
        self.voldi = None
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 'V':
                    self.voldi = (i, j)
        state = []
        curr_tuple = ["wizards"]
        for wizard, value in self.wizards.items():
            x = (wizard, value)
            curr_tuple.append(x)
        state.append(tuple(curr_tuple))
        curr_tuple = ['death_eaters']
        for death_eater in self.death_eaters.keys():
            x = (death_eater, (0, True))
            curr_tuple.append(x)
        state.append(tuple(curr_tuple))
        voldemort_dead = False
        state.append(voldemort_dead)
        horcruxes = []
        for index, loc in enumerate(self.horcruxes):
            horcruxes.append((loc, index))

        state.append(("Destroyed_horcrux", tuple(horcruxes)))
        self.initial = tuple(state)
        self.game_over = False
        self.num_turns = 0
        self.sol_exist = False
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        search.Problem.__init__(self, self.initial)

    def actions(self, state):
        """Return the valid actions that can be executed in the given state."""
        wizards_actions = {}
        wizards = [wizard[0] for wizard in state[0]][1:]
        loc = [x[1][0] for x in state[0]][1:]
        copy_horcrux = []
        dict_horcrux = {}
        for horcrux in list(state[-1][1]):
            copy_horcrux.append(horcrux)
            if horcrux[0] in dict_horcrux.keys():
                dict_horcrux[horcrux[0]] += 1
            else:
                dict_horcrux[horcrux[0]] = 1

        harry_loc = None
        for ind, wizard in enumerate(wizards):
            if wizard == 'Harry Potter':
                harry_loc = loc[ind]
        for index, wiz in enumerate(wizards):
            wizards_actions[wiz] = []
            wizards_actions[wiz].append(('wait', wiz))
            for horcrux in copy_horcrux:
                if loc[index] in self.horcruxes and loc[index] == horcrux[0]:
                    if dict_horcrux[horcrux[0]] > 1:
                        dict_horcrux[horcrux[0]] -= 1
                        copy_horcrux.remove(horcrux)
                    wizards_actions[wiz].append(('destroy', wiz, horcrux[1]))

                    # break
            legal_actions = self.check_directions_validity(loc[index][0], loc[index][1])
            for legal_action, valid in legal_actions.items():
                if valid and self.map[legal_action[0]][legal_action[1]] != 'I':
                    if self.map[legal_action[0]][legal_action[1]] != 'V':
                        wizards_actions[wiz].append(('move', wiz, legal_action))
                    if self.map[legal_action[0]][legal_action[1]] == 'V' and len(list(state[-1][
                                                                                          1])) == 0 and wiz == 'Harry Potter':  # check if it could be that they might die if they get there without harry
                        wizards_actions[wiz].append(('move', wiz, legal_action))
                    else:
                        continue
            if self.map[loc[index][0]][loc[index][1]] == 'V' and len(list(state[-1][1])) == 0 and wiz == 'Harry Potter':
                wizards_actions[wiz] = []
                wizards_actions[wiz].append(('kill', 'Harry Potter'))
        all_actions = product(*(wizards_actions[w] for w in wizards_actions))
        return list(all_actions)

    def check_directions_validity(self, r, c):
        actions = {(r + 1, c): True, (r - 1, c): True, (r, c + 1): True, (r, c - 1): True}
        if self.num_rows <= r + 1:
            actions[(r + 1, c)] = False
        if r - 1 < 0:
            actions[(r - 1, c)] = False
        if c + 1 >= self.num_columns:
            actions[(r, c + 1)] = False
        if c - 1 < 0:
            actions[(r, c - 1)] = False
        return actions

    def check_death_eater(self, wizard, i, state, wizard_location):
        counter = 0
        for death_eater in state[1][1:]:  # if they get to voldemort before harry they dies
            if len(self.death_eaters[death_eater[0]]) > 0:
                if self.death_eaters[death_eater[0]][death_eater[1][0]] == wizard_location:
                    counter += 1
        if state[0][i][1][1] >= counter:
            # self.game_over = True
            temp = list(state[0])
            new_val = state[0][i][1][1] - counter
            temp[i] = (wizard, (temp[i][1][0], new_val))
            state[0] = tuple(temp)
        else:
            temp = list(state[0])
            temp[i] = (wizard, (temp[i][1][0], 0))
            state[0] = tuple(temp)

        # if state[0][i][1][1]==0:
        #     break
        # temp=None
        # for death_eater in next_state[1][1:]:
        #     if self.death_eaters[death_eater[0]][death_eater[1][0]] == wizard_location:
        #         if next_state[0][i][1][1] - 1 == 0:
        #             self.game_over = True
        #         else:
        #             temp = list(next_state[0])
        #             temp[i] = (wizard, (a[2], temp[i][1][1]))
        #             next_state[0] = tuple(temp)
        #

    def result(self, state, action):
        """Return the state that results from executing the given action in the given state."""
        next_state = list(state)

        for a in action:
            wizard = a[1]
            if a[0] == 'move':
                for i in range(1, len(state[0])):
                    # wizard_location=a[2]
                    if state[0][i][0] == wizard:
                        temp = list(next_state[0])
                        temp[i] = (wizard, (a[2], temp[i][1][1]))
                        next_state[0] = tuple(temp)
            elif a[0] == 'destroy':
                horcrux_index = a[2]
                for horcrux in list(state[-1][1]):
                    if horcrux_index == horcrux[1]:
                        list_state = list(state[-1][1])
                        list_state.remove(horcrux)
                        # updated_detroyed.append(horcrux_index)
                        next_state[-1] = tuple(('Destroyed_horcrux', tuple(list_state)))

            elif a[0] == 'kill':
                next_state[len(state) - 2] = True
                self.sol_exist = True
        death_eaters_ls = list(next_state[1])

        # Iterate over the list of death eaters starting from index 1
        for death_eater_index in range(1, len(death_eaters_ls)):
            # Extract and convert the current death eater tuple to a list for modification
            current_death_eater = list(death_eaters_ls[death_eater_index])
            # Convert the position information tuple to a list
            position_info = list(current_death_eater[1])

            # Retrieve the group of the current death eater based on its identifier
            group = self.death_eaters[current_death_eater[0]]

            # Only modify if the group size is not 1
            if len(group) != 1:
                # Check and update the position based on the direction flag
                if position_info[1]:  # True for forward/right
                    if position_info[0] == len(group) - 1:
                        position_info[1] = False
                        position_info[0] -= 1
                    else:
                        position_info[0] += 1
                else:  # False for backward/left
                    if position_info[0] == 0:
                        position_info[1] = True
                        position_info[0] += 1
                    else:
                        position_info[0] -= 1

                # Assign the modified list back as a tuple
                current_death_eater[1] = tuple(position_info)
                death_eaters_ls[death_eater_index] = tuple(current_death_eater)
        next_state[1] = tuple(death_eaters_ls)
        for i in range(1, len(state[0])):
            wizard_location = next_state[0][i][1][0]
            self.check_death_eater(next_state[0][i][0], i, next_state, wizard_location)

        # Convert the tuple to a list to allow modifications

        # Convert the list back to a tuple if needed
        # next_state[1] = tuple(death_eaters_ls)
        return tuple(next_state)

    def goal_test(self, state):
        """Return True if the state is a goal state."""

        harry_ind = None
        wizards_alive = True
        for i in range(1, len(state[0])):
            if state[0][i][0] == 'Harry Potter':
                harry_ind = i
            if state[0][i][1][1] == 0:
                wizards_alive = False
        if wizards_alive == False:
            return False
        harry_place = state[0][harry_ind][1][0]

        if len(list(state[-1][1])) == 0 and self.map[harry_place[0]][harry_place[1]] == 'V' and wizards_alive == True:
            if state[len(state) - 2]:  # state[len(state)-2]
                return True
        return False

    def death_eaters_postions(self, state):
        death_eaters_postions_list = []
        for death_eater in state[1][1:]:
            if len(self.death_eaters[death_eater[0]]) > 0:
                death_eaters_postions_list.append(self.death_eaters[death_eater[0]][death_eater[1][0]])
        return death_eaters_postions_list

    def h(self, node):
        state = node.state
        soul_loss_penalty = 0
        death_eaters_postions_list = self.death_eaters_postions(state)
        current_horcruxes = []
        for i in range(len(self.horcruxes)):
            for index in list(state[-1][1]):
                if i == index[1]:
                    current_horcruxes.append(i)
            # current_horcruxes.append(i)
        harry_loc = None
        new_huristic = 0
        wizards_positions = []
        for wizard in range(1, len(state[0])):
            wizards_positions.append(state[0][wizard][1][0])
            if state[0][wizard][0] == 'Harry Potter':
                harry_loc = state[0][wizard][1][0]
            soul = state[0][wizard][1][1]
            wizard_loc = state[0][wizard][1][0]
            soul_loss_penalty += self.heuristic_soul_loss_penalty(state, soul, wizard_loc, death_eaters_postions_list,
                                                                  current_horcruxes)
        first_h, closest_wizards = self.h1(node)
        second_h = self.h2(harry_loc, self.voldi, current_horcruxes, wizards_positions)
        dict1 = {'sol function': soul_loss_penalty, 'h1': first_h, 'h2': second_h}
        h1_helper_val = self.h1_helper(state, closest_wizards)
        self.count1 += first_h
        self.count2 += second_h
        self.count3 += soul_loss_penalty
        dict2 = {'count1': self.count1, 'count2': self.count2, 'count3': self.count3}
        # print(dict1)
        # print(dict2)

        # if len(state[-1][1])>len(self.horcruxes)*0.5:
        #    return 0.5*second_h+first_h+soul_loss_penalty*3.0

        # if :
        #     0.5 * first_h + 0.5 * soul_loss_penalty
        # if
        closest_huristic = self.closer_horcrux(state, current_horcruxes)
        dict1 = {'sol function': soul_loss_penalty, 'h1': first_h, 'h2': second_h,
                 'len_current': len(current_horcruxes)}
        # print(dict1)
        # if closest_huristic>first_h:
        # len(current_horcruxes)
        # return second_h+0.5* soul_loss_penalty+0.5*first_h+len(current_horcruxes)+closest_huristic-first_h
        # if len(current_horcruxes)>0:
        #     if len(self.wizards)/len(current_horcruxes)>=0.5:
        #         return 0.5*first_h+second_h*0.5 +soul_loss_penalty*2.0

        # if len(current_horcruxes)==1:
        #     0.5 * soul_loss_penalty + 0.5 * first_h + second_h + len(current_horcruxes) + h1_helper_val/len(self.wizards)
        # 0.5* soul_loss_penalty+0.5*first_h+second_h+len(current_horcruxes)+h1_helper_val/(len(self.wizards))
        # return 0.5* soul_loss_penalty+0.5*replace_h1+1.0*second_h
        dict2 = {'sol function': soul_loss_penalty, 'h1': 0.5 * first_h, 'h2': 0.5 * second_h,
                 'len_current': len(current_horcruxes)}
        # print(dict2)
        sum = soul_loss_penalty + 0.5 * first_h + 0.5 * second_h
        # print(f'sum = {sum}')
        if len(current_horcruxes) == 0:
            return soul_loss_penalty + second_h
        return soul_loss_penalty + 0.5 * first_h + second_h * 0.3

    def closer_horcrux(self, state, remained_horcruxes):
        distances = {}
        closest_horc = {}
        for wizard_horc in range(1, len(state[0])):
            min_dist = 0
            if len(remained_horcruxes) > 0:
                distances[wizard_horc] = [0] * len(remained_horcruxes)
                min_dist = float('inf')
                for index, horcrux in enumerate(remained_horcruxes):
                    current_dist = self.manhattan_distance(self.horcruxes[horcrux], state[0][wizard_horc][1][0])
                    distances[wizard_horc][index] = current_dist
                    if current_dist < min_dist:
                        min_dist = current_dist
                        closest_horc[wizard_horc] = index

        dist_sum = 0
        if len(remained_horcruxes) > 0:
            for wizard in range(1, len(state[0])):
                current_val = 0
                for wizard_ in range(1, len(state[0])):
                    if wizard != wizard_:
                        closest_horcrux_index = closest_horc[wizard]
                        first_wizard_dist = distances[wizard][closest_horcrux_index]
                        second_wizard_dist = distances[wizard_][closest_horcrux_index]
                        if first_wizard_dist < second_wizard_dist:
                            # dist_sum+=second_wizard_dist-first_wizard_dist
                            current_val = min(current_val, second_wizard_dist - first_wizard_dist)
                            # current_val=float('inf')
                dist_sum += current_val
        return dist_sum

    def assign_min_horcrux(self, state, closest_wizard):
        distance = 0
        for wizard_ in range(1, len(state[0])):
            max_dist = 0
            if wizard_ not in closest_wizard:
                print(state[0][wizard_][0])
                if len(list(state[-1][1])) > 0:
                    for horc_ in list(state[-1][1]):
                        manhattan = self.manhattan_distance(state[0][wizard_][1][0], horc_[0])
                        max_dist = max(max_dist, manhattan)
                        distance += max_dist
        return distance

    def h1_helper(self, state, closest_wizard):
        horcrux_copy = list(state[-1][1])
        distance = 0
        if len(horcrux_copy) > 0:
            for wizard_min_horc in range(1, len(state[0])):
                if wizard_min_horc in closest_wizard:
                    min_dist_horc = float('inf')
                    current_min_horc = None
                    for horcrux_wiz in horcrux_copy:
                        manhatten_wiz_horcrux = self.manhattan_distance(state[0][wizard_min_horc][1][0], horcrux_wiz[0])
                        if min_dist_horc > manhatten_wiz_horcrux:
                            current_min_horc = horcrux_wiz
                            min_dist_horc = manhatten_wiz_horcrux
                    if len(list(state[-1][1])) > 0:
                        horcrux_copy.remove(current_min_horc)
                else:
                    min_dist_horc = 0
                    if len(horcrux_copy) > 0:
                        min_dist_horc = float('inf')
                        for horcrux_wiz in horcrux_copy:
                            manhatten_wiz_horcrux = self.manhattan_distance(state[0][wizard_min_horc][1][0],
                                                                            horcrux_wiz[0])
                            if min_dist_horc > manhatten_wiz_horcrux:
                                current_min_horc = horcrux_wiz
                                min_dist_horc = manhatten_wiz_horcrux
                distance += min_dist_horc
        return distance

    def h1(self, node):
        state = node.state
        map_space = self.num_rows * self.num_columns
        radius = math.floor(math.sqrt(map_space / len(self.wizards)))
        # radius=1
        distance = 0
        closest_wizard_horcrux = set()
        closest_wizard = set()
        for horcrux in range(len(self.horcruxes)):
            for h in list(state[-1][1]):
                if horcrux == h[1]:
                    min_dist = float('inf')
                    current_closest_wiz_ind = None
                    for wizard in range(1, len(state[0])):
                        wizard_loc = state[0][wizard][1][0]
                        manhatten_distance = abs(wizard_loc[0] - self.horcruxes[horcrux][0]) + abs(
                            wizard_loc[1] - self.horcruxes[horcrux][1])
                        if manhatten_distance < min_dist:
                            min_dist = manhatten_distance
                            current_closest_wiz_ind = wizard
                    distance += min_dist
                    closest_wizard_horcrux.add((current_closest_wiz_ind, h))
                    closest_wizard.add(current_closest_wiz_ind)
                    break

        count = 0
        # for wizard in closest_wizard:
        #     x_loc, y_loc=state[0][wizard][1][0]
        #     for i in range(-radius, radius + 1):  # Iterate within radius in x direction
        #         for j in range(-radius, radius + 1):  # Iterate within radius in y direction
        #             # Calculate the new position to check
        #             # if i !=0 and j != 0:
        #             #     continue
        #             # else:
        #             new_x, new_y = x_loc + i, y_loc + j
        #
        #             # Ensure the position is within the map's legal boundaries
        #             if 0 <= new_x < self.num_rows and 0 <= new_y < self.num_columns:
        #                 # Check if the tile is impassable ('I')
        #                 if self.map[new_x][new_y] == 'I':
        #                     count += 1

        # assign_horcrux=self.assign_min_horcrux(state,closest_wizard)
        return distance + count, closest_wizard

    def souls_heuristic(self, current_pos, goals, death_eaters, harry_lives, harry_loc):
        # Extract current position of Harry Potter
        if len(goals) > 0:
            # 1. Manhattan distance to the closest goal
            manhattan = min(
                abs(current_pos[0] - goal[0]) + abs(current_pos[1] - goal[1]) for goal in goals
            )
        else:
            manhattan = 0

        # 2. Danger zone penalty
        danger_penalty = 0
        for death_eater in death_eaters.values():
            for pos in death_eater:  # Iterate through the death eater's path
                if abs(current_pos[0] - pos[0]) + abs(current_pos[1] - pos[1]) <= 1:
                    danger_penalty += 10  # Add penalty for being near a danger zone

        # 3. Multi-goal distance (approximation using a greedy strategy)
        remaining_goals = goals[:]
        multi_goal_distance = 0
        current = current_pos
        while remaining_goals:
            next_goal = min(remaining_goals, key=lambda g: abs(current[0] - g[0]) + abs(current[1] - g[1]))
            multi_goal_distance += abs(current[0] - next_goal[0]) + abs(current[1] - next_goal[1])
            current = next_goal
            remaining_goals.remove(next_goal)

        # 4. Remaining lives penalty
        remaining_lives = harry_lives
        lives_penalty = 0 if remaining_lives > 1 else 100  # Strong penalty if lives are critical

        # Combine heuristics
        combined_heuristic = (
                1.0 * manhattan +
                2.0 * danger_penalty +
                1.5 * multi_goal_distance +
                3.0 * lives_penalty
        )

        return combined_heuristic

    def manhattan_distance(self, point1, point2):
        """
        Manhattan distance between two points.

        Parameters:
        - point1, point2: tuple, (x, y) coordinates of two points.

        Returns:
        - int: Manhattan distance.
        """
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    def h2(self, hary_lock, voldy_lock, remained_horcruxes, wizards_positions):
        # if len(remained_horcruxes) > 0:
        #     min_dist = float('inf')
        #     second_min_dist = float('inf')  # Initialize the second closest distance
        #
        #     for horcrux in remained_horcruxes:
        #         manhatten = self.manhattan_distance(self.horcruxes[horcrux], hary_lock)
        #
        #         if manhatten < min_dist:
        #             # Update second_min_dist before changing min_dist
        #             second_min_dist = min_dist
        #             min_dist = manhatten
        #         elif manhatten < second_min_dist:
        #             # Update second_min_dist if the distance is smaller than it but larger than min_dist
        #             second_min_dist = manhatten
        #
        #     # After the loop, min_dist is the closest and second_min_dist is the second closest
        #
        # else:
        #     min_dist=0
        #     second_min_dist=0
        map_space = self.num_rows * self.num_columns
        radius = math.floor(math.sqrt(map_space / len(self.wizards)))
        count = 0
        if len(remained_horcruxes) > 0:
            # len(remained_horcruxes)/(len(self.wizards)-1)
            count_num_horcruxes = 0
            for wiz in wizards_positions:
                count_num_wiz = 0
                in_count = 0
                pos_x, pos_y = wiz
                for i in range(-radius, radius + 1):
                    for j in range(-radius, radius + 1):
                        new_x, new_y = pos_x + i, pos_y + j
                        if 0 <= new_x < self.num_rows and 0 <= new_y < self.num_columns:
                            if self.map[new_x][new_y] == 'I':
                                count += 1
                            if len(remained_horcruxes) > 0:
                                for horcrux in remained_horcruxes:
                                    if self.horcruxes[horcrux] == (new_x, new_y):
                                        in_count += 1
                                for ww in wizards_positions:
                                    if ww == (new_x, new_y):
                                        count_num_wiz += 1
                if in_count == 0:
                    return len(self.wizards) * len(remained_horcruxes) + count
                count_num_horcruxes += count_num_wiz / in_count
                if len(self.wizards) > len(remained_horcruxes):
                    return 2 * self.manhattan_distance(hary_lock, voldy_lock) + count + len(
                        remained_horcruxes)  # len(remained_horcruxes) + count
                else:
                    return count_num_horcruxes + self.manhattan_distance(hary_lock, voldy_lock) + len(
                        remained_horcruxes) + count
        else:
            return self.manhattan_distance(hary_lock, voldy_lock) + len(remained_horcruxes) + count

    def calculate_penalty(self, state, soul_count, current, waypoints):
        """
        Calculate a dynamic penalty based on the game context.

        Parameters:
        - soul_count: int, current number of player souls.
        - current: tuple, (x, y) current player position.
        - death_eaters: list of lists, positions of Death Eaters at each step in their cycle [[(x1, y1), ...], ...].
        - cycle_length: int, number of steps in the Death Eaters' cycle.
        - current_step: int, current step in the cycle.
        - goal: tuple, (x, y) coordinates of the goal.
        - waypoints: list of tuples, unvisited waypoints [(x1, y1), ...].

        Returns:
        - float: Calculated penalty for losing a soul.
        """
        if soul_count == 0:
            return float('inf')  # Game over if no souls remain

        # Predict the Death Eaters' position at the current step
        death_eater_positions = self.death_eaters_postions(state)

        # Factor 1: Penalty increases as souls decrease
        base_penalty = 10 * (1 / (soul_count + 1))  # Higher penalty for lower souls

        # Factor 2: Penalty increases if near a Death Eater
        proximity_penalty = 0
        for index, de in enumerate(self.death_eaters):
            # if self.manhattan_distance(current, de)<=1:
            #             #     proximity_penalty +=5
            #             # else:
            #             #     continue
            proximity_penalty += max(0, len(de) - self.manhattan_distance(current, death_eater_positions[
                index]))  # Higher penalty if within 5 steps

        # Factor 3: Reduce penalty if close to the goal
        # Lower penalty for closer goals

        # Factor 4: Adjust penalty based on remaining waypoints
        distance_to_waypoints = sum(self.manhattan_distance(current, self.horcruxes[wp]) for wp in waypoints)
        waypoint_factor = max(1, distance_to_waypoints / (len(waypoints) + 1))  # More waypoints increase penalty

        # Combine factors to calculate the penalty
        penalty = base_penalty + proximity_penalty + waypoint_factor
        return max(0, penalty)  # Ensure penalty is non-negative

    def heuristic_soul_loss_penalty(self, state, soul_count, current, death_eaters,
                                    waypoints):
        penalty = self.calculate_penalty(state, soul_count, current,
                                         waypoints)  # Adjust this to balance between path length and soul loss
        if current in death_eaters:
            if soul_count <= 0:
                return float('inf')  # Game over if last soul is lost
            soul_loss_penalty = penalty * (soul_count - 1)
        else:
            soul_loss_penalty = 0
        return soul_loss_penalty


def create_harrypotter_problem(game):
    return HarryPotterProblem(game)
