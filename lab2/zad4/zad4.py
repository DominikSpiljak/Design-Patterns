from __future__ import annotations
import random
import math
from abc import ABC, abstractmethod


class DistributionTester:

    def __init__(self, number_strategy: NumberStrategy, percentile_strategy: PercentileStrategy):
        self._number_strategy = number_strategy
        self._percentile_strategy = percentile_strategy

    def number_strategy(self, number_strategy: NumberStrategy):
        self._number_strategy = number_strategy

    def percentile_strategy(self, percentile_strategy: PercentileStrategy):
        self._percentile_strategy = percentile_strategy

    def generate_numbers(self):
        numbers = self._number_strategy.generate_numbers()
        print("Generated number list:", str(numbers))
        return numbers

    def calculate_percentiles(self, numbers):
        percentiles = {}
        for percentile in range(10, 100, 10):
            percentiles[percentile] = self._calculate_percentile(percentile, numbers)
            print("Calculated percentile", str(percentile), ":", str(percentiles[percentile]))
        return percentiles
        

    def _calculate_percentile(self, percentile, numbers):
        return self._percentile_strategy.calculate_percentile(percentile, numbers)


class NumberStrategy(ABC):
    
    @abstractmethod
    def generate_numbers(self):
        pass


class SequentialStrategy(NumberStrategy):
    
    def __init__(self, start, end, step):
        self._start = start
        self._end = end
        self._step = step
    
    def generate_numbers(self):
        return list(range(self._start, self._end, self._step))


class RandomNormalDistributionStrategy(NumberStrategy):
    
    def __init__(self, mean, variance, n_elements):
        self._mean = mean
        self._variance = variance
        self._n_elements = n_elements
    
    def generate_numbers(self):
        return [random.normalvariate(self._mean, self._variance) for i in range(self._n_elements)]


class FibonacciStrategy(NumberStrategy):
     
    def __init__(self, n_elements):
        self._n_elements = n_elements
    
    def generate_numbers(self):
        nums = [1, 1]
        for _ in range(self._n_elements - 2):
            nums.append(nums[-1] + nums[-2])
        return nums[:self._n_elements]


class PercentileStrategy(ABC):

    @abstractmethod
    def calculate_percentile(self, percentile):
        pass


class SortedPercentile(PercentileStrategy):

    def calculate_percentile(self, percentile, numbers):
        n_p = (percentile * len(numbers)) / 100 + 0.5 - 1

        if round(n_p) >= len(numbers):
            return sorted(numbers)[-1]
        elif round(n_p) < 0:
            return sorted(numbers)[0]
        else:
            return sorted(numbers)[round(n_p)]
            

class InterpolatedPercentile(PercentileStrategy):

    def calculate_percentile(self, percentile, numbers):
        numbers.sort()
        percentiles = []
        N = len(numbers)
        for i in range(N):
            percentiles.append(100*(i+1-0.5)/N)
        if percentile < percentiles[0]:
            return numbers[0]
        elif percentile > percentiles[-1]:
            return numbers[-1]
        for i in range(len(percentiles) - 1):
            if percentile >= percentiles[i] and percentile <= percentiles[i + 1]:
                vp = numbers[i] + N * (percentile-percentiles[i])*(numbers[i+1]-numbers[i])/100
        return vp



def main():
    dt = DistributionTester(FibonacciStrategy(30), InterpolatedPercentile())
    numbers = dt.generate_numbers()
    dt.calculate_percentiles(numbers)

if __name__ == "__main__":
    main()