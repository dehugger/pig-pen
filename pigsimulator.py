import time
import random

class config:
    mating_cooldown = 20
    hunger_weight_loss = 2
    hunger_weight_gain = 3
    death_weight = 35
    death_age = 1000
    mating_age = 10
    max_days = 1000
    corn_range = range(5,25)

class game():

    def __init__(self):
        self.pigs = []
        self.corn = 0
        self.days = 0
        self.dead_pigs = 0
        print('Creating Intial Pigs')
        for x in range(1,10):
            new_pig = pig()
            self.pigs.append(new_pig)

    def gameLoop(self):
        while self.days <= config.max_days:
            self.days +=1
            print('Day: ', self.days)
            print(len(self.pigs), ' pigs are currently in the pen.')
            self.addCorn()
            print('There is ', self.corn, ' corn to feed them')
            self.pigsEat()
            self.pigsMate()
            self.pigsLifecycle()
            if self.days == 100:
                knife_pig = self.pickPig()
                knife_pig.knife_pig = True
            time.sleep(3)
        print(
            'Game Over!',
            self.dead_pigs, ' died during this game.',
            len(self.pigs), 'total live in the pen'
        )
        for pig in self.pigs:
            pig.pigStats()


    def pickPig(self, notThisOne = None):
        if notThisOne != None:
            pig = random.choice(self.pigs)
            if pig != notThisOne:
                return pig
            else:
                return self.pickPig(notThisOne = notThisOne)
        else:
            return random.choice(self.pigs)

    def pigsEat(self):
        print('Feeding time!')
        if len(self.pigs) <= self.corn:
            print('All the pigs got to eat.')
            while self.corn > 0:
                for pig in self.pigs:
                    pig.eat(1)
                    self.corn -= 1
        else:
            print('Pigs will have to fight for food.')
            for pig in self.pigs:
                pig.hunger -= 5
            while self.corn > 0:
                aggressor_pig = self.pickPig()
                defending_pig = self.pickPig(aggressor_pig)
                fight_winner = aggressor_pig.fight(defending_pig)
                fight_winner.fights_won += 1
                fight_winner.eat(1)
                #print('Pig Fight! ', fight_winner.name, ' has won!')
                self.corn -= 1

    def pigsMate(self):
        print('Pig Mating Season!')
        for pig in self.pigs:
            pig.mating_cooldown -= 1
            if pig.mating_cooldown <= 0:
                other_pig = self.pickPig(pig)
                new_pig = pig.mate(other_pig)
                if new_pig != None:
                    pig.mating_cooldown = config.mating_cooldown
                    #print('A new pig was born! Welcome ', new_pig.name)
                    self.pigs.append(new_pig)

    def pigsLifecycle(self):
        for pig in self.pigs:
            pig.lifecycle()
            if pig.dead == True:
                self.pigs.pop(self.pigs.index(pig))
                self.dead_pigs += 1
                if pig.knife_pig == True:
                    knife_pig = self.pickPig()
                    knife_pig.knife_pig = True


    def addCorn(self):
        self.corn += random.choice(config.corn_range)

class pig():

    def __init__(self):

        self.name = 'Pig_' + str(time.time())
        self.weight = 60 #starts at 60 lbs, under 50 has a chance to die
        self.age = 0
        self.gender = random.choice(['Male', 'Female'])
        self.mating_cooldown = 0
        self.hunger = 25 #starts at 25, 100 is full
        self.dead = False
        self.fights_won = 0
        self.babies = 0
        self.knife_pig = False

    def pigStats(self):
        print(self.name, ' stats')
        if self.knife_pig == True:
            print('I AM THE KNIFE PIG')
        print(
            'Age:' + str(self.age),
            'Weight:' + str(self.weight),
            'Hunger:' + str(self.hunger),
            'Fights Won:' + str(self.fights_won),
            'Babies:' + str(self.babies)
        )

    def lifecycle(self):
        self.age += 1
        if self.hunger <= 25:
            self.weight -= config.hunger_weight_loss
        if self.hunger >= 75:
            self.weight += config.hunger_weight_gain
        if self.age > config.death_age:
            if self.dead != True:
                self.dead = random.choice([True, False])
        if self.weight < config.death_weight:
            if self.dead != True:
                self.dead = random.choice([True, False])

        if self.dead == True:
            print(self.name, ' has died. final statistics:')
            self.pigStats()

    def eat(self, food):
        self.hunger += 5* food

    def fight(self, other_pig):
        fight_chances = [self, other_pig]
        if other_pig.weight >= self.weight:
            fight_chances.append(other_pig)
        else:
            fight_chances.append(self)

        fight_winner = random.choice(fight_chances)

        if self.knife_pig == True:
            fight_winner = self
        elif other_pig.knife_pig == True:
            fight_winner = other_pig

        return fight_winner

    def mate(self, other_pig):
        if self.gender != other_pig.gender:
            if self.age > config.mating_age and other_pig.age > config.mating_age:
                success = random.choice([True, False])
                if success == True:
                    self.babies += 1
                    return pig()
                else:
                    return None

def start_game():
    new_game = game()
    new_game.gameLoop()

start_game()