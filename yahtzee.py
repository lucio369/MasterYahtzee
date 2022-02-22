#@PydevCodeAnalysisIgnore
from random import randint
from pip._internal import self_outdated_check
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
    
    def roll(self,*args):#rolls dice and allows for specific dice to be rolled
        if len(args)>0:#!!!!!!!!!!!!!!!!!!!
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

if __name__=='__main__':#only run if not imported
    gameLoopFlag=True
    
    objList=[]#creating object group
    for i in range(1):
        objList.append(Player(i))
        
    while gameLoopFlag: # game loop
        
        print(objList[0].outScore())#output player's score card
        
        objList[0].roll()#initial roll
        
        quickLoop=True#Loop to analyse input for validity
        while quickLoop:
            
            print('\n{}'.format(objList[0].rolls))#output rolls and have users input what (if any) they want to change
            cutlist=list(input('Enter the indexes of rolls you wish to change:\n').strip())
            
            badChar=False#check if user input appropriate integers
            for index in cutlist:
                try:
                    index=int(index)
                    if index in range(0,5):
                        quickLoop=False
                    else:
                        print("That's not 0-4")
                except ValueError:
                    badChar=True
                    quickLoop=True
            if badChar:
                print('Inappropriate character')
                
            else:#roll accordingly and check if any rolls remaining if required
                rollstatus=objList[0].roll(cutlist)
                if rollstatus==False:
                    quickLoop=False
                    print('\n\n{}'.format(objList[0].rolls))
                else:
                    quickLoop=True
                
        quickLoop=True#Loop to analyse input for dictionary checking for validity
        while quickLoop:
            
            key=input('Enter the key of the dictionary item you want to change:')
            if key in objList[0].scoreCard:
                if objList[0].scoreCard[key]==-1:
                    quickLoop=False
                    
        objList[0].allocateScore(key)#score allocation
        
        objList[0].allocateScore('"Total Score')#checks if scorecard is complete
        if objList[0].scoreCard['"Total Score']!=-1:
            gameLoopFlag=False
            
            for i in objList[0].scoreCard:#outputs scorecard
                print(i,objList[0].scoreCard[i])
                
        objList[0].allocateScore('"Sum')#checks if sum and bonus can be auto-filled due to completions of their dependencies
        objList[0].allocateScore('"Bonus')
        
        objList[0].rollPrep()#resets dice for next round
        
    print('\n\n============================================================================\n\nYou scored:',objList[0].scoreCard['"Total Score'],'\n\nThanks for playing')#termination message
    
