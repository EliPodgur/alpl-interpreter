import alpl_parser as parser
from interpreter import clean

def test_let():
    line = "LET R0 := 500"
    a = parser.parse_let(line)
    assert a == {'command_type': 'let', 'target_reg': 0, 'left_reg': False, 'left': 500,
                 'right_reg': False, 'right': None, 'op': None, 'unary': True}


def test_if():
    line = "IF R0 = R1 END"
    a = parser.parse_if(line)
    assert a == {'command_type': 'if', 'target': 'END', 'left_reg': True, 'left': 0,
                 'right_reg': True, 'right': 1, 'op': int.__eq__}


def test_jump():
    line = "JUMP LOOP"
    a = parser.parse_jump(line)
    assert a == {'command_type': 'jump', 'target': 'LOOP'}


def test_print():
    line = "PRINT R5"
    a = parser.parse_print(line)
    assert a == {'command_type': 'print', 'src_reg': 5}


def test_call():
    line = "CALL LOOP"
    a = parser.parse_call(line)
    assert a == {'command_type': 'call', 'target': 'LOOP'}


def test_label():
    line = "LOOP:"
    a = parser.parse_label(line)
    assert a == {'command_type': 'label', 'target': 'LOOP'}


def test_clean():
    s = "     LET    R1          :=   10   +  R5    "
    assert clean(s) == "LET R1 := 10 + R5"