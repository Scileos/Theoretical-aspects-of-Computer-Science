from random import randint, sample
from itertools import chain, combinations
from time import time

class SSP():
    def __init__(self, S=[], t=0):
        """Initialize the SSP object with a sample array (S), total (t), number of elements."""
        self.S = S
        self.t = t
        self.n = len(S)
        #
        self.decision = False
        self.total    = 0
        self.selected = []

    def __repr__(self):
        """How to represent a printed instance of an object"""
        return "SSP instance: S="+str(self.S)+"\tt="+str(self.t)
    
    def random_instance(self, n, bitlength=10):
        """Creates a random array of given amount numbers, creates a random total to find."""
        max_n_bit_number = 2**bitlength-1
        self.S = sorted( [ randint(0,max_n_bit_number) for i in range(n) ] , reverse=True)
        self.t = randint(0,n*max_n_bit_number)
        self.n = len( self.S )

    def random_yes_instance(self, n, bitlength=10):
        """Creates a random array of given amount numbers, creates a total to find made from the original list, will always pass."""
        max_n_bit_number = 2**bitlength-1
        self.S = sorted( [ randint(0,max_n_bit_number) for i in range(n) ] , reverse=True)
        self.t = sum( sample(self.S, randint(0,n)) )
        self.n = len( self.S )

    ###

    def try_at_random(self):
        """Tests the sum of a random selection from the array and checks it against the toFind number"""
        candidate = []
        total = 0
        while total != self.t:
            candidate = sample(self.S, randint(0,self.n))
            total     = sum(candidate)
            print( "Trying: ", candidate, ", sum:", total )
            

instance = SSP() #Set variable 'instance' as an initialized SSP object (Defined by __init__)
instance.random_yes_instance(4) #Create a random instance array that will definitely pass
print( instance ) #Print the object instance (Defined buy __repr__)

instance.try_at_random() #Test a sum of random numbers against the toFind number, close when solution is found
