import math
import random
import csv
import numpy as np


transitions_made = {}
outcome_count = {}
base_states = ["000", "100", "020", "120", "003", "103", "023", "123"]
lowest_occupied_base = ["HR", "1B", "2B", "1B", "3B", "1B", "2B", "1B"]
runners = [0, 1, 1, 2, 1, 2, 2, 3]
num_start_states = 24
num_end_states = 28
num_lineup_spots = 9

num_base_states = len(base_states)


class TransitionStates:
    def __init__(self, states, row_length):
        #print(states)
        self.transition_states = []
        row_element = 0
        running_probability = 0
        current_row = []
        for i in states:
            running_probability += i
            current_row.append(running_probability)
            row_element += 1
            if row_element >= row_length:
                self.transition_states.append(current_row)
                current_row = []
                row_element = 0
        #print(current_row)
        self.transition_states.append(current_row)

    def states(self):
        for i in self.transition_states:
            print(i)


class Node:
    def __init__(self, base_state_number, outs, transition_states, transition_states_non_pa):
        self.base_state_number = base_state_number
        self.base_state = base_states[base_state_number]
        self.lowest_occupied_base = lowest_occupied_base[base_state_number]
        self.num_runners = runners[base_state_number]
        self.outs = outs
        self.transition_states = transition_states
        self.transition_states_non_pa = transition_states_non_pa
        self.three_out_runs = base_state_number

    def node_number(self):
        return self.outs*8 + self.base_state_number

    def print_start_node(self):
        print("Start of inning", "base state", self.base_state, "num_runners", self.num_runners, "outs", self.outs)

    def print_node(self, at_bat_number, runs_scored=0, lineup_spot=1, non_pa_transition=False):
        pa_trans = "PA Transition"
        if non_pa_transition:
            pa_trans = "Non-Pa Transition"
        print(pa_trans,"Lineup Spot:", lineup_spot + 1, " Inning At Bat: ", at_bat_number + 1, "base state: ", self.base_state, " num_runners: ", self.num_runners, " outs: ", self.outs)
        if runs_scored > 0:
            print("Runs Scored: ", runs_scored)

    def print_first_transition_state(self):
        print(self.transition_states[0][0])

    def next_non_pa_node(self):
        r = random.random()
        row = 0
        for i in self.transition_states_non_pa:
            col = 0
            for j in i:
                if r < self.transition_states_non_pa[row][col]:
                    return (row,col)
                else:
                    col += 1
            row += 1

    def next_node(self):
        r = random.random()
        row = 0
        for i in self.transition_states:
            col = 0
            for j in i:
                #print(row, col, r, self.transition_states)
                if r < self.transition_states[row][col]:
                    return (row,col)
                else:
                    col += 1
            row += 1

