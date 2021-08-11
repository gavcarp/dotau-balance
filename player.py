"""
Player Class
    Input: 10 Players

"""

class Player:
    
    def __init__(self, name_in, pos_in, tier_in):
        '''
        name: string
        pos: list[int (1-5)]
        tier: int (1-4)
        '''
        self.name = name_in
        self.pos = pos_in
        self.tier = tier_in