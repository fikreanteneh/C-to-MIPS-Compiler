from gen import Generator


class Parser:
    def __init__(self) -> None:
        self.datasection = [".data\n"]
        self.mainsection = [".text\n", "\t", "main:\n"]
        self.functions = []
        self.structure = {
            ("datatype", "identifier", "colon"): "DU",

            ("datatype", "identifier", "declare", "number", "colon"): "D",
            ("datatype", "identifier", "declare", "float", "colon"): "D",
            ("datatype", "identifier", "declare", "string", "colon"): "D",
            ("datatype", "identifier", "declare", "identifier", "colon"): "D",

            ("datatype", "identifier", "olist", "number", "clist", "colon"): "DUL",

            ("identifier", "increment", "colon"): "increment",
            ("identifier", "decrement", "colon"): "decrement",


            ("input", "obracket", "identifier", "cbracket", "colon"): "INPUT",
            ("output", "obracket", "identifier", "cbracket", "colon"): "OUTPUT",

            ("while", "obracket", "identifier", "comparison", "identifier", "cbracket", "obrace"): "WHILE",

            ("while", "obracket", "identifier", "comparison", "number", "cbracket", "obrace"): "WHILE",

            ("while", "obracket", "number", "comparison", "identifier", "cbracket", "obrace"): "WHILE",

            ("while", "obracket", "identifier", "comparison", "number", "cbracket", "obrace"): "WHILE",

            ("if", "obracket", "identifier", "comparison", "identifier", "cbracket", "obrace"): "IF",
            ("if", "obracket", "identifier", "comparison", "number", "cbracket", "obrace"): "IF",
            ("if", "obracket", "number", "comparison", "identifier", "cbracket", "obrace"): "IF",

            ("else if", "obracket", "identifier", "comparison", "identifier", "cbracket", "obrace"): "IF",
            ("else if", "obracket", "identifier", "comparison", "number", "cbracket", "obrace"): "IF",
            ("else if", "obracket", "number", "comparison", "identifier", "cbracket", "obrace"): "IF",

            ("else", "obrace"): "ELSE",

            ("break", "colon"): "BREAK",
            ("continue", "colon"): "CONTINUE",
            ("cbrace",): "CLOSE"

        }

    def evaluate(self, lines):
        declared = {}
        i = 0
        n = len(lines)
        output = []
        while i < n and lines[i] != ("end", "end", "end"):

            temp = []

            while True:

                # if lines[i][0] == "for":
                #     while lines[i][0] == "colon":
                #         i += 1
                #         print(lines[i])
                #     decl = lines[i-4:i-1]

                #     print("---",decl)

                if lines[i][0] == "identifier":

                    x = lines[i-1][1]

                    y = declared.get(lines[i][1], "")

                    if y and x in ["int", "float", "char"] and x != y:
                        return ("Declaration Type Error at line " + str(lines[i][2]))
                    elif not y and x not in ["int", "float", "char"]:
                        return ("Unknown Type at line " + str(lines[i][2]))
                    elif not y and x in ["int", "float", "char"]:
                        declared[lines[i][1]] = x

                    elif y and x not in ["int", "float", "char"] and lines[i-1][1] in ";{}":
                        inse = ("datatype", y, lines[i][2])
                        temp.append(inse)

                if lines[i][1] in "}":
                    if temp:
                        output.append(temp)
                    temp = [lines[i]]
                    break

                if lines[i][1] in ";{":
                    temp.append(lines[i])
                    break
                temp.append(lines[i])
                i += 1
                if i >= n:
                    break
            output.append(temp)
            i += 1
            if i >= n:
                break
        # return output
        return self.construct(output)

    # def analyze(self, line):
    #     i = 0
    #     while i < len(line):
    #         if line[i][0][1] == "for":

    #             index = 3
    #             if line[i][2][0] == "keyword":
    #                 index += 1
    #             pushed = line[i][2: 3 + index]
    #             line.insert(i, pushed)
    #             i += 1
    #             condition = line[i][3+index: 6 + index]
    #             increment = line[i][7+index: 13+index]

    #             whiled = [('keyword', 'while'), ('character', '(')] + \
    #                 condition + [('character', ')'), ('character', '{')]
    #             line[i] = whiled
    #             while line[i][0][1] != "}":
    #                 i += 1
    #             line.insert(i, increment)
    #             i += 1

    #         i += 1

    def construct(self, lines):

        stack = [self.mainsection]
        indentation = [[2, "Not"]]
        contextWhile = [""]
        contextIf = [""]

        declared = {}
        for dec, line in enumerate(lines):

            types = func = inden = None

            if line[0][0] == "while":
                types = ("while"+str(dec), "end"+str(dec))
                stack[-1].append("\t" * indentation[-1][0]+types[0]+":\n")
                inden = [indentation[-1][0] + 1, False]
                contextWhile.append(types)
               

            elif line[0][0] == "if":
                types = "if"+str(dec)
                types2 = "end"+str(dec)
                inden = [2, True]
                func = ["\t" + types + ":\n"]
                contextIf.append(types2)

            elif line[0][0] == "else if":
                types = "if"+str(dec)
                inden = [2, True]
                func = ["\t" + types + ":\n"]
                

            elif line[0][0] == "else":
                types = "else" + str(dec)
                inden = [2, True]
                func = ["\t" + types + ":\n"]

            if inden and not inden[1]:
                indentation.append(inden)

            eval = self.statementEvaluate(
                line, declared, types, contextWhile, contextIf, indentation[-1][1])

            if type(eval) == str:
                return eval
            for i in eval[0]:
                self.datasection.append("\t")
                self.datasection.append(i)
            for i in eval[1]:

                stack[-1].append("\t" * indentation[-1][0])
                stack[-1].append(i)

            if inden and inden[1]:
                indentation.append(inden)

            if func:
                stack.append(func)
            if line[0][1] == "}":
                if indentation[-1][1] == True:

                    self.functions.append("".join(stack.pop()))

                stack[-1].append("\t" * indentation[-2][0])
                stack[-1].append(eval[2][0] + ":\n")
                if indentation[-1][1] == True and dec+1 != len(lines) and lines[dec+1][0][0] in ("else if", "else"):
                    stack[-1].pop()
                    stack[-1].pop()
                elif indentation[-1][1] == True:
                    contextIf.pop()
                indentation.pop()

        self.mainsection.append("\t\tli $v0, 10\n\t\tsyscall\n")
        return "".join(self.datasection) + "".join(self.mainsection) + "".join(self.functions)

    def statementEvaluate(self, line, declared, types=None, contextWhile=None, contextIf=None, inden=None):
        temp = []
        for i in line:
            temp.append(i[0])
        temp = tuple(temp)

        if "math" in temp:
            print("mmm", temp)

            if temp[-1] != "colon":
                return ("Wrong Operation at Line " + str(line[0][2]))
            if ("datatype", "identifier", "declare") != (temp[0], temp[1], temp[2]):
                return ("Wrong Operation at Line " + str(line[0][2]))
            if (line[0][1] not in ["int", "float"]):
                return ("Operation on String character is invalid " + str(line[0][2]))

            if line[3][0] == "math":
                if line[3][1] in "-+":
                    line.insert(3, ("number", "0", line[3][2]))
                else:
                    return ("Invalid Operation" + str(line[0][2]))
            if (len(line)-5) % 2 != 0:
                return ("Wrong Operation at line " + str(line[0][2]))

            evaluate = [[line[0], line[1], line[2], line[3], line[-1]]]
            operat = []
            for i in range(4, len(line)-1, 2):
                operat.append((line[i], line[i+1]))
            evaluate.append(operat)
         
            return self.mapper(evaluate, "OPERATION", declared)

        else:
            do = self.structure.get(temp, 0)
            if do == 0:
                return ("Syntax Error at line " + str(line[0][2]) + " maye forgot ; at appropriate position")
            return self.mapper(line, do, declared, types, contextWhile, contextIf, inden)

    def mapper(self, line, gen, declared, types=None, contextWhile=None, contextIf=None, inden=None):
        if gen == "DU":
            return Generator().DU(line, declared)
        elif gen == "D":
            return Generator().D(line, declared)

        elif gen == "OUTPUT":
            return Generator().OUTPUT(line, declared)
        elif gen == "INPUT":
            return Generator().INPUT(line, declared)

        elif gen == "OPERATION":
            return Generator().OPERATION(line, declared)

        elif gen == "WHILE":
            return Generator().WHILE(line, declared, types)
        elif gen == "IF":
            return Generator().IF(line, declared, types)

        elif gen == "ELSE":
            return Generator().ELSE(line, declared, types)

        elif gen == "BREAK":
            return Generator().BREAK(line, declared, types, contextWhile, contextIf)

        elif gen == "CONTINUE":
            return Generator().CONTINUE(line, declared, types, contextWhile, contextIf)

        elif gen == "CLOSE":
            return Generator().CLOSE(line, declared, types, contextWhile, contextIf, inden)
