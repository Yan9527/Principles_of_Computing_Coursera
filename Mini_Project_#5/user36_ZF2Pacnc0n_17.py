"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    lst1 = list(list1)
    for item in lst1:
        while lst1.count(item) != 1:
            lst1.remove(item)
    return lst1

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    for item in list1:
        if item in list2:
            result.append(item)
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    result = []
    lst1 = list(list1)
    lst2 = list(list2)
    while len(lst1) > 0 and len(lst2) >0:
        temp_min = min(lst1[0], lst2[0])
        result.append(temp_min)
        if lst1[0] == temp_min:
            lst1.remove(temp_min)
        else:
            lst2.remove(temp_min)
    result.extend(lst1)
    result.extend(lst2)
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
#    split into 2 lists in the middle
    if len(list1) < 2:
        return list1
    else:
        if len(list1) == 2:
            return [min(list1), max(list1)]
        else:
            split_idx = int(len(list1)/2)
            sub_lst1 = list1[ :split_idx]
            sub_lst2 = list1[split_idx: ]
            merged_lst1 = merge_sort(sub_lst1)
            merged_lst2 = merge_sort(sub_lst2)
            merged_list1 = merge(merged_lst1, merged_lst2)
    return merged_list1

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    elif len(word) == 1:
        return ["", word]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        temp_lst = []
        for item in rest_strings:
            for dummy_i in range(len(item)+1):
                temp_string = item[:dummy_i] + first + item[dummy_i:]
                temp_lst.append(temp_string)
        rest_strings.extend(temp_lst)
        return rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    file_url = codeskulptor.file2url(filename)
    file_opened = urllib2.urlopen(file_url)
    lst = file_opened.readlines()
    result = []
    for item in lst:
        result.append(item.rstrip('\n'))
    return result

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()


