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

transition_state_0 = [0.0255295675198588,	0.235282436010591,	0.0486540158870256,	0,	0.00520741394527802,	0,	0,	0,	0.685326566637246,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]
transition_state_1 = [0.0234638911713686,	0.000456495937186159,	0.0751392312608418,	0.18898931799507,	0.00986031224322103,	0.0370674700995161,	0.0315895188532822,	0,	0.0233725919839313,	0.398703551538391,	0.099242216744271,	0,	0.00337806993517758,	0,	0,	0,	0.108737332237743,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]
transition_state_2 = [0.021600243383024,	0.0520231213872832,	0.0432004867660481,	0.103742013994524,	0.0334651658046851,	0.0921813203529054,	0.00638880438089443,	0,	0.00669303316093702,	0.0127776087617889,	0.36264070581077,	0,	0.259507149376331,	0,	0,	0,	0.00578034682080925,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]
transition_state_3 = [0.0193021529324425,	0.000371195248700817,	0.010022271714922,	0.0397178916109874,	0.0044543429844098,	0.0319227913882702,	0.0597624350408315,	0.153303637713437,	0.00185597624350408,	0.00705270972531552,	0.00371195248700817,	0.338158871566444,	0.00148478099480327,	0.0920564216778025,	0.125463994060876,	0,	0,	0.00965107646622123,	0.0115070527097253,	0,	0.0887156644394952,	0,	0,	0,	0.00148478099480327,	0,	0,	0]
transition_state_4 = [0.0245901639344262,	0.168032786885246,	0.040983606557377,	0,	0,	0.114754098360656,	0,	0,	0.241803278688525,	0.00409836065573771,	0.00819672131147541,	0,	0.389344262295082,	0,	0,	0,	0.00819672131147541,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]
transition_state_5 = [0.0279214064115822,	0.0031023784901758,	0.0361944157187177,	0.148914167528438,	0.00723888314374354,	0.0341261633919338,	0.0858324715615305,	0.0682523267838676,	0.00103412616339193,	0.164426059979317,	0.0558428128231644,	0.0165460186142709,	0.0062047569803516,	0.210961737331955,	0.0372285418821096,	0,	0.0858324715615305,	0.00103412616339193,	0.00206825232678387,	0,	0.0062047569803516,	0,	0,	0,	0.00103412616339193,	0,	0,	0]
transition_state_6 = [0.00924499229583975,	0.0508474576271186,	0.0431432973805855,	0.00770416024653313,	0.0169491525423729,	0.0955315870570108,	0.00924499229583975,	0.13713405238829,	0.00154083204930663,	0.0061633281972265,	0.098613251155624,	0.00462249614791988,	0.149460708782743,	0.0107858243451464,	0.352850539291217,	0,	0,	0,	0.00462249614791988,	0,	0.00154083204930663,	0,	0,	0,	0,	0,	0,	0]
transition_state_7 = [0.0193164933135215,	0.00148588410104012,	0.0163447251114413,	0.0520059435364042,	0.00594353640416048,	0.0312035661218425,	0.0490341753343239,	0.163447251114413,	0,	0.00297176820208024,	0,	0.0638930163447251,	0,	0.0906389301634472,	0.0430906389301634,	0.340267459138187,	0,	0.00594353640416048,	0.00297176820208024,	0.00297176820208024,	0.0668647845468053,	0.00445765230312036,	0.0356612184249629,	0,	0.00148588410104012,	0,	0,	0]
transition_state_8 = [0,	0,	0,	0,	0,	0,	0,	0,	0.0211522658794169,	0.2340140609307,	0.048148035426241,	0,	0.00538697994339106,	0,	0,	0,	0.691298657820251,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]
transition_state_9 = [0,	0,	0,	0,	0,	0,	0,	0,	0.0237217871948411,	0.000998003992015968,	0.0859051128512206,	0.178335636419469,	0.0100568094580071,	0.0389221556886228,	0.0275602640872102,	7.67695378473822E-05,	0.0240288653462306,	0.420082911100875,	0.0766927683095348,	0,	0.00284047290035314,	0,	0,	0,	0.110778443113772,	0,	0,	0]
transition_state_10	= [0,	0,	0,	0,	0,	0,	0,	0,	0.0248425472358293,	0.0547585724282715,	0.0502099370188943,	0.131210636808957,	0.0474107767669699,	0.0622813156053184,	0.00174947515745276,	0,	0.0148705388383485,	0.0118964310706788,	0.410251924422673,	0,	0.181945416375087,	0,	0,	0,	0.00857242827151854,	0,	0,	0]
transition_state_11	= [0,	0,	0,	0,	0,	0,	0,	0,	0.0240728692257645,	0,	0.0158317067881154,	0.0487963565387118,	0.00585556278464541,	0.038169594448059,	0.0665799175883756,	0.140099761440035,	0.000867490782910432,	0.00672305356755584,	0.00954239861201475,	0.357406202559098,	0.00216872695727608,	0.0897852960312297,	0.0707004988072002,	0,	0.123183691173281,	0.000216872695727608,	0,	0]
transition_state_12	= [0,	0,	0,	0,	0,	0,	0,	0,	0.0337078651685393,	0.172284644194757,	0.0492241840556447,	0,	0.00695559122525415,	0.153558052434457,	0,	0,	0.203852327447833,	0.023542001070091,	0.00374531835205993,	0,	0.345104333868379,	0,	0,	0,	0.00802568218298555,	0,	0,	0]
transition_state_13	= [0,	0,	0,	0,	0,	0,	0,	0,	0.0190294957183635,	0.000475737392959087,	0.0266412940057088,	0.126070409134158,	0.010941960038059,	0.0371075166508088,	0.0813510941960038,	0.0742150333016175,	0.00285442435775452,	0.158420551855376,	0.049476688867745,	0.0228353948620362,	0.00903901046622265,	0.236441484300666,	0.027592768791627,	0,	0.115128449096099,	0.00237868696479543,	0,	0]
transition_state_14	= [0,	0,	0,	0,	0,	0,	0,	0,	0.0146683673469388,	0.0714285714285714,	0.0503826530612245,	0.00829081632653061,	0.017219387755102,	0.0809948979591837,	0.00255102040816327,	0.200255102040816,	0.00127551020408163,	0.00510204081632653,	0.0880102040816327,	0.0076530612244898,	0.14859693877551,	0.0223214285714286,	0.26594387755102,	0,	0.0133928571428571,	0.00191326530612245,	0,	0]
transition_state_15	= [0,	0,	0,	0,	0,	0,	0,	0,	0.0214646464646465,	0,	0.014520202020202,	0.0492424242424242,	0.00883838383838384,	0.0359848484848485,	0.0542929292929293,	0.158459595959596,	0,	0.00694444444444444,	0.00315656565656566,	0.0707070707070707,	0.00126262626262626,	0.0965909090909091,	0.0492424242424242,	0.298611111111111,	0.125,	0.00568181818181818,	0,	0]
transition_state_16	= [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.0218124664571034,	0.236487004523499,	0.0441232845204324,	0,	0.00456183393391091,	0,	0,	0,	0.693015410565054,	0,	0,	0]
transition_state_17	= [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.0214899713467049,	0.000904840898808626,	0.111974061227567,	0.164002412909063,	0.0103302669280651,	0.0447142210827929,	0.0187000452420449,	0,	0.627356356507314,	0.000527823857638365,	0,	0]
transition_state_18	= [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.0164942689404529,	0.0817724350013978,	0.050041934582052,	0.149846239865809,	0.0398378529493989,	0.0301928990774392,	0.000419345820519989,	0,	0.627341347497903,	0.00405367626502656,	0,	0]
transition_state_19	= [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.0206458443620963,	0.000882301041115229,	0.023116287277219,	0.050114699135345,	0.00564672666313746,	0.0492323980942298,	0.0545262043409211,	0.109934709722957,	0.67901888124228,	0.00582318687136051,	0.00105876124933827,	0]
transition_state_20	= [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.0368223661779748,	0.13126491646778,	0.0470508012274122,	0,	0.00409137401977497,	0.147289464711899,	0,	0,	0.632117286055234,	0.00136379133992499,	0,	0]
transition_state_21	= [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.0147783251231527,	0.00211118930330753,	0.0369458128078818,	0.08972554539057,	0.00668543279380718,	0.0387051372273047,	0.0999296270232231,	0.0805770584095707,	0.625263898662913,	0.00422237860661506,	0.00105559465165376,	0]
transition_state_22	= [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.0187121629058888,	0.0671436433681893,	0.0429279031370391,	0.000550357732526142,	0.0176114474408365,	0.0275178866263071,	0,	0.181618051733627,	0.638965327462851,	0.00220143093010457,	0.00275178866263071,	0]
transition_state_23 = [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0.020463112547119,	0.00107700592353258,	0.0215401184706516,	0.0414647280560043,	0.0113085621970921,	0.0376952073236403,	0.0403877221324717,	0.113624124932687,	0.705977382875606,	0.00323101777059774,	0.00323101777059774,	0]


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
    def __init__(self, base_state, num_runners, outs, transition_states, three_out_runs = 0):
        self.base_state = base_state
        self.num_runners = num_runners
        self.outs = outs
        self.transition_states = transition_states
        self.three_out_runs = three_out_runs

    def print_node(self, at_bat_number, runs_scored = 0):
        print("At Bat: ", at_bat_number, "base state: ", self.base_state, " num_runners: ", self.num_runners, " outs: ", self.outs)
        if runs_scored > 0:
            print("Runs Scored: ", runs_scored)

    def next_node(self):
        r = random.random()
        #print("r: ", r)
        row = 0
        #print(self.transition_states)
        for i in self.transition_states:
            col = 0
            for j in i:
                #print(row, col)
                if r < self.transition_states[row][col]:
                    return (row,col)
                else:
                    col += 1
            row += 1

    def determine_base_out_code(self, outs, base_state_cd, runs_scored = 0):
        if outs == 3:
            if runs_scored == 0:
                return 24
            elif runs_scored == 1:
                return 25
            elif runs_scored == 2:
                return 26
            else:
                return 27
        else:
            return (outs * 7) + base_state_cd



