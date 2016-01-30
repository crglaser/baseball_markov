import math
import random

bases_empty = "000"
man_on_first = "100"
man_on_second = "020"
man_on_third = "003"
men_on_first_second = "120"
men_on_first_third = "103"
men_on_second_third = "023"
bases_loaded = "123"

#test_states = [[.035, .07, .105, .14, .175, .21, .245, .28],
#               [.315, .35, .385, .42, .455, .49, .525, .56],
#               [.595, .63, .665, .70, .735, .77, .805, .84],
#               [.875, .91, .945, 1, -1, -1, -1, -1]]

test_state_vector = [.035, .07, .105, .14, .175, .21, .245, .28,
                     .315, .35, .385, .42, .455, .49, .525, .56,
                     .595, .63, .665, .70, .735, .77, .805, .84,
                     .875, .91, .945, 1, -1, -1, -1, -1]

class TransitonStates:
    def __init__(self, states, row_length):
        self.transition_states = []
        row_element = 0
        current_row = []
        for i in states:
            current_row.append(i)
            row_element += 1
            if row_element >= row_length:
                self.transition_states.append(current_row)
                current_row = []
                row_element = 0

    def print_states(self):
        for i in self.transition_states:
            print(i)

class Node:
    def __init__(self, base_state, num_runners, outs, transition_states, three_out_runs = 0):
        self.base_state = base_state
        self.num_runners = num_runners
        self.outs = outs
        self.transition_states = transition_states
        self.three_out_runs = three_out_runs

    def print_node(self):
        print("base state: ", self.base_state, " num_runners: ", self.num_runners, " outs: ", self.outs)
        if self.outs == 3:
            print("three_out_runs: ", self.three_out_runs)

    def next_node(self):
        r = random.random()
        #print("r: ", r)
        row = 0
        for i in self.transition_states:
            col = 0
            for j in i:
                #print(row, col)
                if r < self.transition_states[row][col]:
                    return (row,col)
                else:
                    col += 1
            row += 1

