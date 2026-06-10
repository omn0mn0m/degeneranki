import random

from .api import ambr
from .database import Database

# Based off https://www.hoyolab.com/article/497840
class GachaMachine:
    RATE_5_STAR = 0.006
    PITY_5_STAR = 73
    RATE_4_STAR = 0.051
    PITY_4_STAR = 8

    def __init__(self):
        self.data = Database()

        self.rarity_sorted_characters = ambr.sort_by_rarity(self.data.characters)
        self.rarity_sorted_weapons = ambr.sort_by_rarity(self.data.weapons)

    def roll(self):
        pull = {}

        # Add 1 roll and remove gacha points
        self.data.lifetime_rolls += 1

        x = random.random() # 0.0 <= prob < 1.0
        prob_5_star = self.RATE_5_STAR + max(0, ((self.data.pity_5_star + 1) - self.PITY_5_STAR) * 10 * self.RATE_5_STAR)
        prob_4_star = self.RATE_4_STAR + max(0, ((self.data.pity_4_star + 1) - self.PITY_4_STAR) * 10 * self.RATE_4_STAR)

        if x < prob_5_star:
            pull = random.choice(self.rarity_sorted_characters[5])
            self.data.add_owned_character(pull, 'genshin_impact')
            self.data.pity_5_star = 0
            self.data.pity_4_star += 1
        elif x < (prob_4_star + prob_5_star):
            if random.randint(0, 1):
                pull = random.choice(self.rarity_sorted_characters[4])
                self.data.add_owned_character(pull, 'genshin_impact')
            else:
                pull = random.choice(self.rarity_sorted_weapons[4])
                pull.name = 'Pity Fodder'

            self.data.pity_5_star += 1
            self.data.pity_4_star = 0
        else:
            pull = random.choice(self.rarity_sorted_weapons[3])
            pull.name = 'Pity Fodder'

            self.data.pity_4_star += 1
            self.data.pity_5_star += 1
        
        return pull
