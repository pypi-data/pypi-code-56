"""
This file contains the main logic for the RandomList class and
the helper functions it uses
"""

import typing as t
import random
from copy import deepcopy

# ------------------------------------------------- #
#                        Helpers                    #
# ------------------------------------------------- #


def format_list(input_list: t.List[t.Any]) -> t.List[t.Dict]:
    '''
    Given a list, for each item, adds a "probability" of 1 if key isn't present,
    then sorts list by probability value
    '''
    formatted_list = []
    for item in input_list:
        if isinstance(item, dict) and "probability" in item and "item" in item:
            formatted_list.append(item)
        else:
            new_item = {
                "item": item,
                "probability": 1
            }
            formatted_list.append(new_item)
    return sorted(formatted_list, key=lambda k: k['probability'], reverse=True)


def format_list_probabilities(input_list: t.List[t.Dict]) -> t.List[t.Dict]:
    '''
    Given a formatted list, formats it (again) so the probabilities are cumulatively weighed
    Ex: Given items with probabilties of 10 and 20, it will return items
    with probabilities of 10 and 30 (10+20).
    '''
    cumulative_probability = 0
    new_list = []
    for item in input_list:
        new_item = item.copy()
        cumulative_probability += new_item["probability"]
        new_item["probability"] = cumulative_probability
        new_list.append(new_item)
    return new_list


def get_from_list(target: int, input_list: t.List[t.Dict]) -> t.Dict:
    '''
    Given a "target", returns the first item in formatted list with a greater probability
    Ex: Item A has a probability of 20 and Item B has 50. Our target is 32, so we return Item B.
    '''
    for item in input_list:
        if target <= item["probability"]:
            return item
    raise IndexError(f'Nothing found in list matching probability value of {target}.')


def deepcopy_list(input_list: t.List[t.Dict]) -> t.List[t.Dict]:
    '''
    Returns a deepcopy of a list of dictionaries
    '''
    new_list = []
    for dict_item in input_list:
        new_dict = deepcopy(dict_item)
        new_list.append(new_dict)
    return new_list

# ------------------------------------------------- #
#                        Class                      #
# ------------------------------------------------- #


class RandomList:
    '''
    A class for getting random results from a list.

    Items in this list can either given in the following format:
        {
            "item": (the actual thing you want),
            "probability": (an int representing the comparative probability)
        }

    If given in any other format, items will be auto-formatted and provided
    a probability of 1.
    '''

    def __init__(self, input_list: t.List[t.Any]):
        self._contents = format_list(deepcopy_list(input_list))
        self._offset_contents = format_list_probabilities(self._contents)
        self._original_contents = deepcopy_list(self._contents)

    def _get_item_index(self, input_item: t.Any):
        for item in self._contents:
            if item["item"] == input_item:
                return self._contents.index(item)
        raise IndexError(f'Could not find index of list item {input_item}.')

    def _adjust_probability(self, target_item: t.Dict, adjustment_amount: int):
        target_index = self._get_item_index(target_item)
        self._contents[target_index]["probability"] += adjustment_amount
        # Remove from list if prob becomes 0
        if self._contents[target_index]["probability"] <= 0:
            del self._contents[target_index]
        self._offset_contents = format_list_probabilities(self._contents)

    def _get_random_probability(self):
        range_max = self._offset_contents[-1]["probability"]
        return random.randint(1, range_max)

    def get_random(self):
        '''
        Returns a random item from self._contents
        '''
        if len(self._contents) == 0:
            raise IndexError('RandomList is empty!')
        target_probability = self._get_random_probability()
        return get_from_list(target_probability, self._offset_contents)["item"]

    def get_random_and_remove(self):
        '''
        Returns a random item from self._contents and decreases its probability by 1
        If its probability reaches 0, it is removed from the list
        '''
        if len(self._contents) == 0:
            raise IndexError('RandomList is empty!')
        target_probability = self._get_random_probability()
        random_item = get_from_list(target_probability, self._offset_contents)["item"]
        self._adjust_probability(random_item, -1)
        return random_item

    def reset_contents(self):
        '''
        Returns contents to their original state, resetting all probability values
        and replacing any removed items
        '''
        self._contents = self._original_contents
        self._offset_contents = format_list_probabilities(self._contents)

    def get_items(self):
        '''
        Returns a list of all possible items in RandomList
        '''
        return [item["item"] for item in self._contents]

    def get_contents(self):
        '''
        Returns the contents of the RandomList
        '''
        return self._contents

    def item_count(self):
        '''
        Returns the number of items in self._contents
        '''
        return len(self._contents)

class RandomGroup:
    '''
    Very much like a RandomList, except it's a collection of RandomLists. They can
    be given comparative probabilities like follows:

        {
            "item": (your RandomList),
            "probability": (an int representing the comparative probability)
        }

    Otherwise the RandomLists will be auto-formatted and each given a probability of 1.
    '''

    def __init__(self, input_lists: t.List[t.Type[RandomList]]):
        self._lists = format_list(input_lists)
        self._offset_lists = format_list_probabilities(self._lists)
        self._original_lists = deepcopy_list(self._lists)

    def _get_random_probability(self):
        range_max = self._offset_lists[-1]["probability"]
        return random.randint(1, range_max)

    def get_random(self):
        '''
        Selects a RandomList from self._lists, then returns a random item from its contents
        by calling the RandomList's own get_random() method
        '''
        if len(self._lists) == 0:
            raise IndexError('RandomGroup is empty!')
        target_probability = self._get_random_probability()
        random_list = get_from_list(target_probability, self._offset_lists)["item"]
        return random_list.get_random()

    def get_list_items(self):
        '''
        For each list in self._lists, returns a list of its items
        '''
        return [random_list["item"].get_items() for random_list in self._lists]

    def get_contents(self):
        '''
        For each list in self._lists, returns a full list of its contents, along with the
        list's probability
        '''
        return [
            {
                "item": random_list["item"].get_contents(),
                "probability": random_list["probability"]
            }
            for random_list in self._lists
        ]

