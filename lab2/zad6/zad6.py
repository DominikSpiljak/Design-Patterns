
from __future__ import annotations
from abc import ABC, abstractmethod
import ast
import string
import re
import copy


class Subject(ABC):

    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class Observer(ABC):

    @abstractmethod
    def update(self, subject: Subject):
        pass


class Sheet():
    
    def __init__(self, x, y):
        self._cells = [[Cell('0') for j in range(y)] for i in range(x)]
        self._observers = []

    @staticmethod
    def _calculate_position(ref):
        row = int(re.findall(r'[1-9][0-9]*', ref)[0]) - 1
        letters = list(reversed(re.findall(r'[A-Z]', ref)))
        column = string.ascii_uppercase.index(letters[0])
        for i, letter in enumerate(letters):
            if i == 0:
                continue
            column += (string.ascii_uppercase.index(letter) + 1) * i * len(string.ascii_uppercase)
        return [row, column]

    def cell(self, ref):
        row, column = Sheet._calculate_position(ref)
        return self._cells[row][column]

    def set(self, ref, content):
        backup_cells = copy.deepcopy(self._cells)
        backup_observers = copy.deepcopy(self._observers)

        try:
            row, column = Sheet._calculate_position(ref)

            for ref in self.getrefs(self._cells[row][column]):
                self.cell(ref).detach(self._cells[row][column])

            self._cells[row][column].exp = content

            for ref in self.getrefs(self._cells[row][column]):
                self.cell(ref).attach(self._cells[row][column])

            self.evaluate(self._cells[row][column])
        
        except:

            self._cells = backup_cells
            self._observers = backup_observers
            raise RuntimeError('Error detected, restoring from backup')

    def getrefs(self, cell):
        return re.findall(r'[A-Z]+[1-9][0-9]*', cell.exp)

    def evaluate(self, cell):
        vars = {}
        refs = {}
        for ref in self.getrefs(cell):
            vars[ref] = self.cell(ref).value
            refs[ref] = self.cell(ref)
        cell.value = Sheet.eval_expression(cell.exp, variables=vars)
        cell.variables = vars
        cell.ref = refs
        cell.notify()
        return cell.value

    @staticmethod
    def eval_expression(exp, variables={}):
        def _eval(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Name):
                return variables[node.id]
            elif isinstance(node, ast.BinOp):
                return _eval(node.left) + _eval(node.right)
            else:
                raise Exception('Unsupported type {}'.format(node))

        node = ast.parse(exp, mode='eval')
        return _eval(node.body)

    def print(self):
        print('\n'.join([''.join(['{:6}'.format(item.value) for item in row]) 
            for row in self._cells]))


class Cell(Observer, Subject):

    def __init__(self, exp):
        self.exp = exp
        self._observers = []
        self.value = 0
        self.ref = {}
        self.variables = {}

    def update(self, subject):
        # find ref of updated subject
        for reference, cell_object in self.ref.items():
            if cell_object == subject:
                # update value
                self.variables[reference] = subject.value
        # reevaluate expression
        self.value = Sheet.eval_expression(self.exp, variables=self.variables)
        self.notify()

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


if __name__=="__main__":
    s=Sheet(5,5)
    print()

    s.set('A1','2')
    s.set('A2','5')
    s.set('A3','A1+A2')
    s.print()
    print()

    s.set('A1','4')
    s.set('A4','A1+A3')
    s.print()
    print()

    try:
        s.set('A1','A3')
    except RuntimeError as e:
        print("Caught exception:",e)

    s.print()
    print()
