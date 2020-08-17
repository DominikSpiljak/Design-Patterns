
Symbols = {}

class parseExpression:

    def __init__(self, expression):
        self.expression = expression

    def parse(self, strinput):
        for operator in ["+-", "*/"]:
            depth = 0
            for p in range(len(strinput) - 1, -1, -1):
                if strinput[p] == ')': depth += 1
                elif strinput[p] == '(': depth -= 1
                elif depth==0 and strinput[p] in operator:
                    # strinput is a compound expression
                    return (strinput[p], self.parse(strinput[:p]), self.parse(strinput[p+1:]))
        strinput = strinput.strip()
        if strinput[0] == '(':
            # strinput is a parenthesized expression?
            return self.parse(strinput[1:-1])
        # strinput is an atom!
        return strinput

    def _convert_to_str(self, expression):
        if type(expression[1]) != str:
            expression1 = self._convert_to_str(expression[1])
        else:
            try:
                expression1 = str(float(expression[1]))
            except(ValueError):
                expression1 = expression[1]
        if type(expression[2]) != str:
            expression2 = self._convert_to_str(expression[2])
        else:
            try:
                expression2 = str(float(expression[2]))
            except(ValueError):
                expression2 = expression[2]
        return '({} {} {})'.format(expression1, expression[0], expression2)

    def  __str__(self):
        expression = self.expression
        for symbol in Symbols:
            expression = expression.replace(symbol, str(Symbols[symbol]))
        parsed = self.parse(expression)
        return self._convert_to_str(parsed)

    def evaluate(self):
        eval_str = self.__str__()
        return eval(eval_str)


def main():
    global Symbols
    tree = parseExpression("6*(x+4)/2-3-x")
    print(tree)
    Symbols['x'] = 5
    print(tree.evaluate())

if __name__ == "__main__":
    main()