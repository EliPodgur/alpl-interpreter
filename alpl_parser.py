from exceptions import *


def parse_register(r) -> int:
    try:
        i = int(r[1])
    except:
        raise SyntaxException
    if i > 9:
        raise IllegalValue
    return i


def parse_int(integer) -> int:
    return int(integer)


def parse_operator(op: str) -> callable:
    if op == "+":
        return int.__add__
    elif op == "*":
        return int.__mul__
    elif op == "<":
        return int.__lt__
    elif op == "=":
        return int.__eq__
    else:
        return int.__gt__


def parse_let(line: str):
    line = line[4:]  # remove LET token
    target_reg = parse_register(line[:2])  # get target register
    line = line[6:]  # remove := and target register

    right = None
    left_reg = False
    right_reg = False
    op = None
    finished = False

    if line.startswith("R"):
        left = parse_register(line[:2])
        left_reg = True
    else:
        if line.find(' ') == -1:  # only left assigned
            left = parse_int(line)
            finished = True  # finished parsing the line
        else:
            left = parse_int(line[:line.find(' ')])
    if not finished:
        line = line[line.find(' ') + 1:]
        op = parse_operator(line[:1])
        line = line[2:]

        if line.startswith("R"):
            right = parse_register(line[:2])
            right_reg = True
        else:
            right = parse_int(line)
    result = {'command_type': 'let', 'target_reg': target_reg, 'left_reg': left_reg, 'left': left,
              'right_reg': right_reg, 'right': right, 'op': op, 'unary': finished}
    return result


def parse_if(line):
    line = line[3:]
    left_reg = False
    right_reg = False

    if line.startswith("R"):
        left = parse_register(line[:2])
        left_reg = True
    else:
        left = parse_int(line[:line.find(' ')])

    line = line[line.find(' ') + 1:]
    op = parse_operator(line[:1])
    line = line[2:]

    if line.startswith("R"):
        right = parse_register(line[:2])
        right_reg = True
    else:
        right = parse_int(line[:line.find(' ')])

    line = line[line.find(' ') + 1:]
    target = line
    result = {'command_type': 'if', 'target': target, 'left_reg': left_reg, 'left': left, 'right_reg': right_reg,
              'right': right, 'op': op}
    return result


def parse_jump(line):
    line = line[5:]
    return {'command_type': 'jump', 'target': line}


def parse_print(line):
    line = line[6:]
    r = parse_register(line)
    return {'command_type': 'print', 'src_reg': r}


def parse_call(line):
    line = line[5:]
    return {'command_type': 'call', 'target': line}


def parse_return():
    return {'command_type': 'return'}


def parse_label(line):
    label = line[:-1]
    return {'command_type': 'label', 'target': label}


def parse_line(line: str):
    if line.startswith("LET "):
        return parse_let(line)

    elif line.startswith("IF "):
        return parse_if(line)

    elif line.startswith("JUMP "):
        return parse_jump(line)

    elif line.startswith("PRINT "):
        return parse_print(line)

    elif line.startswith("CALL "):
        return parse_call(line)

    elif line == "RETURN":
        return parse_return()

    elif line.endswith(":"):
        return parse_label(line)

    else:
        raise SyntaxException


def file_parser(file_path: str) -> list:
    with open(file_path, 'r') as f:
        code = f.read().splitlines()
    return code
