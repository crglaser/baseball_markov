import math
import random
import csv
import pandas as pd
import numpy as np


transitions_made = {}
base_states = ["000", "100", "020", "120", "003", "103", "023", "123"]
runners = [0, 1, 1, 2, 1, 2, 2, 3]

num_base_states = len(base_states)


class TransitionStates:
    def __init__(self, states, row_length):
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
        self.transition_states.append(current_row)

    def print_states(self):
        for i in self.transition_states:
            print(i)


class Node:
    def __init__(self, base_state_number, outs, transition_states):
        self.base_state_number = base_state_number
        self.base_state = base_states[base_state_number]
        self.num_runners = runners[base_state_number]
        self.outs = outs
        self.transition_states = transition_states
        self.three_out_runs = base_state_number

    def node_number(self):
        return self.outs*8 + self.base_state_number

    def print_node(self, at_bat_number, runs_scored = 0, lineup_spot = 1):
        print("Lineup Spot:", lineup_spot, " Inning At Bat: ", at_bat_number + 1, "base state: ", self.base_state, " num_runners: ", self.num_runners, " outs: ", self.outs)
        if runs_scored > 0:
            print("Runs Scored: ", runs_scored)

    def next_node(self):
        r = random.random()
        row = 0
        for i in self.transition_states:
            col = 0
            for j in i:
                if r < self.transition_states[row][col]:
                    return (row,col)
                else:
                    col += 1
            row += 1


class Inning:
    def __init__(self, lineup, do_print=True):
        self.lineup = lineup
        self.active_node = lineup.lineup_spot().nodes[0][0]
        self.do_print = do_print

    def iterate_inning(self, at_bat_of_inning, do_print):
        beginning_node = self.active_node

        next_node = self.active_node.next_node()

        next_row = next_node[0]
        next_col = next_node[1]

        self.active_node = self.lineup.lineup_spot().nodes[next_row][next_col]
        self.lineup.iterate_lineup()

        key = str(beginning_node.node_number()) + " " + str(self.active_node.node_number())
        if transitions_made.has_key(key):
            transitions_made[key] += 1
        else:
            transitions_made[key] = 1

        start_runners_and_outs = self.runners_and_outs(beginning_node)
        end_runners_and_outs = self.runners_and_outs(self.active_node)

        runs_scored = 0
        if self.active_node.outs == 3:
            runs_scored = self.active_node.three_out_runs
        elif end_runners_and_outs < 1 + start_runners_and_outs:
            runs_scored = start_runners_and_outs + 1 - end_runners_and_outs

        if do_print:
            self.active_node.print_node(at_bat_of_inning, runs_scored, lineup_spot=self.lineup.current_spot + 1)

        return runs_scored

    def runners_and_outs(self, current_node):
        return current_node.outs + current_node.num_runners

    def simulate_inning(self):
        self.active_node = self.lineup.lineup_spot().nodes[0][0]
        inning_runs_scored = 0
        at_bat_of_inning = 1

        if self.do_print:
            self.active_node.print_node(0,lineup_spot=self.lineup.current_spot+1)

        while self.active_node.outs != 3:
            inning_runs_scored += self.iterate_inning(at_bat_of_inning, self.do_print)
            at_bat_of_inning += 1

        self.lineup.iterate_lineup()

        if self.do_print:
            print("Total runs in inning: ", inning_runs_scored)

        return inning_runs_scored


class Lineup:
    def __init__(self, lineup_spots):
        self.lineup_spots = lineup_spots
        self.num_spots = len(lineup_spots)
        self.current_spot = 0

    def lineup_spot(self):
        return self.lineup_spots[self.current_spot]

    def iterate_lineup(self):
        self.current_spot += 1
        if self.current_spot == self.num_spots:
            self.current_spot = 0


