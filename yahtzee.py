#@PydevCodeAnalysisIgnore
from random import randint
class Player:
    def __init__(self,ID):
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
        
    def rollPrep(self):
        self.rolls=[-1,-1,-1,-1,-1]
        self.rollCount=0
        
    def tempConstructor(self):
        self.val_dict={}
        self.total=0
    
    def valueCalculator(self,vs):
        self.tempConstructor()
        for v in vs:
            self.total+=v
            try:
                self.val_dict[v]+=+1
            except KeyError:
                self.val_dict.update({v:1})
    
    def streakCount(self,score,streak,vs):
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
    
    def allocateScore(self,key):
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
    
    def roll(self,*args):
        print(args)
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
        
if __name__=='__main__':
    gameLoopFlag=True
    objList=[]
    for i in range(1): # creating object group
        objList.append(Player(i))
        
    while gameLoopFlag: # game loop
            
        for i in objList[0].scoreCard:#outputs scorecard
            print(i,objList[0].scoreCard[i])
        quickLoop=True
        objList[0].roll()
        while quickLoop:
            print('\n\n{}'.format(objList[0].rolls))
            cutlist=list(input('Enter the indexes of rolls you wish to change').strip())
            badChar=False
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
            elif objList[0].roll(cutlist)==False:
                quickLoop=False
                print('\n\n{}'.format(objList[0].rolls))
        quickLoop=True
        while quickLoop:
            key=input('Enter the key of the dictionary item you want to change:')
            if key in objList[0].scoreCard:
                if objList[0].scoreCard[key]==-1:
                    quickLoop=False
        objList[0].allocateScore(key)
        objList[0].allocateScore('"Total Score')
        if objList[0].scoreCard['"Total Score']!=-1:
            gameLoopFlag=False
            for i in objList[0].scoreCard:#outputs scorecard
                print(i,objList[0].scoreCard[i])
        objList[0].allocateScore('"Sum')
        objList[0].allocateScore('"Bonus')
        objList[0].rollPrep()
    print('\n\n============================================================================\n\nYou scored:',objList[0].scoreCard['"Total Score'],'\n\nThanks for playing')
