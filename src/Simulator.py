import math
import random
import csv
import pandas as pd
import numpy as np
import time

transitions_made = {}
base_states = ["000", "100", "020", "120", "003", "103", "023", "123"]
runners = [0, 1, 1, 2, 1, 2, 2, 3]

num_base_states = len(base_states)

class TransitonStates:
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

    def print_node(self, at_bat_number, runs_scored = 0):
        print("At Bat: ", at_bat_number, "base state: ", self.base_state, " num_runners: ", self.num_runners, " outs: ", self.outs)
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
    nodes = []
    states = []

    def __init__(self, df, do_print = True):
        self.do_print = do_print
        for row in df:
            ts = TransitonStates(row,num_base_states)
            self.states.append(ts.transition_states)
        self.create_nodes()
        self.active_node = self.nodes[0][0]

    #Move creation of nodes out of Inning object
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

    def iterate(self, at_bat_of_inning, do_print):
        beginning_node = self.active_node

        next_node = self.active_node.next_node()

        next_row = next_node[0]
        next_col = next_node[1]

        self.active_node = self.nodes[next_row][next_col]

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
            self.active_node.print_node(at_bat_of_inning, runs_scored)

        return runs_scored

    def runners_and_outs(self, current_node):
        return current_node.outs + current_node.num_runners

    def simulate_inning(self):
        inning_runs_scored = 0
        at_bat_of_inning = 1
        if self.do_print:
            self.active_node.print_node(0)

        while self.active_node.outs != 3:
            inning_runs_scored += self.iterate(at_bat_of_inning, self.do_print)
            at_bat_of_inning += 1

        if self.do_print:
            print("Total runs in inning: ", inning_runs_scored)

        return inning_runs_scored

#Fix this so it uses the csv in the project by relative path
x = np.loadtxt('C:\\Data\\transitions_2013.csv', delimiter=",")

num_innings = 10000
total_runs = 0.0
for curr_inning in range(0,num_innings):
    print(curr_inning)
    test = Inning(x, False)
    total_runs += test.simulate_inning()

print("average runs ", total_runs/num_innings)
#for key in transitions_made:
#    print(key, transitions_made[key])




