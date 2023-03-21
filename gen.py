class Generator:
    def __init__(self) -> None:
        self.datatype = {
            "char": ".byte ' '",
            "int": ".word 0",
            "float": ".float 0"
        }
        self.load = {
            "int": "lw",
            "float": "lwc1",
            "char": "lb",
            "number": "li",
            "float": "lic1",
            "string": "lb"


        }
        self.store = {
            "int": "sw",
            "float": "swc1",
            "char": "sb",

        }
        self.out = {
            "int": 1,
            "float": 2,
            "char": 11
        }
        self.inn = {
            "int": 5,
            "float": 6,
            "char": 12
        }
        self.operate = {
            "+": "add",
            "*": "mul",
            "/": "div",
            "-": "sub",
            "%": "rem"
        }
        self.equalities = {
            "==": "eq",
            "!=": "ne",
            "<=": "le",
            ">=": "ge",
            "<": "lt",
            ">": "gt"
        }
        self.inverse = {
            "==": "ne",
            "!=": "eq",
            "<=": "gt",
            ">=": "lt",
            "<": "ge",
            ">": "le"
        }

    def DU(self, token, declared):
        code = [[], [], []]
        if token[1][1] in declared:
            return code
        code[0].append(token[1][1] + ": "+self.datatype[token[0][1]] + "\n")
        declared[token[1][1]] = token[0][1]
        return code

    def D(self, token, declared):
        # TO DO for differnt Types String

        code = [[], [], []]
        if not token[1][1] in declared:
            x = self.DU(token, declared)
            code = x
        if token[3][0] == "identifier":
            code[1].append(self.load[token[0][1]] +
                           " $t0, " + token[3][1] + "\n")
        else:
            code[1].append(self.load[token[3][0]] +
                           " $t0, " + token[3][1] + "\n")
        code[1].append(self.store[token[0][1]] + " $t0, " + token[1][1] + "\n")
        return code

    def OUTPUT(self, token, declared):
        if token[2][1] not in declared:
            return ("Declare Variable First Line " + str(token[2][1]))

        code = [[], [], []]
        code[1].append(self.load[declared[token[2][1]]] +
                       " $a0, " + token[2][1] + "\n")
        code[1].append("li" + " $v0, " +
                       str(self.out[declared[token[2][1]]]) + "\n")
        code[1].append("syscall\n")
        # code[1].append("la $a0, newLine\n")
        # code[1].append("li $v0, 4\n")
        # code[1].append("syscall\n")

        return code

    def INPUT(self, token, declared):
        if token[2][1] not in declared:
            return ("Declare Variable First Line " + str(token[2][1]))

        code = [[], [], []]
        code[1].append("li" + " $v0, " +
                       str(self.inn[declared[token[2][1]]]) + "\n")
        code[1].append("syscall\n")
        code[1].append(self.store[declared[token[2][1]]] +
                       " $v0, " + token[2][1] + "\n")

        return code

    def OPERATION(self, token, declared):
        code = self.D(token[0], declared)
        code[1].pop()
        # print("--", token[1])
        # print("\n\n")
        # print("".join(code[0]))
        # print("".join(code[1]))
        # for float un handled
        for i in token[1]:
            # print("--", code)
            if i[1][0] == "identifier":
                if i[1][1] not in declared:
                    return ("Undeclared value found at line ", str(i[1][2]))
                if declared[i[1][1]] not in ("int", "float"):
                    return ("An operatable value at line ", str(i[1][2]))
                code[1].append("lw" + " $t1, " + i[1][1] + "\n")
            else:
                code[1].append(self.load[i[1][0]] + " $t1, " + i[1][1] + "\n")
            code[1].append(self.operate[i[0][1]] + " $t0, $t0, $t1\n")
        code[1].append(self.store[token[0][0][1]] +
                       " $t0, " + token[0][1][1] + "\n")
        # print("+++++", code)
        return code

    def WHILE(self, token, declared, types):
        code = [[], [], []]
        for i in range(2, 5, 2):
            if token[i][0] == "identifier":
                code[1].append(self.load[declared[token[i][1]]] +
                               " $t"+str(i//2) + ", " + token[i][1] + "\n")
            else:
                code[1].append(self.load[token[i][0]] +
                               " $t"+str(i//2) + ", " + token[i][1] + "\n")
        code[1].append("b"+self.inverse[token[3][1]] +
                       " $t1, $t2, " + types[1] + "\n")
        # code[1].append("j " + types + "\n")

        return code

    def IF(self, token, declared, types):
        code = [[], [], []]
        # if not "else" in token[0][1]:
        #     code[1].append("li $s0, 0\n")

        for i in range(2, 5, 2):
            if token[i][0] == "identifier":
                code[1].append(self.load[declared[token[i][1]]] +
                               " $t"+str(i//2) + ", " + token[i][1] + "\n")
            else:
                code[1].append(self.load[token[i][0]] +
                               " $t"+str(i//2) + ", " + token[i][1] + "\n")
        code[1].append("b"+self.equalities[token[3][1]] +
                       " $t1, $t2, " + types + "\n")
        # code[1].append("j " + types + "\n")
        return code

    def ELSE(self, token, declared, types):
        code = [[], [], []]
        code[1].append("b " + types + "\n")

        return code

    def BREAK(self, token, declared, types, contextWhile, contestIf):
        if not contextWhile:
            return ("Break Statement Without a loop" + str(token[0][2]))
        code = [[], [], []]
        code[1].append("j "+contextWhile[-1][1]+"\n")
        return code

    def CONTINUE(self, token, declared, types, contextWhile, contestIf):
        if not contextWhile:
            return ("Continue Statement Without a loop" + str(token[0][2]))
        code = [[], [], []]
        code[1].append("j "+contextWhile[-1][0]+"\n")
        return code

    def CLOSE(self, token, declared, types, contextWhile, contextIf, inden):
        code = [[], [], []]
        # con = contextIf.pop() if inden else contextWhile.pop()[0]
        if inden:
            code[1].append("j " + contextIf[-1] + "\n")
            code[2].append(contextIf[-1])
        else:
            code[1].append("j " + contextWhile[-1][0] + "\n")
            code[2].append(contextWhile.pop()[1])
        return code
