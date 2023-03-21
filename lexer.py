import re
import nltk
from parse import Parser


class Lexer:
    def __init__(self, line):
        self.keywords = "auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|string|class|struc|include|scanf|printf"
        self.operators = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)"
        self.numerals = "^(\d+)$"
        self.characters = "[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\""
        self.identifiers = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
        self.headers = "([a-zA-Z]+\.[h])"
        self.word = line
        self.grammar = {"int": "datatype", "float": "datatype", "char": "datatype", "double": "datatype", "{": "obrace", "}": "cbrace", ";": "colon", "(": "obracket", ")": "cbracket", "[": "olist", "]": "clist", "printf": "output", "scanf": "input", "while": "while", "for": "for", "=": "declare", "if": "if", "else if": "else if", "else": "else", "continue": "continue", "break": "break", "+": "math", "-": "math", "%": "math", "*": "math", "/": "math", "++": "increment", "--": "decrement", "==": "comparison", "<=": "comparison", ">=": "comparison", "!=": "comparison", ">": "comparison", "<": "comparison"}

    def lexe(self, Source_Code):

        output = []
        count = 0
        for line in self.word:
            count = count + 1
            if (line.startswith("#include")):
                tokens = nltk.word_tokenize(line)
            else:
                tokens = nltk.wordpunct_tokenize(line)
            temp = []
            for token in tokens:
                if (re.findall(self.keywords, token)):
                    temp.append(("keyword", token))
                elif (re.findall(self.headers, token)):
                    temp.append(("header", token))
                elif (re.findall(self.operators, token)):
                    temp.append(("operator", token))
                elif (re.findall(self.numerals, token)):
                    temp.append(("number", token))
                elif (re.findall(self.characters, token)):
                    temp.append(("character", token))
                elif (re.findall(self.identifiers, token)):
                    temp.append(("identifier", token))
            output.append(temp)

        return output

    def lexing(self, lines):

        output = []
        for i, line in enumerate(lines):
            line.strip()
            if (line.startswith("#include")):
                tokens = nltk.word_tokenize(line)
            else:
                tokens = nltk.wordpunct_tokenize(line)
            temp = []
            for token in tokens:
                if (re.findall(self.keywords, token)):
                    temp.append(("keyword", token, i))
                elif (re.findall(self.headers, token)):
                    temp.append(("header", token, i))
                elif (re.findall(self.operators, token)):
                    temp.append(("operator", token, i))
                elif (re.findall(self.numerals, token)):
                    temp.append(("number", token, i))
                elif (re.findall(self.characters, token)):
                    temp.append(("character", token, i))
                elif (re.findall(self.identifiers, token)):
                    temp.append(("identifier", token, i))
            output.append(temp)
        # return output
        return self.filter(output)

    def filter(self, lines):
        output = []
        for i in lines:
            if not i or i[0][1] == "#" or i[0][1] == "//":
                continue
            for j in i:
                output.append(j)
        output.append(("end", "end", "end"))
        # return output

        return self.decompose(output)

    def decompose(self, lines):
        output = []
        n = len(lines)
        i = 0
        while i < n:
            word = lines[i]
            if word[0] == "character":
                for ch in word[1]:
                    output.append(("character", ch, word[2]))
            else:
                output.append(word)

            i += 1

        # return output
        return self.merge(output)

    def merge(self, lines):

        output = []
        n = len(lines) - 1
        i = 0
        while i < n:
            word = lines[i]
            if word[0] == "identifier" and output and output[-1][1] == '"' and lines[i + 1][1] == '"':
                output.pop()
                output.append((("string"), "'" + word[1] + "'", word[2]))
                i += 1

            elif word[1] == "." and output[-1][0] == "number" and lines[i + 1][0] == 'number':
                x = output.pop()[1] + word[1] + lines[i+1][1]
                output.append(("float", x, word[2]))
                i += 1
           

            elif word[1] == "else" and lines[i + 1][1] == 'if':
                output.append(("keyword", "else if", word[2]))
                i += 1

            elif word[1] == "printf" or word[1] == "scanf":
                identify = None
                i += 1
                while i < n:
                    if lines[i][0] == "identifier":
                        identify = lines[i][1]
                    if ")" in lines[i][1]:
                        output.append(word)
                        output.append(('character', '(', word[2]))
                        output.append(("identifier", identify, word[2]))
                        output.append(('character', ')', word[2]))
                        identify = 1
                        if ";" in lines[i][1]:
                            output.append(('character', ';', word[2]))
                        break
                    if identify == 1:
                        return ("Error on Line" + str(word[2]))

                    i += 1

            else:
                output.append(word)
            i += 1
        # return output
        return self.modify(output)

    def modify(self, lines):
        output = []
        for line in lines:
            if line[1] in self.grammar:
                output.append((self.grammar[line[1]], line[1], line[2]))
            else:
                output.append(line)

        # return output
        return Parser().evaluate(output)
