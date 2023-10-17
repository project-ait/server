from auth import auth
from auth.rule import id_rule
from auth.dto.return_code import IdValidateCode, PWValidateCode


def test_is_include_not_allowed_char():
    data = [
        ["emp ty", True],
        ["allow", False],
        ["!@#$%^&*", False],
        ["ABCDEFG", False],
        ["1234567", False],
        ["?`'", True],
    ]
    for d in data:
        assert auth.is_include_not_allowed_char(d[0]) == d[1]


def test_has_consecutive_char():
    data = [
        ["abcd", id_rule.MAX_REPEAT_TIME, True],
        ["dcba", id_rule.MAX_REPEAT_TIME, True],
        ["1234", id_rule.MAX_REPEAT_TIME, True],
        ["4321", id_rule.MAX_REPEAT_TIME, True],
        ["aaaa", id_rule.MAX_REPEAT_TIME, False],
        ["5555", id_rule.MAX_REPEAT_TIME, False],
        ["efgh", id_rule.MAX_REPEAT_TIME, True],
        ["4567", id_rule.MAX_REPEAT_TIME, True],
        ["1212", id_rule.MAX_REPEAT_TIME, False],
        ["abcb", id_rule.MAX_REPEAT_TIME, False],
        ["!@#$", id_rule.MAX_REPEAT_TIME, False],
    ]
    for d in data:
        assert auth.has_consecutive_char(d[0], d[1]) == d[2]


def test_validate_id():
    data = [
        ["testId123", IdValidateCode.ID_REQ_NUMBER],
    ]
    for d in data:
        assert auth.validate_id(d[0]) == d[1]
