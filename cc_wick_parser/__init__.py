import cc_wick_parser.core


def parse(operator_string, occupation_type_dict=None):
    return core.cc_parser(operator_string, occupation_type_dict=occupation_type_dict)
