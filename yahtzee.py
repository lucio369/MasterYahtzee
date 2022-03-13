#@PydevCodeAnalysisIgnore
from random import randint
from time import sleep

class Player:
    def __init__(self,ID):#init function for Player
        #! Addition of dice values
        #" User cannot assign
        #£ Constant score
        self.ID=ID
        self.scoreCard={
            '!1':-1,
            '!2':-1,
            '!3':-1,
            '!4':-1,
            '!5':-1,
            '!6':-1,
            '"Sum':-1,
            '"Bonus':-1,
            '£Three of a kind':-1,
            '£Four of a kind':-1,
            '$Full House':-1,
            '$Small Straight':-1,
            '$Large Straight':-1,
            '£Chance':-1,            
            '$Yahtzee':-1,
            '"Total Score':-1}
        self.tempConstructor()
        self.rollPrep()
        
    def rollPrep(self):#resets temp round variables for roll method
        self.rolls=[-1,-1,-1,-1,-1]
        self.rollCount=0
        
    def tempConstructor(self):#resets temp round variables for value calculator
        self.val_dict={}
        self.total=0
    
    #NOTE: Isn't value calculator a kind of form of StreakCount? 
    def valueCalculator(self,vs):#counts values of dice instances
        print(vs)
        self.tempConstructor()
        for v in vs:
            self.total+=v
            try:
                self.val_dict[v]+=1
            except KeyError:
                self.val_dict[v]=1
    
    def streakCount(self,score,streak,vs):#counts instances of dice
        streakCount=1
        streakRecord=1
        for v in range(1,len(vs)):
            if vs[v-1]==vs[v]-1:
                streakCount=streakCount+1
            elif vs[v-1]!=vs[v]:
                streakCount=1
            streakRecord=max(streakRecord,streakCount)
        if streakRecord<streak:
            score=0
        print(streakRecord)
        return score
    
    def allocateScore(self,key):#allocates points according to how roll meets conditions
        try:
            if self.scoreCard[key]!=-1:
                return
        except KeyError:
            return
        if key[:1]=='!':#1-6
            total=0
            for v in self.rolls:
                if v == int(key[1:]):
                    total+=v
            self.scoreCard[key]=total
        elif key[:1]=='£':#three of a kind, four of a kind, chance
            if key[1:]=='Three of a kind':
                required_count=3
            elif key[1:]=='Four of a kind':
                required_count=4
            elif key[1:]=='Chance':
                required_count=0
            self.valueCalculator(self.rolls)
            if required_count > max(list(self.val_dict.values())):
                self.total=0
            self.scoreCard[key]=self.total
        elif key[:1]=='$':#full house, small straight, large straight, yahtzee
            if key[1:]=='Full House':
                score=25
                self.valueCalculator(self.rolls)
                if 2 not in list(self.val_dict.values()):
                    if 3 not in list(self.val_dict.values()):
                        score=0
                self.scoreCard[key]=score
            elif key[1:]=='Small Straight':
                self.scoreCard[key]=self.streakCount(25,4,self.rolls)
            elif key[1:]=='Large Straight':
                self.scoreCard[key]=self.streakCount(40,5,self.rolls)
            elif key[1:]=='Yahtzee':
                score=50
                self.valueCalculator(self.rolls)
                if 5 not in list(self.val_dict.values()):
                    score=0
                self.scoreCard[key]=score
        elif key[:1]=='"':#Sum, Bonus, Total Score (automated)
            if key[1:]=='Sum':
                if -1 not in list(self.scoreCard.values())[:6]:
                    self.scoreCard[key]=sum(list(self.scoreCard.values())[:6])
            elif key[1:]=='Bonus':
                if self.scoreCard['"Sum']!=-1:
                    score=35
                    if self.scoreCard['"Sum']<63:
                        score=0
                    self.scoreCard[key]=score
            elif key[1:]=='Total Score':
                if -1 not in list(self.scoreCard.values())[6:-1]:
                    self.scoreCard[key]=sum(list(self.scoreCard.values())[6:-1])
    
    def roll(self,*args):#rolls dice and allows for specific dice to be rolled
        if len(args)>0:
            args=args[0]
            
        for i in range(5):
            if str(i) in args:
                self.rolls[i]=-1
            if self.rolls[i]==-1:
                self.rolls[i]=randint(1,6)
        self.rolls.sort()
        self.rollCount+=1
        if self.rollCount>=3 or len(args)<1:
            return False
        else:
            return True
    
    
    def outScore(self):#outputs scorecard
        outMsg=''
        for i in self.scoreCard:
            outMsg=outMsg+i+' '+str(self.scoreCard[i])+'\n'
        return outMsg

