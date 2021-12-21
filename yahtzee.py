#@PydevCodeAnalysisIgnore
from random import randint
class Player:
    def __init__(self,ID):
        #! Addition of dice values
        #" User cannot assign
        #£ Constant score
        self.ID=ID
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
        self.skip=True
        
        
    def freshTurn(self):
        self.ignoreDiceList=[]
        self.rolls=0
        self.skip=False
        
    def turn(self):
        if self.rolls<3 and self.skip==False:
            self.rollDice()
        else:
            print('no reroll')
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
        
    def diceGen(self,roll):
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
        temp=[]
        for row in diceList:
            temp.append(''.join(row))
        return temp

def turnOutput(ps):
    disDice=''
    for i in range(0,3):disDice+=('  '.join(x[i] for x in ps))+'\n'
    msg='''
What'cha get?

{}
    
So...what'cha ganna do bout' it?
'''.format(disDice)
    return msg

if __name__=='__main__':
    objList=[]
    objIndex=0
    gameLoopFlag=True
    for i in range(1): # creating object group
        objList.append(Player(i))
    
    temp=[]
    for i in range(6): # roll generation
        temp.append(objList[0].diceGen(randint(1,6)))
        
    msg=turnOutput(temp)
    while gameLoopFlag: # game loop
        print(msg)
        input()
        print(turnOutput(temp))
        input()
    
'''
Steps for Yahtzee game-play

1. Swap turn
2. Roll dice and any amount of dice after for maximum of three times
3. Allocate
4. If no more points to allocate calculate winner and end game

'''