class World:
    trans_states = TransitonStates(test_state_vector,8)
    test_states = trans_states.transition_states

    no_outs_bases_empty = Node(base_state=bases_empty, num_runners=0, outs=0, transition_states=test_states)
    no_outs_man_on_first = Node(base_state=man_on_first, num_runners=1, outs=0, transition_states=test_states)
    no_outs_man_on_second = Node(base_state=man_on_second, num_runners=1, outs=0, transition_states=test_states)
    no_outs_man_on_third = Node(base_state=man_on_third, num_runners=1, outs=0, transition_states=test_states)
    no_outs_men_on_first_second = Node(base_state=men_on_first_second, num_runners=2, outs=0, transition_states=test_states)
    no_outs_men_on_first_third = Node(base_state=men_on_first_third, num_runners=2, outs=0, transition_states=test_states)
    no_outs_men_on_second_third = Node(base_state=men_on_second_third, num_runners=2, outs=0, transition_states=test_states)
    no_outs_bases_loaded = Node(base_state=bases_loaded, num_runners=3, outs=0, transition_states=test_states)

    one_out_bases_empty = Node(base_state=bases_empty, num_runners=0, outs=1, transition_states=test_states)
    one_out_man_on_first = Node(base_state=man_on_first, num_runners=1, outs=1, transition_states=test_states)
    one_out_man_on_second = Node(base_state=man_on_second, num_runners=1, outs=1, transition_states=test_states)
    one_out_man_on_third = Node(base_state=man_on_third, num_runners=1, outs=1, transition_states=test_states)
    one_out_men_on_first_second = Node(base_state=men_on_first_second, num_runners=2, outs=1, transition_states=test_states)
    one_out_men_on_first_third = Node(base_state=men_on_first_third, num_runners=2, outs=1, transition_states=test_states)
    one_out_men_on_second_third = Node(base_state=men_on_second_third, num_runners=2, outs=1, transition_states=test_states)
    one_out_bases_loaded = Node(base_state=bases_loaded, num_runners=3, outs=1, transition_states=test_states)
    
    two_outs_bases_empty = Node(base_state=bases_empty, num_runners=0, outs=2, transition_states=test_states)
    two_outs_man_on_first = Node(base_state=man_on_first, num_runners=1, outs=2, transition_states=test_states)
    two_outs_man_on_second = Node(base_state=man_on_second, num_runners=1, outs=2, transition_states=test_states)
    two_outs_man_on_third = Node(base_state=man_on_third, num_runners=1, outs=2, transition_states=test_states)
    two_outs_men_on_first_second = Node(base_state=men_on_first_second, num_runners=2, outs=2, transition_states=test_states)
    two_outs_men_on_first_third = Node(base_state=men_on_first_third, num_runners=2, outs=2, transition_states=test_states)
    two_outs_men_on_second_third = Node(base_state=men_on_second_third, num_runners=2, outs=2, transition_states=test_states)
    two_outs_bases_loaded = Node(base_state=bases_loaded, num_runners=3, outs=2, transition_states=test_states)

    three_outs_no_runs = Node(base_state=bases_empty, num_runners=0, outs=3, transition_states=test_states, three_out_runs=0)
    three_outs_one_run = Node(base_state=bases_empty, num_runners=0, outs=3, transition_states=test_states, three_out_runs=1)
    three_outs_two_runs = Node(base_state=bases_empty, num_runners=0, outs=3, transition_states=test_states, three_out_runs=2)
    three_outs_three_runs = Node(base_state=bases_empty, num_runners=0, outs=3, transition_states=test_states, three_out_runs=3)

    base_out_states = []
    no_outs_states = [no_outs_bases_empty, no_outs_man_on_first, no_outs_man_on_second, no_outs_man_on_third,
                      no_outs_men_on_first_second, no_outs_men_on_first_third, no_outs_men_on_second_third,
                      no_outs_bases_loaded]
    base_out_states.append(no_outs_states)

    one_out_states = [one_out_bases_empty, one_out_man_on_first, one_out_man_on_second, one_out_man_on_third,
                      one_out_men_on_first_second, one_out_men_on_first_third, one_out_men_on_second_third,
                      one_out_bases_loaded]

    base_out_states.append(one_out_states)
    
    two_out_states = [two_outs_bases_empty, two_outs_man_on_first, two_outs_man_on_second, two_outs_man_on_third,
                      two_outs_men_on_first_second, two_outs_men_on_first_third, two_outs_men_on_second_third,
                      two_outs_bases_loaded]

    base_out_states.append(two_out_states)

    three_out_states = [three_outs_no_runs, three_outs_one_run, three_outs_two_runs, three_outs_three_runs]

    base_out_states.append(three_out_states)

    def __init__(self):
        self.active_node = self.no_outs_bases_empty

    def iterate(self):
        beginning_node = self.active_node

        next_node = self.active_node.next_node()
        #print "next_node: ", next_node

        next_row = next_node[0]
        next_col = next_node[1]

        #print ("row: ", next_row, " col: ", next_col)

        self.active_node = self.base_out_states[next_row][next_col]

        start_runners_and_outs = self.runners_and_outs(beginning_node)
        end_runners_and_outs = self.runners_and_outs(self.active_node)

        runs_scored = 0
        if self.active_node.outs == 3:
            runs_scored = self.active_node.three_out_runs
        elif end_runners_and_outs < 1 + start_runners_and_outs:
            runs_scored = start_runners_and_outs + 1 - end_runners_and_outs

        print("Start: ", start_runners_and_outs, " End: ", end_runners_and_outs, " Runs: ", runs_scored)
        self.active_node.print_node()

        return runs_scored

    def runners_and_outs(self, current_node):
        return current_node.outs + current_node.num_runners

test = World()
test.active_node.print_node()

inning_runs_scored = 0

while test.active_node.outs != 3:
    inning_runs_scored += test.iterate()
    print(inning_runs_scored)




