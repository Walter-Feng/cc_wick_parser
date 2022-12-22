import itertools
import copy
import math
import re
from enum import Enum


class OccupationType(Enum):
    Occupied = 1
    Virtual = -1
    General = 0


class Operator(object):
    def __init__(self, symbol, group, is_creation: bool, occupation_type: OccupationType):
        self.symbol = symbol
        self.group = group
        self.is_creation = is_creation
        self.occupation_type = occupation_type


def check_has_pair_in_same_group(list_of_creation_operators: [Operator],
                                 list_of_annihilation_operators: [Operator]):
    assert len(list_of_creation_operators) == len(list_of_annihilation_operators)

    for i in range(len(list_of_creation_operators)):
        assert list_of_creation_operators[i].is_creation is True
        assert list_of_annihilation_operators[i].is_creation is False

        if list_of_creation_operators[i].group == list_of_annihilation_operators[i].group:
            return True

    return False


def check_has_occ_virt_pair(list_of_creation_operators: [Operator],
                            list_of_annihilation_operators: [Operator]):
    assert len(list_of_creation_operators) == len(list_of_annihilation_operators)

    for i in range(len(list_of_creation_operators)):
        assert list_of_creation_operators[i].is_creation is True
        assert list_of_annihilation_operators[i].is_creation is False

        if list_of_creation_operators[i].occupation_type.value * list_of_annihilation_operators[
            i].occupation_type.value < 0:
            return True

    return False


def sort_and_get_sign(listable):
    sorted_list = copy.deepcopy(listable)
    sign = 0

    i = 0
    while i < len(listable) - 1:
        if sorted_list[i] > sorted_list[i + 1]:
            temp = sorted_list[i + 1]
            sorted_list[i + 1] = sorted_list[i]
            sorted_list[i] = temp
            sign += 1
            i = 0
        else:
            i += 1

    return math.pow(-1, sign % 2)


def get_sign(list_of_creation_operators: [Operator]):
    creation_symbols = [operator.symbol for operator in list_of_creation_operators]
    sign_from_creation = sort_and_get_sign(creation_symbols)
    return sign_from_creation


class DeltaPairs(object):

    def __init__(self,
                 list_of_creation_operators: [Operator],
                 list_of_annihilation_operators: [Operator],
                 sign):
        assert (len(list_of_creation_operators) == len(list_of_annihilation_operators))

        length = len(list_of_creation_operators)
        symbol_pairs = []
        for i in range(length):
            symbol_pairs.append(list_of_creation_operators[i].symbol + list_of_annihilation_operators[i].symbol)

        self.symbol_pairs = symbol_pairs
        self.sign = sign

    def to_latex(self):
        string = "".join(list(map(lambda pair: "\\delta_{" + pair + "}", self.symbol_pairs)))
        if self.sign > 0:
            return " + " + string
        else:
            return " - " + string


def cc_parser_core(list_of_creation_operators: [Operator],
                   list_of_annihilation_operators: [Operator],
                   sign):

    initial_sign = sign * get_sign(list_of_creation_operators) * get_sign(list_of_annihilation_operators)

    permutations = itertools.permutations(list_of_creation_operators)

    legit_pairs = []
    for new_order in permutations:
        list_form_of_new_order = list(new_order)
        if check_has_occ_virt_pair(list_form_of_new_order, list_of_annihilation_operators) or \
                check_has_pair_in_same_group(list_form_of_new_order, list_of_annihilation_operators):
            continue

        sign_from_permutation = get_sign(list_form_of_new_order)
        legit_pairs.append(DeltaPairs(list_form_of_new_order,
                                      list_of_annihilation_operators,
                                      sign_from_permutation * initial_sign))

    return legit_pairs


def cc_parser_wrapper(groups_of_creation_annihilation_pairs,
                      occupation_type_dict):
    sign = 1
    creation_operators = []
    annihilation_operators = []
    for group in range(len(groups_of_creation_annihilation_pairs)):
        creation = groups_of_creation_annihilation_pairs[group]["creation"]
        annihilation = groups_of_creation_annihilation_pairs[group]["annihilation"]

        assert len(creation) == len(annihilation)

        n_operators = len(creation)
        group_sign = math.pow(-1, (n_operators - 1) % 2)
        sign = sign * group_sign

        for i in range(n_operators):
            creation_operators.append(Operator(creation[i], group,
                                               True, occupation_type_dict[creation[i]]))

            annihilation_operators.append(Operator(annihilation[i], group,
                                                   False, occupation_type_dict[annihilation[i]]))

    return cc_parser_core(creation_operators, annihilation_operators, sign)


def generate_conventional_occupation_type_dict(list_of_symbols):
    result = {}
    for symbol in list_of_symbols:
        if symbol >= "p":
            result[symbol] = OccupationType.General
        else:
            if symbol >= "i":
                result[symbol] = OccupationType.Occupied
            else:
                result[symbol] = OccupationType.Virtual

    return result


def cc_parser(operator_string, occupation_type_dict=None):
    groups_of_operator_string = operator_string.split(",")
    creation_pattern = re.compile(r"(?P<symbol>[a-z])\+")
    annihilation_pattern = re.compile(r"(?P<symbol>[a-z])")

    occ_dict = occupation_type_dict
    if occupation_type_dict is None:
        occ_dict = {}

    groups_of_creation_annihilation_pairs = []
    for group in range(len(groups_of_operator_string)):

        group_string = groups_of_operator_string[group]

        creation_operators = []
        annihilation_operators = []

        for creation_operator in creation_pattern.finditer(group_string):
            creation_operators.append(creation_operator.groupdict()["symbol"])

        group_string_with_creation_operator_removed = creation_pattern.sub("", group_string)

        for annihilation_operator in annihilation_pattern.finditer(group_string_with_creation_operator_removed):
            annihilation_operators.append(annihilation_operator.groupdict()["symbol"])

        groups_of_creation_annihilation_pairs.append({"creation": creation_operators,
                                                      "annihilation": annihilation_operators})

        if occupation_type_dict is None:
            concatenated = creation_operators + annihilation_operators
            for symbol in concatenated:
                if symbol >= "p":
                    occ_dict[symbol] = OccupationType.General
                else:
                    if symbol >= "i":
                        occ_dict[symbol] = OccupationType.Occupied
                    else:
                        occ_dict[symbol] = OccupationType.Virtual

    return cc_parser_wrapper(groups_of_creation_annihilation_pairs, occ_dict)