class World:
    states_0 = TransitonStates(transition_state_0, 8).transition_states
    states_1 = TransitonStates(transition_state_1, 8).transition_states
    states_2 = TransitonStates(transition_state_2, 8).transition_states
    states_3 = TransitonStates(transition_state_3, 8).transition_states
    states_4 = TransitonStates(transition_state_4, 8).transition_states
    states_5 = TransitonStates(transition_state_5, 8).transition_states
    states_6 = TransitonStates(transition_state_6, 8).transition_states
    states_7 = TransitonStates(transition_state_7, 8).transition_states
    states_8 = TransitonStates(transition_state_8, 8).transition_states
    states_9 = TransitonStates(transition_state_9, 8).transition_states
    states_10 = TransitonStates(transition_state_10, 8).transition_states
    states_11 = TransitonStates(transition_state_11, 8).transition_states
    states_12 = TransitonStates(transition_state_12, 8).transition_states
    states_13 = TransitonStates(transition_state_13, 8).transition_states
    states_14 = TransitonStates(transition_state_14, 8).transition_states
    states_15 = TransitonStates(transition_state_15, 8).transition_states
    states_16 = TransitonStates(transition_state_16, 8).transition_states
    states_17 = TransitonStates(transition_state_17, 8).transition_states
    states_18 = TransitonStates(transition_state_18, 8).transition_states
    states_19 = TransitonStates(transition_state_19, 8).transition_states
    states_20 = TransitonStates(transition_state_20, 8).transition_states
    states_21 = TransitonStates(transition_state_21, 8).transition_states
    states_22 = TransitonStates(transition_state_22, 8).transition_states
    states_23 = TransitonStates(transition_state_23, 8).transition_states

    no_outs_bases_empty = Node(base_state=bases_empty, num_runners=0, outs=0, transition_states=states_0)
    no_outs_man_on_first = Node(base_state=man_on_first, num_runners=1, outs=0, transition_states=states_1)
    no_outs_man_on_second = Node(base_state=man_on_second, num_runners=1, outs=0, transition_states=states_2)
    no_outs_men_on_first_second = Node(base_state=men_on_first_second, num_runners=2, outs=0, transition_states=states_3)
    no_outs_man_on_third = Node(base_state=man_on_third, num_runners=1, outs=0, transition_states=states_4)
    no_outs_men_on_first_third = Node(base_state=men_on_first_third, num_runners=2, outs=0, transition_states=states_5)
    no_outs_men_on_second_third = Node(base_state=men_on_second_third, num_runners=2, outs=0, transition_states=states_6)
    no_outs_bases_loaded = Node(base_state=bases_loaded, num_runners=3, outs=0, transition_states=states_7)

    one_out_bases_empty = Node(base_state=bases_empty, num_runners=0, outs=1, transition_states=states_8)
    one_out_man_on_first = Node(base_state=man_on_first, num_runners=1, outs=1, transition_states=states_9)
    one_out_man_on_second = Node(base_state=man_on_second, num_runners=1, outs=1, transition_states=states_10)
    one_out_men_on_first_second = Node(base_state=men_on_first_second, num_runners=2, outs=1, transition_states=states_11)
    one_out_man_on_third = Node(base_state=man_on_third, num_runners=1, outs=1, transition_states=states_12)
    one_out_men_on_first_third = Node(base_state=men_on_first_third, num_runners=2, outs=1, transition_states=states_13)
    one_out_men_on_second_third = Node(base_state=men_on_second_third, num_runners=2, outs=1, transition_states=states_14)
    one_out_bases_loaded = Node(base_state=bases_loaded, num_runners=3, outs=1, transition_states=states_15)
    
    two_outs_bases_empty = Node(base_state=bases_empty, num_runners=0, outs=2, transition_states=states_16)
    two_outs_man_on_first = Node(base_state=man_on_first, num_runners=1, outs=2, transition_states=states_17)
    two_outs_man_on_second = Node(base_state=man_on_second, num_runners=1, outs=2, transition_states=states_18)
    two_outs_men_on_first_second = Node(base_state=men_on_first_second, num_runners=2, outs=2, transition_states=states_19)
    two_outs_man_on_third = Node(base_state=man_on_third, num_runners=1, outs=2, transition_states=states_20)
    two_outs_men_on_first_third = Node(base_state=men_on_first_third, num_runners=2, outs=2, transition_states=states_21)
    two_outs_men_on_second_third = Node(base_state=men_on_second_third, num_runners=2, outs=2, transition_states=states_22)
    two_outs_bases_loaded = Node(base_state=bases_loaded, num_runners=3, outs=2, transition_states=states_23)

    three_outs_no_runs = Node(base_state=bases_empty, num_runners=0, outs=3, transition_states=states_0, three_out_runs=0)
    three_outs_one_run = Node(base_state=bases_empty, num_runners=0, outs=3, transition_states=states_0, three_out_runs=1)
    three_outs_two_runs = Node(base_state=bases_empty, num_runners=0, outs=3, transition_states=states_0, three_out_runs=2)
    three_outs_three_runs = Node(base_state=bases_empty, num_runners=0, outs=3, transition_states=states_0, three_out_runs=3)

    base_out_states = []
    no_outs_states = [no_outs_bases_empty, no_outs_man_on_first, no_outs_man_on_second, no_outs_men_on_first_second,
                      no_outs_man_on_third, no_outs_men_on_first_third, no_outs_men_on_second_third,
                      no_outs_bases_loaded]
    base_out_states.append(no_outs_states)

    one_out_states = [one_out_bases_empty, one_out_man_on_first, one_out_man_on_second, one_out_men_on_first_second,
                      one_out_man_on_third, one_out_men_on_first_third, one_out_men_on_second_third,
                      one_out_bases_loaded]

    base_out_states.append(one_out_states)
    
    two_out_states = [two_outs_bases_empty, two_outs_man_on_first, two_outs_man_on_second, two_outs_men_on_first_second,
                      two_outs_man_on_third, two_outs_men_on_first_third, two_outs_men_on_second_third,
                      two_outs_bases_loaded]

    base_out_states.append(two_out_states)

    three_out_states = [three_outs_no_runs, three_outs_one_run, three_outs_two_runs, three_outs_three_runs]

    base_out_states.append(three_out_states)

    def __init__(self):
        self.active_node = self.no_outs_bases_empty

    def iterate(self, at_bat_of_inning):
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

        self.active_node.print_node(at_bat_of_inning, runs_scored)

        return runs_scored

    def runners_and_outs(self, current_node):
        return current_node.outs + current_node.num_runners

test = World()
test.active_node.print_node(0)

inning_runs_scored = 0

at_bat_of_inning = 1
while test.active_node.outs != 3:
    inning_runs_scored += test.iterate(at_bat_of_inning)
    at_bat_of_inning += 1

print("Total runs in inning: ", inning_runs_scored)




