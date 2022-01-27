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
            '£Chance':-1,            '$Yahtzee':-1,
            '"Total Score':-1}
        self.tempConstructor()
        
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
    
    def allocateScore(self,key, vals):
        try:
            if self.scoreCard[key]!=-1:
                return
        except KeyError:
            return
        if key[:1]=='!':#1-6
            total=0
            for v in vals:
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
            self.valueCalculator(vals)
            if required_count > max(list(self.val_dict.values())):
                self.total=0
            self.scoreCard[key]=self.total
        elif key[:1]=='$':#full house, small straight, large straight, yahtzee
            if key[1:]=='Full House':
                score=25
                self.valueCalculator(vals)
                if 2 not in list(self.val_dict.values()):
                    if 3 not in list(self.val_dict.values()):
                        score=0
                self.scoreCard[key]=score
            elif key[1:]=='Small Straight':
                self.scoreCard[key]=self.streakCount(25,4,vals)
            elif key[1:]=='Large Straight':
                self.scoreCard[key]=self.streakCount(40,5,vals)
            elif key[1:]=='Yahtzee':
                score=50
                self.valueCalculator(vals)
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
if __name__=='__main__':
    gameLoopFlag=True
    objList=[]
    for i in range(1): # creating object group
        objList.append(Player(i))
        
    while gameLoopFlag: # game loop
        rolls=[]
        for i in range(5):#dice generation
            rolls.append(randint(1,6))
        rolls.sort()
            
        for i in objList[0].scoreCard:#outputs scorecard
            print(i,objList[0].scoreCard[i])
        print('\n\n{}'.format(rolls))
        objList[0].allocateScore(input('Enter the key of the dictionary item you want to change:'),rolls)
        objList[0].allocateScore('"Total Score',rolls)
        if objList[0].scoreCard['"Total Score']!=-1:
            gameLoopFlag=False
            for i in objList[0].scoreCard:#outputs scorecard
                print(i,objList[0].scoreCard[i])
        objList[0].allocateScore('"Sum',rolls)
        objList[0].allocateScore('"Bonus',rolls)
    print('\n\n============================================================================\n\nYou scored:',objList[0].scoreCard['"Total Score'],'\n\nThanks for playing')