class Inning:
    def __init__(self, lineup, do_print=True, include_non_pa_transitions=True):
        self.lineup = lineup
        self.active_node = lineup.current_lineup_spot().nodes[0][0]
        self.do_print = do_print
        self.include_non_pa_transitions = include_non_pa_transitions

    def non_pa_transition(self, beginning_node, at_bat_of_inning, do_print):
        next_node = self.active_node.next_non_pa_node()
        next_row = next_node[0]
        next_col = next_node[1]

        self.active_node = self.lineup.current_lineup_spot().nodes[next_row][next_col]

        start_runners_and_outs = self.runners_and_outs(beginning_node)
        end_runners_and_outs = self.runners_and_outs(self.active_node)

        runs_scored = 0
        if self.active_node.outs == 3:
            runs_scored = self.active_node.three_out_runs
        elif end_runners_and_outs < start_runners_and_outs:
            runs_scored = start_runners_and_outs - end_runners_and_outs

        if beginning_node.node_number() != self.active_node.node_number():
            if beginning_node.outs == self.active_node.outs:
                if outcome_count.has_key("SB"):
                    outcome_count["SB"] += 1
                else:
                    outcome_count["SB"] = 1
            else:
                if outcome_count.has_key("CS"):
                    outcome_count["CS"] += 1
                else:
                    outcome_count["CS"] = 1

        if do_print and beginning_node.node_number() != self.active_node.node_number():
            self.active_node.print_node(at_bat_of_inning, runs_scored, lineup_spot=self.lineup.current_spot, non_pa_transition=True)

        return runs_scored

    def iterate_inning(self, at_bat_of_inning, do_print):
        beginning_node = self.active_node

        non_pa_runs = 0
        if include_non_pa_transitions:
            #should be a loop since multiple non-pa transitions can happen here
            non_pa_runs = self.non_pa_transition(beginning_node, at_bat_of_inning, do_print)

        if self.active_node.outs == 3:
            return non_pa_runs

        next_node = self.active_node.next_node()

        next_row = next_node[0]
        next_col = next_node[1]

        self.active_node = self.lineup.current_lineup_spot().nodes[next_row][next_col]

        start_runners_and_outs = self.runners_and_outs(beginning_node)
        end_runners_and_outs = self.runners_and_outs(self.active_node)

        runs_scored = 0
        if self.active_node.outs == 3:
            runs_scored = self.active_node.three_out_runs
        elif end_runners_and_outs < 1 + start_runners_and_outs:
            runs_scored = start_runners_and_outs + 1 - end_runners_and_outs


        outs_made = self.active_node.outs - beginning_node.outs
        #Otherwise tracks base_out states
        track_base_states = True

        key = self.create_key(beginning_node, self.active_node, outs_made, runs_scored, track_base_states)

        #Track Outcomes
        if outs_made == 0:
            if outcome_count.has_key(self.active_node.lowest_occupied_base):
                outcome_count[self.active_node.lowest_occupied_base] += 1
            else:
                outcome_count[self.active_node.lowest_occupied_base] = 1
        elif outs_made == 2:
            if outcome_count.has_key("GIDP"):
                outcome_count["GIDP"] += 1
            else:
                outcome_count["GIDP"] = 1
        elif outs_made == 3:
            if outcome_count.has_key("GITP"):
                outcome_count["GITP"] += 1
            else:
                outcome_count["GITP"] = 1


        if transitions_made.has_key(key):
            transitions_made[key] += 1
        else:
            transitions_made[key] = 1

        if do_print:
            self.active_node.print_node(at_bat_of_inning, runs_scored, lineup_spot=self.lineup.current_spot)

        return runs_scored + non_pa_runs

    def create_key(self, start_node, end_node, outs_made, runs_scored, track_base_states = True):
        start_state = start_node.base_state_number if track_base_states else start_node.node_number()
        end_state = end_node.base_state_number if track_base_states else end_node.node_number()
        key = "start_" + str(start_state) + "_end_" + str(end_state) + "_outs_" + str(outs_made) + "_runs_" + str(runs_scored)
        return key

    def runners_and_outs(self, current_node):
        return current_node.outs + current_node.num_runners

    def simulate_inning(self):
        self.active_node = self.lineup.current_lineup_spot().nodes[0][0]
        inning_runs_scored = 0
        at_bat_of_inning = 0

        if self.do_print:
            self.active_node.print_start_node()

        while self.active_node.outs != 3:
            inning_runs_scored += self.iterate_inning(at_bat_of_inning, self.do_print)
            self.lineup.iterate_lineup()
            at_bat_of_inning += 1

        if self.do_print:
            print("Total runs in inning: ", inning_runs_scored)

        return inning_runs_scored


class Lineup:
    def __init__(self, lineup_spots):
        self.lineup_spots = lineup_spots
        self.num_spots = len(lineup_spots)
        self.current_spot = 0

    def print_each_spot(self):
        for spot in self.lineup_spots:
            print(spot)
            spot.print_first_transition()

    def current_lineup_spot(self):
        return self.lineup_spots[self.current_spot]

    def iterate_lineup(self):
        self.current_spot += 1
        if self.current_spot == self.num_spots:
            self.current_spot = 0


