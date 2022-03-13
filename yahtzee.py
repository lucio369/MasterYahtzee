#@PydevCodeAnalysisIgnore
from random import randint

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
        self.tempConstructor()
        for v in vs:
            self.total+=v
            try:
                self.val_dict[v]+=1
            except KeyError:
                self.val_dict.update({v:1})
    
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
        return self.scoreCard['"Total Score']
    
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

def createObjectGroup(x):#OBJECT GROUP GENERATION OF (X) PLAYERS
    return [Player(i) for i in range(x)]#creating object group

def outputScore(x,sc):#OUTPUT PLAYER (X) SCORE
    msg='Player {}\n\n{}'
    return msg.format(x+1,sc)

def rollIndexCheck(x):#CHECKS IF INPUT ONLY HAS INTEGERS IN RANGE(0-4) 
    for i in x:
        if not i.isnumeric():
            return True
        if i not in range(0,4):
            return True
    return False

def rollAndTerminate(i,cl):#ROLLS ANYTHING IN (CL) FOR EACH (I)
    if i.roll(cl)==False:
        print('\n{}'.format(i.rolls))
        return False
    else:
        return True

def checkKeyInDict(i):#RETURNS PRESENSE OF (X) IN (I) DICT AND (X) INPUT
    x=input('Enter the key of the dictionary item you want to change:\n')
    try:
        if i[x]==-1:
            return False,x
    except KeyError:
        pass
    return True,x

def scoreCardCheck(i):#CHECKS IF TOTAL SCORE IS CALCULATED IN OBJECT (I) AND RETURNS THE GAME LOOP FLAG STATUS
    if topPlayer[1]<i.allocateScore('"Total Score')!=-1:
        topPlayer=[playerIndex,i.scoreCard['"Total Score']]
        if playerIndex==len(objList):
            playerIndex=0
            objList.pop()
        else:
            objList.pop()
        if len(objList)==0:
            return False
    return True

def gameLoop():
    objList,playerIndex=createObjectGroup(2),0#creating object group
    
    topPlayer=[0,0]#initialising top score measure list
    
    gameLoopFlag=True
    while gameLoopFlag: # game loop
        
        print(outputScore(playerIndex,objList[playerIndex].outScore()))#output score card
        
        objList[playerIndex].roll()#initial roll
        
        quickLoop=True#Loop to analyse input for validity
        while quickLoop:
            
            print('\n{}'.format(objList[playerIndex].rolls))#output rolls and have users input what (if any) they want to change
            
            cutlist=list(input('Enter the indexes of rolls you wish to change:\n'))#Input formatting
            
            quickLoop=rollIndexCheck(cutlist)#check if input appropriate integers
                
            if not quickLoop:quickLoop=rollAndTerminate(objList[playerIndex],cutlist)#rolls unless no input or out of rolls
                
        quickLoop=True#Loop to analyse input for dictionary checking for validity
        while quickLoop:
            
            quickLoop,key=checkKeyInDict(objList[playerIndex].scoreCard)#checks vacancy and presence of key in dictionary
        
        objList[playerIndex].allocateScore('"Sum')#auto fills sum and bonus
        objList[playerIndex].allocateScore('"Bonus')
        
        objList[playerIndex].rollPrep()#resets dice for next round
        
        gameLoopFlag=scoreCardCheck(objList[playerIndex])#score allocation

if __name__=='__main__':#only run if not imported
    topPlayer=gameLoop()

print('\n\nPlayer {} wins with {} points!'.format(topPlayer[0],topPlayer[1]))
    
