"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(50)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    score_lst = []
    if len(hand) > 0:
        for dummy_i in range(1, max(hand)+1):
            temp_score = hand.count(dummy_i) * dummy_i
            score_lst.append(temp_score)
    else:
        return 0
    return max(score_lst)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    # generate possible outcome of each dice position
    dice_outcome = []
    for dummy_i in range(1, num_die_sides+1):
        dice_outcome.append(dummy_i)
    # generate all possible sequences of free dice(s)  
    free_dice_seq = gen_all_sequences(set(dice_outcome), num_free_dice)
    exp_val = 0
    probability = 1.0 / num_die_sides ** num_free_dice
    for sub_seq in free_dice_seq:
        full_seq = list(held_dice) + list(sub_seq)
        exp_val += score(tuple(full_seq)) * probability
    return exp_val


def to_tuple(holds):
    """
    Helper function that convert list to tuple
    eg. [1,2,3] >>> (1,2,3)
    """
    return tuple(holds)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    hand_lst = list(hand)
    powerset = [[]]
    for dice in hand_lst:
        powerset.extend([remained + [dice] for remained in powerset])
    return set(map(to_tuple, powerset))

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    possible_holds = list(gen_all_holds(hand))
    exp_lst = []
    for hold in possible_holds:
        num_free_dice = len(hand) - len(hold)
        exp_val = expected_value(hold, num_die_sides, num_free_dice)
        exp_lst.append(exp_val)
    optimal_val = max(exp_lst)
    optimal_hold = possible_holds[exp_lst.index(optimal_val)]
    return (optimal_val, optimal_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()

#import user35_oGFuhcPNLh_0 as score_testsuite
#score_testsuite.run_suite(score)

#import user35_uLOFnLQSJV29rFh_5 as expected_value_testsuite
#expected_value_testsuite.run_suite(expected_value)

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
        
#import user35_mGREPnDxbs_0 as strategy_testsuite
#strategy_testsuite.run_suite(strategy)
    
    
    



