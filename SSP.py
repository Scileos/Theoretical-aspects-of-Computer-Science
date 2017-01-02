from random import randint, sample
from itertools import chain, combinations
from time import time

class SSP():
    def __init__(self, S=[], t=0):
        self.S = S
        self.t = t
        self.n = len(S)
        #
        self.decision = False
        self.total    = 0
        self.selected = []

    def __repr__(self):
        return "SSP instance: S="+str(self.S)+"\tt="+str(self.t)
    
    def random_instance(self, n, bitlength=10):
        max_n_bit_number = 2**bitlength-1
        self.S = sorted( [ randint(0,max_n_bit_number) for i in range(n) ] , reverse=True)
        self.t = randint(0,n*max_n_bit_number)
        self.n = len( self.S )

    def random_yes_instance(self, n, bitlength=10):
        max_n_bit_number = 2**bitlength-1
        self.S = sorted( [ randint(0,max_n_bit_number) for i in range(n) ] , reverse=True)
        self.t = sum( sample(self.S, randint(0,n)) )
        self.n = len( self.S )

    ###

    def try_at_random(self):
        candidate = []
        total = 0
        while total != self.t:
            candidate = sample(self.S, randint(0,self.n))
            total     = sum(candidate)
            print( "Trying: ", candidate, ", sum:", total )


    def bruteforce(self):
        numbers = self.S
        target = self.t
        size = 1
        subsets = []
        while size <= len(numbers):
            for combination in combinations(numbers, size):
                if sum(combination) == target:
                    subsets.append(combination)
            size += 1
        if not subsets:
            print (False)    
        else:
            print (subsets)
            print (True)


    def combinations(numbers, size):
        if len(numbers) <= 0 or size <= 0:
            yield []
        else:
            for index, number in enumerate(numbers):
                for combination in combinations(numbers[index+1:], size-1):
                    yield [number]+combination
        
                

                
            

instance = SSP()
instance.random_yes_instance(5)
print( instance )

instance.bruteforce()