class LineupSpot:
    def __init__(self, raw_transitions_pa, raw_transitions_non_pa):
        self.nodes = []
        self.states = []
        self.states_non_pa = []

        #print(type(raw_transitions_non_pa))
        for row in raw_transitions_pa:
            #print(row)
            prob_row = self.count_to_prob(row)
            ts = TransitionStates(prob_row, num_base_states)
            #print(ts)
            self.states.append(ts.transition_states)

        for row in raw_transitions_non_pa:
            prob_row = self.count_to_prob(row)
            ts = TransitionStates(prob_row, num_base_states)
            self.states_non_pa.append(ts.transition_states)

        self.create_nodes()

    def count_to_prob(self,row):
        #print(row, type(row))
        total = float(sum(row))
        #print(total)
        new_row = [a/total for a in row]
        #print(new_row)
        return new_row

    def create_nodes(self):
        for outs in range(0, 3):
            out_nodes = []
            for state in range(0,num_base_states):
                out_nodes.append(Node(state, outs, self.states[outs*8 + state], self.states_non_pa[outs*8 + state]))
            self.nodes.append(out_nodes)
        three_out_nodes = []
        for state in range(0,4):
            three_out_nodes.append(Node(state, 3, self.states[0], self.states_non_pa[0]))
        self.nodes.append(three_out_nodes)

    def print_first_transition(self):
        print(self.nodes[0][0].print_first_transition_state())


def make_lineup(pa_transitions, non_pa_transitions):
    constructed_lineup = []
    for lineup_spot in range(1, num_lineup_spots+1):
        final_pa_transitions = []
        final_non_pa_transitions = []
        current_pa_transitions = pa_transitions[np.in1d(pa_transitions[:, 0], lineup_spot)]
        current_non_pa_transitions = non_pa_transitions[np.in1d(non_pa_transitions[:, 0], lineup_spot)]
        for start_state in range(0,num_start_states):
            pa_row = [0] * num_end_states
            non_pa_row = [0] * num_end_states
            pa_for_start_state = current_pa_transitions[np.in1d(current_pa_transitions[:, 1], start_state)]
            non_pa_for_start_state = current_non_pa_transitions[np.in1d(current_non_pa_transitions[:, 1], start_state)]
            for row in pa_for_start_state:
                pa_row[row[2]] = row[3]
            final_pa_transitions.append(pa_row)
            for row in non_pa_for_start_state:
                non_pa_row[row[2]] = row[3]
            final_non_pa_transitions.append(non_pa_row)
        #print(final_pa_transitions)
        constructed_lineup.append(LineupSpot(final_pa_transitions, final_non_pa_transitions))
    return constructed_lineup

def check_valid_home_game(total_runs):
    num_1b = outcome_count["1B"] if outcome_count.has_key("1B") else 0
    num_2b = outcome_count["2B"] if outcome_count.has_key("2B") else 0
    num_3b = outcome_count["3B"] if outcome_count.has_key("3B") else 0
    num_hr = outcome_count["HR"] if outcome_count.has_key("HR") else 0
    num_hit_walk = num_1b + num_2b + num_3b + num_hr
    num_gidp = outcome_count["GIDP"] if outcome_count.has_key("GIDP") else 0
    num_gitp = outcome_count["GITP"] if outcome_count.has_key("GITP") else 0
    num_sb = outcome_count["SB"] if outcome_count.has_key("SB") else 0
    num_cs = outcome_count["CS"] if outcome_count.has_key("CS") else 0

    print("Runs", total_runs, "1B", num_1b, "2B", num_2b, "3B", num_3b, "HR", num_hr, "Hit + walk", num_hit_walk, "GIDP", num_gidp, "GITP", num_gitp, "SB", num_sb, "CS", num_cs)

    if total_runs != 4:
        return False

    if num_1b < 6 or num_1b > 13:
        return False

    if num_2b < 1 or num_2b > 2:
        return False

    if num_3b > 1:
        return False

    if num_hr > 1:
        return False

    if num_hit_walk < 9 or num_hit_walk > 16:
        return False

    if num_gidp > 2:
        return False

    if num_gitp > 0:
        return False

    if num_sb > 1:
        return False

    return True

