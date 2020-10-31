import sys

import alpl_parser as parser
from exceptions import *

registers = [None] * 10  # use this to manage registers
return_stack = []  # use this to manage returns
labels = {}  # use this to manage labels


def clean(line: str) -> str:
    # replace all double spaces with one space and removes leading and trailing spaces
    return ' '.join(line.split())


def execute_let(target_reg, left_reg, left, right_reg, right, op, unary, **kwargs):
    if left_reg:
        left_value = registers[left]
        if left_value is None:
            raise UnassignedRegister(f"R{left}")
    else:
        left_value = left

    if not unary:
        if right_reg:
            right_value = registers[right]
            if right_value is None:
                raise UnassignedRegister(f"R{left}")
        else:
            right_value = right
        result = op(left_value, right_value)

    else:
        result = left_value

    registers[target_reg] = result


def execute_if(target, left_reg, left, right_reg, right, op, index, **kwargs):
    if target not in labels.keys():
        raise NoSuchLabel

    if left_reg:
        left_value = registers[left]
        if left_value is None:
            raise UnassignedRegister(f"R{left}")
    else:
        left_value = left

    if right_reg:
        right_value = registers[right]
        if right_value is None:
            raise UnassignedRegister(f"R{right}")
    else:
        right_value = right

    if op(left_value, right_value):
        return labels[target]
    else:
        return index + 1


def execute_jump(target, **kwargs):
    return labels[target]


def execute_print(src_reg, **kwargs):
    to_print = registers[src_reg]
    if to_print is None:
        raise UnassignedRegister(f"R{src_reg}")
    print(to_print)


def execute_call(target, index, **kwargs):
    return_stack.append(index)
    return execute_jump(target=target)


def execute_return():
    return return_stack.pop() + 1


def execute_line(params: dict, index: int):
    if params['command_type'] == 'let':
        execute_let(**params)

    elif params['command_type'] == 'label':
        pass

    elif params['command_type'] == 'if':
        return execute_if(**params, index=index)

    elif params['command_type'] == 'jump':
        return execute_jump(**params)

    elif params['command_type'] == 'print':
        execute_print(**params)

    elif params['command_type'] == 'call':
        return execute_call(**params, index=index)

    elif params['command_type'] == 'return':
        return execute_return()
    return index + 1


def prog_preprocessor(prog: list):
    for i in range(len(prog)):
        d = prog[i]
        if d['command_type'] == 'label':  # map labels with indices in label hash table
            if d['target'] in labels.keys():
                raise LabelDuplication
            labels[d['target']] = i
    for i in range(len(prog)):
        d = prog[i]
        if d['command_type'] == 'jump' or d['command_type'] == 'call':
            if d['target'] not in labels.keys():
                raise NoSuchLabel


def main(file):
    program = parser.file_parser(file)
    program_dicts = []
    for line in program:
        line = clean(line)
        program_dicts.append(parser.parse_line(line))
    prog_preprocessor(program_dicts)  # checks and inits labels

    index = 0
    while index < len(program_dicts):  # execution loop
        index = execute_line(program_dicts[index], index)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'prog2.txt'
    main(file_path)
