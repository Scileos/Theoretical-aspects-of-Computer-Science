from random import randint, sample
from itertools import chain, combinations
import time
import random

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


    def bruteforce(self):
        """Uses a brute force method to exhaustively search for a subset of S that has the sum of t"""
        numbers = self.S 
        target = self.t
        size = 1
        subsets = []
        while size <= len(numbers): #Check every element in the set
            for combination in combinations(numbers, size): #For each combination
                if sum(combination) == target: #If the sum of the combination is the total then add it to the correct subset array
                    subsets.append(combination)
            size += 1
        if not subsets: #If subsets is empty return false
            return False    
        else: #else Return True as there is at least one result
            return True
            


    def combinations(numbers, size):
        """Recursively creates every possible combination of numbers from the set"""
        if len(numbers) <= 0 or size <= 0: #If the length of the array is 0 return blank
            yield []
        else:
            for index, number in enumerate(numbers):
                for combination in combinations(numbers[index+1:], size-1):
                    yield [number]+combination
        
                
    

    def Dynamic(self, S, n, t):
        """Using Dynamic Programming principals creates a two-dimensional array that will be filled with boolean attributes
        The last entry in the array will decide on our answer """
        subset = [[0 for x in range(n+1)] for y in range(t+1)] #Creates an array of our needed size, rows for our elements and columns for our total
        
        for i in range(0, n+1): #All results in column 0 will return True
            subset[0][i] = True
        
        for i in range(1, t+1): #All results in row 0 apart from the first element will return False
            subset[i][0] = False
         
        for i in range(1, t+1): #for each integer in the total
            for j in range(1, n+1): # for each element from the set (So essentially for each cell in the array)
                subset[i][j] = subset[i][j-1] #Sets the value as false
                if i >= S[j-1]: #When the column value is greater than the element (So it can be a subset of it)
                    subset[i][j] = subset[i][j] or subset[i - S[j-1]][j-1] #Set the value as True
        return subset[t][n] #Return the last result in the array




    def Greedy(self):
        """Uses a Greedy methodology to get an approximate solution, but very quick
        The algorithm sorts the Set largest first then adds each element to the solution subset unless it
        compromises the feasability of said subset ie: It will make the solution larger than the total"""
        S = sorted(self.S)
        t = self.t  
        counter = 0
        pick = 0
        solution = []
        for i in range(0, len(S)): #For each element in the set
            pick = S[i]
            if (counter + pick <= t): #Check if it will ruin the feasability of the solution
                counter += pick
                solution.append(pick) #If not then add it to the solution subset            
        return solution


    def Grasp(self):
        """An extension of Greedy that tries to improve upon the original answer by swapping out one of 
        the numbers with one in the neighbourhood of S for a given number of iterations """
        Best_Candidate = []
        for i in range(0, 20): #In given iterations
            Greedy_Candidate = self.randomizedGreedy()
            if len(Greedy_Candidate) == 0:
                return 0
            restOfSet = [x for x in self.S if x not in Greedy_Candidate] #Create an array which contains the neighbourhood of Greedy_Candidate in S
            Grasp_Candidate = self.localSearch(Greedy_Candidate, restOfSet)
            if abs(self.t - sum(Grasp_Candidate)) < abs(self.t - sum(Best_Candidate)):
                print("Changing best candidate from ", sum(Best_Candidate), " to ", sum(Grasp_Candidate))
                Best_Candidate = Grasp_Candidate
        return ("Best candidate: ",sum(Best_Candidate))


    def localSearch(self, Greedy_Candidate, restOfSet):
        Local_Search = Greedy_Candidate
        changingList = list(Local_Search)
        Random_Num = random.choice(changingList) #choose a random number from the best candidate
        changingList.remove(Random_Num)
        if not restOfSet:
            return Local_Search
        else:    
            changingList.append(random.choice(restOfSet)) #And swap it with a random number from it's neighbourhood
            Local_Search = changingList #Then change the Best solution
        return Local_Search


    def randomizedGreedy(self):
        """Constructs a randomized Greedy solution to be used in GRASP """
        S = sorted(self.S)
        t = self.t  
        counter = 0
        pick = 0
        solution = []
        while len(S) != 0: #While the list isn't empty'
            pick = random.choice(S)
            S.remove(pick)
            if (counter + pick <= t): #Check if it will ruin the feasability of the solution
                counter += pick
                solution.append(pick) #If not then add it to the solution subset            
        return solution


    def Tabu(self):
        """Uses the Tabu metaheuristic approach to find a solution by only allowing non-Tabu elements to be added"""
        S = self.S
        t = self.t
        tabuList = [] #List of already used elements
        initialCandidate = []

        #t = 0 special case
        if t == 0:
            return 0

        #Simple algorithm to create an initial solution
        for i in range(0, 3):
            ran = random.choice(self.S)
            if ran + sum(initialCandidate) <= t:
                initialCandidate.append(ran)
                S.remove(ran)
                
        #Tabu search    
        best = list(initialCandidate) #Setting best option
        nonTabu = [x for x in S if x not in initialCandidate] #Create the neighbourhood of S
        for i in range(0, 50): #For a given amount of iterations
            if len(tabuList) == len(nonTabu): #If all options tried then finish
                break
            bestCandidate = 0 #Refresh bestCandidate
            if len(nonTabu) == 0: #If neighbourhood is 0 special case
                return best
            for j in range(0, len(nonTabu)): #Check every item in the neighbourhood
                if nonTabu[j] not in tabuList: #If not tabu
                    if bestCandidate < nonTabu[j]: #And element is greater than current bestCandidate
                        bestCandidate = nonTabu[j] #Set new bestCandidate                       
            if sum(best) + bestCandidate <= t: #After bestCandidate is found, check if it will ruin feasibility of best solution
                print ("adding: ", bestCandidate)
                best.append(bestCandidate) #If ok, then create new best
                print("Total now: ", sum(best))
                tabuList.append(bestCandidate) #Add used element to tabuList
        return best
                         



instance = SSP()
#instance.random_yes_instance(10)
#print (instance)
#instance.(Method)


#Code to print times and percentages
#for i in range(5, 25):
#    times = []
#    percentage = []
#    for j in range(0, 20):
#        instance.random_yes_instance(i)
#        percentage.append(instance.Tabu())
#    print (sum(percentage) / len(percentage))

        #start_time = time.clock()
        #print("--- %s seconds ---" % (time.clock() - start_time))   
       # times.append(time.clock() - start_time)
    #print ("length of array: ", i, " average time taken: ", sum(times) / len(times))
    #print(sum(times) / len(times))

