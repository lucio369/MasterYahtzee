import os
from dotenv import load_dotenv
from discord.ext import commands

from random import randint, choice, shuffle
from time import sleep


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

    def reqRoll(self):  # requesting input for rolls to change 1.a
        #print(f'Player {self.ID}\n\n{self.outScore()}')
        print(f'Input the rolls you wish to change```{self.rolls}```')

    def anlsRoll(self,msg): # analyses roll to check if input is appropriate (msg formatted as list of stripped string 1.b
        if len(msg) == 0:return True
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

    def reqAllocate(self):  # requesting input to allocate roll 2.a.i
        print(f'{self.outScore()}\n\nEnter the key of the dictionary item you wish to change')

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
        return objList[playerIndex].allocateScore('"Total Score'): 

    
def game():
    '''
    Stage 1:
    a. awaiting input for rolls to change
    b. analysing rolls and checking for remaining rolls (prompting input if has more rolls)
    Stage 2:
    a. awaiting input to determine what to allocate the roll to
       allocating appropriate score according to validity of rolls according to scorecard
    b. Score allocation
    '''
def game(objList, playerIndex, topPlayer, stage, fresh, raw_input, ignoreList):
    if stage == 0:
        if fresh is True:
            # output player's score card
            print('Player {}\n\n{}'.format(
                playerIndex+1, objList[playerIndex].outScore()))
            objList[playerIndex].roll()  # initial roll
            # output rolls and have users input what they want to change
            rMessage = '\n{}Enter the indexes of rolls you wish to change:\n'
            print(rMessage.format(objList[playerIndex].rolls))
            return objList, playerIndex, topPlayer, 0, False, ignoreList
        quickLoop = True
        cutlist = list(raw_input.strip())  # ignore the rest (we're cool)
        if len(cutlist) == 0:
            quickLoop = False
            return objList, playerIndex, topPlayer, 1, True, ignoreList

        if quickLoop:
            for index in cutlist:  # check if user input appropriate integers
                try:
                    rollError = True
                    if not int(index) in [x for x in range(5)]:
                        print("That's not 0-4")
                        break
                    rollError = False
                except ValueError:
                    print("That's not even an integer")
                    break
            if rollError is True:
                print('Enter the indexes of rolls you wish to change:\n')
                return objList, playerIndex, topPlayer, 0, False, ignoreList

        # roll accordingly and check if any rolls remaining if required
        quickLoop = objList[playerIndex].roll(cutlist)
        print('\n\n{}Enter the indexes of rolls you wish to change:\n'.format(
            objList[playerIndex].rolls))

        if quickLoop:
            return objList, playerIndex, topPlayer, 0, False, ignoreList
        return objList, playerIndex, topPlayer, 1, True, ignoreList
    elif stage == 1:
        if fresh is True:
            print('Enter the key of the dictionary item you want to change:')
            return objList, playerIndex, topPlayer, 1, False, ignoreList
            tOutput = ''
        if raw_input not in objList[playerIndex].scoreCard.keys():
            tOutput = '''
            Inappropriate key
            Enter the key of the dictionary item you want to change:
            '''
        elif objList[playerIndex].scoreCard[raw_input] != -1:
            tOutput = '''
            Inappropriate key
            Enter the key of the dictionary item you want to change:
            '''
        if tOutput != '':
            print(tOutput)
            return objList, playerIndex, topPlayer, 1, False, ignoreList

        objList[playerIndex].allocateScore(raw_input)  # score allocation

        # checks if sum and bonus can be auto-filled
        objList[playerIndex].allocateScore('"Sum')
        objList[playerIndex].allocateScore('"Bonus')

        objList[playerIndex].rollPrep()  # resets dice for next round

        # checks if scorecard is complete
        objList[playerIndex].allocateScore('"Total Score')
        if objList[playerIndex].scoreCard['"Total Score'] != -1:
            if topPlayer[1] < objList[playerIndex].scoreCard['"Total Score']:
                sCard = objList[playerIndex].scoreCard
                topPlayer = [playerIndex+1, sCard['"Total Score']]
            ignoreList.append(playerIndex)

        playerIndex = playerIndex+1  # changes player (if possible)
        if playerIndex not in range(0, len(objList)):
            if len(objList) == 0:
                topPlayer = tuple(topPlayer)
                return objList, playerIndex, topPlayer, 0, True, ignoreList
            playerIndex = 0
        return objList, playerIndex, topPlayer, 0, True, ignoreList

def main(players):
    '''
    setup initial parameters
    gameloop:
        break/continue if player finished
        run game for player
    '''
def main():
    gameLoopFlag = True
    players = 2
    oL = [Player(x) for x in range(players)]
    pI = 0
    tP = [0, 0]
    s = 0
    f = True
    rI = ''
    iL = []

    indexScript = []
    actionScript = [x for x in oL[0].scoreCard.keys() if '"' not in x]
    for i in range(len(actionScript)):
        temp = ''
        templ = [x for x in range(5)]
        for j in range(randint(0, 5)):
            tempi = choice(templ)
            temp = temp+'{}'.format(tempi)
            templ.remove(tempi)
        indexScript.append(temp)
        if temp != '':
            indexScript.append('')
    shuffle(indexScript)
    shuffle(actionScript)
    indexScript = indexScript*players
    actionScript = actionScript*players
    print('\n\n{}\n\n{}'.format(indexScript, actionScript))
    indexScript = iter(indexScript)
    actionScript = iter(actionScript)

    while gameLoopFlag:
        if pI in iL:
            if len(iL) == players:
                gameLoopFlag = False
                break
            else:
                while pI in iL:
                    pI = pI+1
                    if pI not in range(0, players):
                        pI = 0
        # objList, playerIndex, topPlayer
        oL, pI, tP, s, f, iL = game(oL, pI, tP, s, f, rI, iL)
        if type(tP) is tuple:
            gameLoopFlag = False
            continue
        if f is False:
            # rI=input()
            # for AI
            if pI == 0:
                rI = input()
                continue
            if s == 0:
                rI = next(indexScript)
            if s == 1:
                rI = next(actionScript)
            print(rI)
            # input()

            # Multiplayer w/ keyboard (uncomment 242 and comment out until 251)
            # Play with bots as well (leave 244 - 251 uncommented)
            # Play only with bots (comment out 244 - 246)


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
async def yahtzee(ctx, *players):
    playerString=' , '.join([x for x in players])
    await ctx.send(f'```Inviting players...\n{playerString} ```')
    
if __name__ == '__main__':  # only run if not imported
    bot.run(TOKEN)

# Have fun with embeds

'''
@bot.command()
async def x(ctx, *apple):
    await ctx.send('output')
'''
