from space import Checker
from lexer import Lexer


def main(value):
    with open(value, "r") as file:
        lines = file.readlines()

    lines = Checker(lines).blockChecker(lines)
    # for i in lines:
    #     print("\n")
    #     print(i)

    return lines


print(main("c.c"))