class LineupSpot:
    nodes = []
    states = []

    def __init__(self, transitions):
        for row in transitions:
            ts = TransitionStates(row, num_base_states)
            self.states.append(ts.transition_states)
        self.create_nodes()

    def create_nodes(self):
        for outs in range(0, 3):
            out_nodes = []
            for state in range(0,num_base_states):
                out_nodes.append(Node(state, outs, self.states[outs*8 + state]))
            self.nodes.append(out_nodes)
        three_out_nodes = []
        for state in range(0,4):
            three_out_nodes.append(Node(state, 3, self.states[0]))
        self.nodes.append(three_out_nodes)


def count_to_prob(row):
    total = row.sum()
    new_row = [a/total for a in row]
    return new_row


def counts_to_probabilities(transition_counts):
    perc = np.apply_along_axis(count_to_prob, axis=1, arr=transition_counts)
    return perc

file_transitions = np.loadtxt('..\\data\\transitions_2013.csv', delimiter=",")
transitions_raw_ls_1 = np.loadtxt('..\\data\\transitions_raw_ls_1.csv', delimiter=",")
transitions_raw_ls_2 = np.loadtxt('..\\data\\transitions_raw_ls_2.csv', delimiter=",")
transitions_raw_ls_3 = np.loadtxt('..\\data\\transitions_raw_ls_3.csv', delimiter=",")
transitions_raw_ls_4 = np.loadtxt('..\\data\\transitions_raw_ls_4.csv', delimiter=",")
transitions_raw_ls_5 = np.loadtxt('..\\data\\transitions_raw_ls_5.csv', delimiter=",")
transitions_raw_ls_6 = np.loadtxt('..\\data\\transitions_raw_ls_6.csv', delimiter=",")
transitions_raw_ls_7 = np.loadtxt('..\\data\\transitions_raw_ls_7.csv', delimiter=",")
transitions_raw_ls_8 = np.loadtxt('..\\data\\transitions_raw_ls_8.csv', delimiter=",")
transitions_raw_ls_9 = np.loadtxt('..\\data\\transitions_raw_ls_9.csv', delimiter=",")

transitions_ls_1 = counts_to_probabilities(transitions_raw_ls_1)
transitions_ls_2 = counts_to_probabilities(transitions_raw_ls_2)
transitions_ls_3 = counts_to_probabilities(transitions_raw_ls_3)
transitions_ls_4 = counts_to_probabilities(transitions_raw_ls_4)
transitions_ls_5 = counts_to_probabilities(transitions_raw_ls_5)
transitions_ls_6 = counts_to_probabilities(transitions_raw_ls_6)
transitions_ls_7 = counts_to_probabilities(transitions_raw_ls_7)
transitions_ls_8 = counts_to_probabilities(transitions_raw_ls_8)
transitions_ls_9 = counts_to_probabilities(transitions_raw_ls_9)

print_box_score = False
print_transitions = True
print_transitions_count = False
print_inning_number = True
num_innings = 9
total_runs = 0.0
runs_each_inning = []
innings = []

lineup_spots = []

lineup_spot_1 = LineupSpot(transitions_ls_1)
lineup_spot_2 = LineupSpot(transitions_ls_2)
lineup_spot_3 = LineupSpot(transitions_ls_3)
lineup_spot_4 = LineupSpot(transitions_ls_4)
lineup_spot_5 = LineupSpot(transitions_ls_5)
lineup_spot_6 = LineupSpot(transitions_ls_6)
lineup_spot_7 = LineupSpot(transitions_ls_7)
lineup_spot_8 = LineupSpot(transitions_ls_8)
lineup_spot_9 = LineupSpot(transitions_ls_9)

lineup_spots.append(lineup_spot_1)
lineup_spots.append(lineup_spot_2)
lineup_spots.append(lineup_spot_3)
lineup_spots.append(lineup_spot_4)
lineup_spots.append(lineup_spot_5)
lineup_spots.append(lineup_spot_6)
lineup_spots.append(lineup_spot_7)
lineup_spots.append(lineup_spot_8)
lineup_spots.append(lineup_spot_9)

lineup = Lineup(lineup_spots)

for curr_inning in range(1,num_innings+1):
    inning = Inning(lineup, print_transitions)
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




