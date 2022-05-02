import os
from dotenv import load_dotenv
from discord.ext import commands

from random import randint, choice, shuffle
from time import sleep
from itertools import cycle

class Player:
    def __init__(self, ID):  # init function for Player
        # ! Addition of dice values
        # " User cannot assign
        # £ Constant score
        self.ID = ID
        self.scoreCard = {
            '!1': -1,
            '!2': -1,
            '!3': -1,
            '!4': -1,
            
            '!5': -1,
            '!6': -1,
            '"Sum': -1,
            '"Bonus': -1,
            '£Three of a kind': -1,
            '£Four of a kind': -1,
            '$Full House': -1,
            '$Small Straight': -1,
            '$Large Straight': -1,
            '£Chance': -1,
            '$Yahtzee': -1,
            '"Total Score': -1}
        self.stage,self.fresh,self.complete=0, True, False
        self.tempConstructor()
        self.rollPrep()

    def rollPrep(self):  # resets temp round variables for roll method
        self.rolls = [-1, -1, -1, -1, -1]
        self.rollCount = 0

    def tempConstructor(self):  # resets round variables for value calculator
        self.val_dict = {}
        self.total = 0

    def valueCalculator(self, vs):  # counts values of dice instances
        self.tempConstructor()
        for v in vs:
            self.total += v
            try:
                self.val_dict[v] += 1
            except KeyError:
                self.val_dict[v] = 1

    def streakCount(self, score, streak, vs):  # counts instances of dice
        streakCount = 1
        streakRecord = 1
        for v in range(1, len(vs)):
            if vs[v-1] == vs[v]-1:
                streakCount = streakCount + 1
            elif vs[v-1] != vs[v]:
                streakCount = 1
            streakRecord = max(streakRecord, streakCount)
        if streakRecord < streak:
            score = 0
        return score

    def allocateScore(self, key):  # sets points according to roll conditions
        try:
            if self.scoreCard[key] != -1:
                print('used key')
                return False
        except KeyError:
            print('bad key')
            return False
        if key[:1] == '!':  # 1-6
            total = 0
            for v in self.rolls:
                if v == int(key[1:]):
                    total += v
            self.scoreCard[key] = total
        elif key[:1] == '£':  # three of a kind, four of a kind, chance
            if key[1:] == 'Three of a kind':
                required_count = 3
            elif key[1:] == 'Four of a kind':
                required_count = 4
            elif key[1:] == 'Chance':
                required_count = 0
            self.valueCalculator(self.rolls)
            if required_count > max(list(self.val_dict.values())):
                self.total = 0
            self.scoreCard[key] = self.total
        elif key[:1] == '$':  # fullHouse smallStraight largeStraight yahtzee
            if key[1:] == 'Full House':
                score = 25
                self.valueCalculator(self.rolls)
                if 2 not in list(self.val_dict.values()):
                    if 3 not in list(self.val_dict.values()):
                        score = 0
                self.scoreCard[key] = score
            elif key[1:] == 'Small Straight':
                self.scoreCard[key] = self.streakCount(25, 4, self.rolls)
            elif key[1:] == 'Large Straight':
                self.scoreCard[key] = self.streakCount(40, 5, self.rolls)
            elif key[1:] == 'Yahtzee':
                score = 50
                self.valueCalculator(self.rolls)
                if 5 not in list(self.val_dict.values()):
                    score = 0
                self.scoreCard[key] = score
        elif key[:1] == '"':  # Sum, Bonus, Total Score (automated)
            if key[1:] == 'Sum':
                if -1 not in list(self.scoreCard.values())[:6]:
                    diceValues = list(self.scoreCard.values())[:6]
                    self.scoreCard[key] = sum(diceValues)
            elif key[1:] == 'Bonus':
                if self.scoreCard['"Sum'] != -1:
                    score = 35
                    if self.scoreCard['"Sum'] < 63:
                        score = 0
                    self.scoreCard[key] = score
            elif key[1:] == 'Total Score':
                if -1 not in list(self.scoreCard.values())[6:-1]:
                    self.scoreCard[key] = sum(list(self.scoreCard.values())[6:-1])
                    return True
                return False

    def roll(self, *args):  # rolls specific (or not) dice to be rolled
        if len(args) > 0:
            args = args[0]

        for i in range(5):
            if str(i) in args:
                self.rolls[i] = -1
            if self.rolls[i] == -1:
                self.rolls[i] = randint(1, 6)
        self.rolls.sort()
        self.rollCount += 1
        if self.rollCount >= 3 or len(args) < 1:
            return False
        else:
            return True

    def outScore(self):  # outputs scorecard
        outMsg = ''
        for i in self.scoreCard:
            outMsg = outMsg+i+' '+str(self.scoreCard[i])+'\n'
        return outMsg

    def anlsRoll(self,msg): # analyses roll to check if input is appropriate (msg formatted as list of stripped string 1.b
        #if len(msg) == 0:return True
        try:
            for index in msg:
                if not int(index) in [x for x in range(5)]:
                    print('That isn\'t an available dice')
                    raise anlsErr
        except ValueError:
            print('That input isn\'t numeric')
            raise anlsErr
        except anlsErr:
            return False
        else:
            return True

    def chckScore(self,msg):    # allocating appropriate score according to scorecard 2.a.ii
        try:
            if msg not in self.scoreCard.keys():
                print('Inappropriate key')
                raise anlsErr
            elif self.scoreCard[msg] != -1:
                print('Points already allocated here')
                raise anlsErr
        except anlsErr:
            self.reqAllocate()
            return False
        else:
            self.allocateScore(msg)
            return True
        
    def autoAllocate(self): # allocate further points where possible 2.b
        objList[playerIndex].allocateScore('"Sum')
        objList[playerIndex].allocateScore('"Bonus')
        return objList[playerIndex].allocateScore('"Total Score')

    
def game(player,msg):
    '''
    Stage 1:
    a. awaiting input for rolls to change
    b. analysing rolls and checking for remaining rolls (prompting input if has more rolls)
    Stage 2:
    a. awaiting input to determine what to allocate the roll to
       allocating appropriate score according to validity of rolls according to scorecard
    b. Score allocation
    '''
    
    if stage == 0:
        if player.fresh == True:
            print(f'Input the rolls you wish to change```{player.rolls}```')
            player.fresh=False
        else:
            player.fresh=True
            if player.anlsRoll(msg):
                player.stage=1
    else:
        if player.fresh == True:
            print(f'{player.outScore()}\n\nEnter the key of the dictionary item you wish to change')
        else:
            player.fresh=True
            if player.chckScore(msg):
                player.stage=0
                if player.autoAllocate():
                    player.complete = True
                    return True
    return False
  
def main(p,msg):
    '''
    initial parameters (maybe having main and game functions in a class might be useful??)

    check if author is next in queue (whitelist)| Any player can go when they want
        OR
    check if author is still involved (whiteItem)| One at a time
    
    run game for author
    remove finished authors and add score to leaderboard
    if no authors remaining, reveal leaderboard
    '''
    if gm == 'y':
        print('hmm')
    print('ohh')
    

load_dotenv()  # reads bot token
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')  # creates discord client and runs it


@bot.event
async def on_ready():
    print(bot.user, 'is connected')  # status message for console


@bot.listen()
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    

@bot.command()
async def yahtzee(ctx, gm, *p):
    bot.whiteSet=set(p)
    bot.players=[Player(x) for x in range(len(p))]
    bot.itPlayers=iter(bot.players)
    bot.gm=gm
    await bot.main()##needs work
    
if __name__ == '__main__':  # only run if not imported
    bot.run(TOKEN)

# Have fun with embeds
