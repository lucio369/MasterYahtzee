#@PydevCodeAnalysisIgnore
from random import randint
class Player:
    def __init__(self):
        #! Addition of dice values
        #" User cannot assign
        #£ Constant score
        self.scoreCard={
            '!Ones':-1,
            '!Twos':-1,
            '!Threes':-1,
            '!Fours':-1,
            '!Fives':-1,
            '!Sixes':-1,
            '"Sum':-1,
            '"Bonus':-1,
            '!Three of a kind':-1,
            '!Four of a kind':-1,
            '£Full House':-1,
            '£Small straight':-1,
            '£Large straight':-1,
            '!Chance':-1,
            '£Yahtzee':-1,
            '"Total Score':-1}
        self.finalSum=False
        self.finalScore=False
        self.dice=[-1,-1,-1,-1,-1,-1]
        self.freshTurn()
        
    def freshTurn(self):
        self.ignoreDiceList=[]
        self.rolls=0
        
    def turn(self):
        self.freshTurn()
        self.rollDice()
        return self.dice
    
    def rollDice(self):
        self.rolls=self.rolls+1
        for die in range(0,len(self.dice)):
            if die not in self.ignoreDiceList:
                self.dice[die]=randint(1,6)
            
            
    
    def showCard(self):
        return self.scoreCard
    
    def diceSum(self):
        return sum(self.dice)
    
    def nonUserCalculations(self):
        if self.finalSum==False:
            if -1 not in list(self.scoreCard.values())[:6]:
                self.finalSum=True
                self.scoreCard['!Sum']=sum(list(self.scoreCard.values())[:6])
                if self.scoreCard['!Sum']>62:
                    self.scoreCard['!Bonus']=35
                else:
                    self.scoreCard=0
        elif self.finalScore==False:
            if -1 not in list(self.scoreCard.values())[6:-1]:
                self.finalScore=True
                self.scoreCard['!Total Score']=sum(list(self.scoreCard.values())[6:-1])
        
def diceGen(roll):
    diceList=[['-','-','-',],
              ['-','-','-',],
              ['-','-','-',]]
    if roll % 2 !=0:
        diceList[1][1]='0'
    if roll > 1:
        diceList[0][2]=diceList[2][0]='0'
    if roll > 3:
        diceList[0][0]=diceList[2][2]='0'
    if roll ==6:
        diceList[1][0]=diceList[1][2]='0'
    return diceList


if __name__=='__main__':
    p1 = Player()
    while p1.finalScore!=True:
        print(p1.turn())
        p1.finalScore=True

    print("Well played!")

        
'''
Steps for Yahtzee game-play

1. Swap turn
2. Roll dice and any amount of dice after for maximum of three times
3. Allocate
4. If no more points to allocate calculate winner and end game

'''