def check_valid_road_game(total_runs):
    num_1b = outcome_count["1B"] if outcome_count.has_key("1B") else 0
    num_2b = outcome_count["2B"] if outcome_count.has_key("2B") else 0
    num_3b = outcome_count["3B"] if outcome_count.has_key("3B") else 0
    num_hr = outcome_count["HR"] if outcome_count.has_key("HR") else 0
    num_hit_walk = num_1b + num_2b + num_3b + num_hr
    num_gidp = outcome_count["GIDP"] if outcome_count.has_key("GIDP") else 0
    num_gitp = outcome_count["GITP"] if outcome_count.has_key("GITP") else 0
    num_sb = outcome_count["SB"] if outcome_count.has_key("SB") else 0
    num_cs = outcome_count["CS"] if outcome_count.has_key("CS") else 0

    print("Runs", total_runs, "1B", num_1b, "2B", num_2b, "3B", num_3b, "HR", num_hr, "Hit + walk", num_hit_walk, "GIDP", num_gidp, "GITP", num_gitp, "SB", num_sb, "CS", num_cs)

    if total_runs != 3:
        return False

    if num_1b < 6 or num_1b > 12:
        return False

    if num_2b < 1 or num_2b > 2:
        return False

    if num_3b > 1:
        return False

    if num_hr > 1:
        return False

    if num_hit_walk < 8 or num_hit_walk > 15:
        return False

    if num_gidp > 2:
        return False

    if num_gitp > 0:
        return False

    if num_sb > 1:
        return False

    return True


print_box_score = False
print_transitions = True
print_transitions_count = False
print_outcome_count = True
print_inning_number = True
include_non_pa_transitions = True
num_innings = 9

transitions_2013 = np.loadtxt('..\\data\\transitions_by_lineup_spot_2013.csv', delimiter=",", skiprows=1, dtype=int)
non_pa_transitions_2013 = np.loadtxt('..\\data\\non_pa_transitions_by_lineup_spot_2013.csv', delimiter=",", skiprows=1, dtype=int)

lineup = Lineup(make_lineup(transitions_2013, non_pa_transitions_2013))

seeking_home_game = False
seeking_away_game = not seeking_home_game

num_sims = 1

while seeking_home_game or seeking_away_game:
    print ("Simulation number ", num_sims)
    outcome_count = {}
    total_runs = 0.0
    runs_each_inning = []
    innings = []

    for curr_inning in range(1,num_innings+1):
        inning = Inning(lineup, print_transitions, include_non_pa_transitions=include_non_pa_transitions)
        if print_inning_number:
            print("Inning #: ", curr_inning)
        runs_this_inning = inning.simulate_inning()
        total_runs += runs_this_inning
        innings.append(curr_inning)
        runs_each_inning.append(runs_this_inning)

    innings.append("R")
    runs_each_inning.append(sum(runs_each_inning))

    print("average runs ", total_runs/num_innings)
    if print_box_score:
        print(innings)
        print(runs_each_inning)

    if print_transitions_count:
        for key in transitions_made:
            print(key, transitions_made[key])

    if print_outcome_count:
        for key in outcome_count:
            print(key, outcome_count[key])

    if seeking_home_game:
        seeking_home_game = not check_valid_home_game(total_runs)

    if seeking_away_game:
        seeking_away_game = not check_valid_road_game(total_runs)

    num_sims +=1



