from __future__ import annotations
from abc import ABC, abstractmethod
import time
from datetime import datetime
import statistics

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


class SlijedBrojeva(Subject):
    
    def __init__(self, input_method):
        self.array = []
        self.input_method = input_method
        self._observers = []

    def kreni(self):
        while True:
            number = self.input_method.getNextInput()
            if self.input_method.out_of_resources:
                break
            self.array.append(number)
            self.notify()
            time.sleep(1)

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


class Observer(ABC):

    @abstractmethod
    def update(self, subject: Subject):
        pass


class FileWriterObserver(Observer):
    
    def __init__(self, file):
        self._file = file
        with open(file, 'w'):
            pass

    
    def update(self, subject):
        with open(self._file, "a") as out:
            out.write(str(subject.array) + ', ' + str(datetime.now().isoformat(' ')) + '\n')


class SumPrinterObserver(Observer):

    def update(self, subject):
        print("Sum:", sum(subject.array))


class AvgPrinterObserver(Observer):

    def update(self, subject):
        print("Average:", sum(subject.array)/len(subject.array))


class MedianPrinterObserver(Observer):

    def update(self, subject):
        print("Median:", statistics.median(subject.array))


class InputMethod(ABC):
    
    out_of_resources = False

    @abstractmethod
    def getNextInput(self):
        pass


class TipkovnickiIzvor(InputMethod):
    
    def getNextInput(self):
        number =  int(input("Input a number or -1 to end inputs: "))
        if number == -1:
            self.out_of_resources = True
        return number
    

class DatotecniIzvor(InputMethod):
    
    def __init__(self, file):
        self._file = open(file)

    def getNextInput(self):
        number = int(self._file.readline().strip())
        if number == -1:
            self.out_of_resources = True
        return number


def main():
    sb = SlijedBrojeva(DatotecniIzvor('input.txt'))
    sb.attach(FileWriterObserver('output.txt'))
    sb.attach(SumPrinterObserver())
    sb.attach(AvgPrinterObserver())
    sb.attach(MedianPrinterObserver())
    sb.kreni()

if __name__ == "__main__":
    main()