aiScript=[['','!1'],['','!2'],['','!3'],['','!4'],['','!5'],['','!6'],
          ['','!Three of a kind'],['','!Four of a kind'],['','$Full House'],
          ['','$Small Straight'],['','$Large Straight'],['','£Chance'],
          ['','$Yahtzee']]
    
def gameLoop(objList, playerIndex, topPlayer, stage, fresh):    
    print('Player {}\n\n{}'.format(playerIndex+1,objList[playerIndex].outScore()))#output player's score card
    
    objList[playerIndex].roll()#initial roll
    
    print('\n{}'.format(objList[playerIndex].rolls))#output rolls and have users input what (if any) they want to change
    
    quickLoop=True#Loop to ensure valid input is eventually input
    while quickLoop:

        cutlist=list(input('Enter the indexes of rolls you wish to change:\n').strip())
        if len(cutlist)==0:
            quickLoop=False
            continue
        
        for index in cutlist:#check if user input appropriate integers
            try:
                rollError=True
                if not int(index) in [x for x in range(5)]:
                    print("That's not 0-4")
                    break
                rollError=False
            except ValueError:
                print("That's not even an integer")
                break
        if rollError==True:
            continue
        
        quickLoop=objList[playerIndex].roll(cutlist)#roll accordingly and check if any rolls remaining if required
        print('\n\n{}'.format(objList[playerIndex].rolls))
            
    quickLoop=True#Loop to analyse input for dictionary checking for validity
    while quickLoop:
        key=input('Enter the key of the dictionary item you want to change:')
        if not key in objList[playerIndex].scoreCard.keys() or not objList[playerIndex].scoreCard[key]==-1:
            print('Inappropriate key')
            continue
        quickLoop=False
    
    objList[playerIndex].allocateScore('"Sum')#checks if sum and bonus can be auto-filled due to completions of their dependencies
    objList[playerIndex].allocateScore('"Bonus')
                
    objList[playerIndex].allocateScore(key)#score allocation
    
    objList[playerIndex].rollPrep()#resets dice for next round
    
    skip=False
    objList[playerIndex].allocateScore('"Total Score')#checks if scorecard is complete
    if objList[playerIndex].scoreCard['"Total Score']!=-1:
        if topPlayer[1]<objList[playerIndex].scoreCard['"Total Score']:
            topPlayer=[playerIndex+1,objList[playerIndex].scoreCard['"Total Score']]
            objList.pop(playerIndex)
    
    playerIndex=playerIndex+1#changes player (if possible)
    if playerIndex not in range(0,len(objList)):
        if len(objList)==0:
            return objList,playerIndex,tuple(topPlayer), stage, False
        playerIndex=0
    return objList, playerIndex, topPlayer, stage, False

if __name__=='__main__':#only run if not imported
    gameLoopFlag=True
    oL,pI,tP,s,f=[Player(x) for x in range(1)],0,[0,0],0,True
    while gameLoopFlag:
        oL,pI,tP,s,f=gameLoop(oL,pI,tP,s,f)#objList, playerIndex, topPlayer
        if type(tP) is tuple:
            gameLoopFlag=False


print('\n\nPlayer {} wins with {} points!'.format(tP[0],tP[1]))
