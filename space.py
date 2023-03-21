from lexer import Lexer


class Checker:
    def __init__(self, value):
        # with open(value, "r") as file:
        #     self.lines = file.readlines()
        self.lines = value
        # self.code = self.removeComments()
        # self.blockPass = self.blockChecker()

        # self.variables = set()
        # self.functions = set()

    def returns(self):
        if self.blockPass:
            return self.lines
        return False

    def removeComments(self, lines):  # removes comment, white spaces and header files
        answer = []
        block = False
        comment = False
        temp = []
        temp2 = []
        i, j = 0, 0
        while i < len(lines):
            line = lines[i][0]
            if line[0] == "#":
                line = "\n"
            if line[-1] == "\n":
                line = line[:-1]
            j = 0
            temp = []
            while j < len(line):
                word = line[j]
                j += 1
                if block:
                    if word == "*" and line[j] == "/":
                        temp, temp2 = temp2, []
                        block = False
                        j += 1
                    continue
                elif word == "/" and j < len(line):
                    if line[j] == "*":
                        temp2, temp = temp, []
                        block = True
                        j += 1
                        continue
                    elif line[j] == "/":
                        break
                temp.append(word)
            appended = "".join(temp).strip()
            if appended:
                answer.append(appended)
            i += 1
        return answer

    def blockChecker(self, lines):   # checks the correct block element is done
        stack = []

        blockElements = {"{", "(", "["}
        equiv = {"]": "[", ")": "(", "}": "{"}
        for i, line in enumerate(lines):

            for i, word in enumerate(line):
                if word == "/" and line[i+1] == "/":
                    break
                elif word in blockElements:
                    stack.append(word)
                elif word in equiv:

                    if not stack or stack.pop() != equiv[word]:
                        return( "Error: Unmatched Paranthesis at line " +  str(i))
        if len(stack) != 0:
            print(stack)
            return "Error: Unclosed Paranthesis"
        return Lexer(lines).lexing(lines)

    def lineAppender(self, lines):
        for i, line in enumerate(lines):
            x = i+1
            lines[i] = (line, x)
        return lines


# x = Checker("c.c")
# print(x.code)
