class SyntaxException(Exception):
    pass


class IllegalValue(Exception):
    pass


class LabelDuplication(Exception):
    pass


class NoSuchLabel(Exception):
    pass


class UnassignedRegister(Exception):
    pass