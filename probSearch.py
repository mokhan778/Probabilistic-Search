import random
import numpy as np

class terrain:
    def __init__(self, terrain_type, probability, relativeProbabilities, hasTarget):
        self.type = terrain_type
        self.prob = probability
        self.relProbs = relativeProbabilities
        self.target = hasTarget
        
    def toString(self):
        return "Type: " + self.type + " | Chance to find target: " + str(self.prob)
        


class search:
    
    terrainProb = {
        "flat": 0.2,
        "hill": 0.3,
        "forrest": 0.3,
        "cave": 0.2
    }
    
    findProb = {
        "flat": 0.9,
        "hill": 0.7,
        "forrest": 0.3,
        "cave": 0.1
    }
    
    targetR = random.randint(0,50)
    targetC = random.randint(0,50)
    beliefs = [[0.0 for i in range(50)] for j in range(50)]
    currentLoc = [0,0]
    
    def __init__(self, landscape):
        self.land = landscape
        
    def populateLand(self):
        #row and column the target is located
        
        d = 1.0/(50*50)
        relProb = d
        for i in range(50):
            for j in range(50):
                t = np.random.choice(list(self.terrainProb.keys()), 4, list(self.terrainProb.values()))[0]
                self.land[i][j] = terrain(t,self.findProb[t], relProb, True) if (i == self.targetR and j == self.targetC) else terrain(t,self.findProb[t], relProb, False)
        #self.printLand(self.land)
        return self.land
        
    
    def pickLocation(self):
        rc = [None, None]
        nextLocation = 0.0
        for i in range(50):
            for j in range(50):
                if (nextLocation < self.land[i][j].relProbs or nextLocation == 0.0):
                    nextLocation = self.land[i][j].relProbs
                    rc = [i, j]
        return rc
        
    def pickTypeLocation(self, type):
        rc = [None, None]
        move = self.moveTarget()
        
        type1 = move[0]
        type2 = move[1]
        extra = 0.0
        
        for i in range(50):
            for j in range(50):
                surround = 0.0
                if ( self.land[i][j].relProbs != 0.0):
                    if (i>0 and (self.land[i-1][j].type == type1 or self.land[i-1][j].type == type2)):
                        surround = surround + 1
                    if (i < 49 and (self.land[i+1][j].type == type1 or self.land[i+1][j].type == type2)):
                        surround = surround + 1
                    if (j > 0 and (self.land[i][j-1].type == type1 or self.land[i][j-1].type == type2)):
                        surround = surround + 1
                    if (j < 49 and (self.land[i][j+1].type == type1 or self.land[i][j+1].type == type2)):
                        surround = surround + 1
                    if (surround > 0):
                        if (i>0 and (self.land[i-1][j].type == type1 or self.land[i-1][j].type == type2)):
                            self.land[i-1][j].relProbs += self.land[i][j].relProbs/surround
                        if (i < 49 and (self.land[i+1][j].type == type1 or self.land[i+1][j].type == type2)):
                            self.land[i+1][j].relProbs += self.land[i][j].relProbs/surround
                        if (j > 0 and (self.land[i][j-1].type == type1 or self.land[i][j-1].type == type2)):
                            self.land[i][j-1].relProbs += self.land[i][j].relProbs/surround
                        if (j < 49 and (self.land[i][j+1].type == type1 or self.land[i][j+1].type == type2)):
                            self.land[i][j+1].relProbs += self.land[i][j].relProbs/surround
                        self.land[i][j].relProbs = 0.0
                    else:
                        extra += self.land[i][j].relProbs
                        self.land[i][j].relProbs = 0.0
        if ( extra != 0.0):
            nonEmpty = 0.0
            for i in range(50):
                for j in range(50):
                    if ( self.land[i][j].relProbs != 0.0):
                        nonEmpty += 1
            for i in range(50):
                for j in range(50):
                    if ( self.land[i][j].relProbs != 0.0):
                        self.land[i][j].relProbs = self.land[i][j].relProbs * (1.0 + (extra/nonEmpty))
        if(type == "type1"):
            rc = self.pickLocation()
        else:
            rc = self.pickLocation2()
    
        return rc
        
    def pickLocation2(self):
        rc = [None, None]
        nextLocation = 0.0
        for i in range(50):
            for j in range(50):
                s = self.land[i][j].prob
                self.beliefs[i][j] = s * self.land[i][j].relProbs
                if (nextLocation < self.beliefs[i][j]):
                    nextLocation = self.beliefs[i][j]
                    rc = [i, j]
        return rc
        
    def pickCurrentLocation(self):
        rc = [0,0]
        nextLoc = 0.0
        distance = 0.0
        d = 0
        for i in range(50):
            for j in range(50):
                distance = abs((i - self.currentLoc[0])) + abs((j - self.currentLoc[1]))
                if (nextLoc < self.land[i][j].relProbs * self.land[i][j].prob/(distance + 1.0)):
                    nextLoc = (self.land[i][j].relProbs * self.land[i][j].prob/(distance + 1.0))
                    rc = [i, j]
                    d = int(distance)
        self.currentLoc[0] = rc[0]
        self.currentLoc[1] = rc[1]
        return rc
        
    def moveTarget(self):
        rand = random.uniform(0, 1)
        tempC = self.targetC
        tempR = self.targetR
        if (self.targetR > 0 and self.targetR < 49 and self.targetC > 0 and self.targetC < 49):
            if (rand <= 0.25):
                tempR = self.targetR -1
            elif (rand > 0.25 and rand <= 0.5):
                tempC = self.targetC -1
            elif (rand > 0.5 and rand <= 0.75):
                tempC = self.targetC+1
            elif (rand > 0.75):
                tempR = self.targetR + 1
        elif (self.targetR > 0 and self.targetR < 49):
            if (rand <= 0.33 and self.targetC == 0):
                tempC = self.targetC +1
            elif (rand <= 0.33 and self.targetC == 49):
                tempC = self.targetC -1
            elif (rand > 0.33 and rand <= 0.66):
                tempR = self.targetR-1
            else:
                tempR = self.targetR + 1
        elif (self.targetC > 0 and self.targetC < 49):
            if (rand <= 0.33 and self.targetR == 0):
                tempR = self.targetR +1
            elif (rand <= 0.33 and self.targetR == 49):
                tempR = self.targetR -1
            elif (rand > 0.33 and rand <= 0.66):
                tempC = self.targetC-1
            else:
                tempC = self.targetC +1
        else:
            if (self.targetR == 0 and self.targetC == 0):
                if (rand <= 0.5):
                    tempR = self.targetR + 1
                else:
                    tempC = self.targetC + 1
            elif (self.targetR == 0 and self.targetC == 49):
                if (rand <= 0.5):
                    tempR = self.targetR + 1
                else:
                    tempC = self.targetC - 1
            elif (self.targetR == 49 and self.targetC == 0):
                if (rand <= 0.5):
                    tempR = self.targetR - 1
                else:
                    tempC = self.targetC + 1
            else:
                if (rand <= 0.5):
                    tempR = self.targetR - 1
                else:
                    tempC = self.targetC - 1
        self.land[self.targetR][self.targetC].target = False;
        firstType = self.land[self.targetR][self.targetC].type
        self.targetR = tempR
        self.targetC = tempC
        self.land[self.targetR][self.targetC].target = True;
        lastType = self.land[self.targetR][self.targetC].type
        return [firstType, lastType]
        
    def foundTarget(self, row, col):
        if (self.land[row][col].target and self.land[row][col].prob >= random.uniform(0, 1)):
            return True
        else:
            return False
            
    def updateBelief(self, row ,col):
        rb = self.land[row][col].relProbs
        p = self.land[row][col].prob
        op = 1-rb
        for i in range(50):
            for j in range(50):
                if (i != row and j != col):
                    self.land[i][j].relProbs = self.land[i][j].relProbs + (rb * p)*(self.land[i][j].relProbs/op)
        self.land[row][col].relProbs = rb*(1.0-p);
        
    def rule1(self):
        for count in range(250000):
            rc = self.pickLocation()
            if(self.foundTarget(rc[0], rc[1])):
                print("Target Found: [" + str(rc[0]) + ", " + str(rc[1]) + "]  |  Actual Location: [" + str(self.targetR) + ", " + str(self.targetC) + "]")
                print()
                return count
            else:
                self.updateBelief(rc[0],rc[1])
                
        return 250000
                
    def rule2(self):
        self.beliefs= [[0.0 for i in range(50)] for j in range(50)]
        for count in range(250000):
            rc = self.pickLocation2()
            if(self.foundTarget(rc[0], rc[1])):
                print("Target Found: [" + str(rc[0]) + ", " + str(rc[1]) + "]  |  Actual Location: [" + str(self.targetR) + ", " + str(self.targetC) + "]")
                print()
                return count
            else:
                self.updateBelief(rc[0],rc[1])
        return 250000
                
    def type1(self):
        for x in range(250000):
            rc = self.pickTypeLocation("type1")
            if(self.foundTarget(rc[0], rc[1])):
                print("Target Found: [" + str(rc[0]) + ", " + str(rc[1]) + "]  |  Actual Location: [" + str(self.targetR) + ", " + str(self.targetC) + "]")
                print()
                return x
        return 250000
    
    def type2(self):
        self.beliefs= [[0.0 for i in range(50)] for j in range(50)]
        for x in range(250000):
            rc = rc = self.pickTypeLocation("type2")
            if(self.foundTarget(rc[0], rc[1])):
                print("Target Found: [" + str(rc[0]) + ", " + str(rc[1]) + "]  |  Actual Location: [" + str(self.targetR) + ", " + str(self.targetC) + "]")
                print()
                return x
        return 250000
                
    def currentLocation(self):
        self.currentLoc = [0,0]
        d = 0
        
        for x in range(250000):
            rc = self.pickCurrentLocation()
            if(self.foundTarget(rc[0], rc[1])):
                print("Target Found: [" + str(rc[0]) + ", " + str(rc[1]) + "]  |  Actual Location: [" + str(self.targetR) + ", " + str(self.targetC) + "]")
                print()
                return x
            else:
                self.updateBelief(rc[0], rc[1])
        return 250000
                
    def stats(self):
        rule1 = 0.0
        rule2 = 0.0
        moving1 = 0.0
        moving2 = 0.0
        locCount = 0.0
        for x in range(50):
            print("Testing Rule 1 - " + str((x+1)))
            self.targetR = random.randint(0,50)
            self.targetC = random.randint(0,50)
            self.land = self.populateLand()
            rule1 += self.rule1()
        
        for x in range(50):
            print("Testing Rule 2 - " + str((x+1)))
            self.targetR = random.randint(0,50)
            self.targetC = random.randint(0,50)
            self.land = self.populateLand()
            rule2 += self.rule2()
        
        for x in range(50):
            print("Testing Moving Type 1 - " + str((x+1)))
            self.targetR = random.randint(0,50)
            self.targetC = random.randint(0,50)
            self.land = self.populateLand()
            moving1 += self.type1()
        
        for x in range(50):
            print("Testing Moving Type 2 - " + str((x+1)))
            self.targetR = random.randint(0,50)
            self.targetC = random.randint(0,50)
            self.land = self.populateLand()
            moving2 += self.type2()
        
        for x in range(50):
            print("Testing Current Location - " + str((x+1)))
            self.targetR = random.randint(0,50)
            self.targetC = random.randint(0,50)
            self.land = self.populateLand()
            locCount += self.type2()
        print("Rule 1 average number of moves: " + str(rule1/50))
        print("Rule 2 average number of moves: " + str(rule2/50))
        print("Type 1 average number of moves: " + str(moving1/50))
        print("Type 2 average number of moves: " + str(moving2/50))
        print("Current Location average number of moves: " + str(locCount/50))
            
                
    def printLand(self, landscape):
        for i in range(50):
            for j in range(50):
                print(landscape[i][j].toString())

                     
    
    
            
        
        
        
        
        
        
        
        
        
#initialize 50 x 50 2d list to represent the landscape
landscape= [[0 for i in range(50)] for j in range(50)]


#current search iteration
searchNum = 0
distanceTraveled = 0




print("-----Stationary Search-----")
print("-----Rule 1-----")
landscape = search(landscape).populateLand()
search(landscape).rule1()
print("-----Rule 2-----")
search(landscape).rule2()
print("-----Moving Search-----")
print("-----Type 1-----")
search(landscape).type1()
print("-----Type 2-----")
search(landscape).type2()
print("-----Current Location Search-----")
search(landscape).currentLocation()
print("-----Statitistics-----")
search(landscape).stats()

    