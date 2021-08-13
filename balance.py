"""
DotaU Lobby Balancer
"""

from player import Player
import itertools as itt

def initPlayerList():
    """
    TODO: Find some way to input the list of players, possibly through DotaU bot or just a GUI.
    """
    return [None]*10

def basicScore(perm):
    """
    This can be used on partial permuatations for pruning
    """
    pen = 0
    if len(perm) <= 5:
        return 10. - sum((i + 1 not in perm[i].pos) for i in range(len(perm)))
    else:
        radiant, dire = perm[:5], perm[5:]
        r_pen = sum((i + 1 not in radiant[i].pos) for i in range(5))
        d_pen = sum((i + 1 not in dire[i].pos) for i in range(len(perm)-5))
        return 10. - (r_pen + d_pen)

def fullScore(perm):
    """
    For scoring full permutations
    """
    assert(len(perm) == 10)

    radiant, dire = perm[:5], perm[5:]

    # number of players in incorect position
    r_pen = sum((i + 1 not in radiant[i].pos) for i in range(5))
    d_pen = sum((i + 1 not in dire[i].pos) for i in range(5))

    # same as above, but weighted for number of positions selected and tier of player
    r_weighted_pen = sum((i + 1 not in radiant[i].pos) * len(radiant[i].pos) * (5 - radiant[i].tier) for i in range(5))
    d_weighted_pen = sum((i + 1 not in dire[i].pos) * len(dire[i].pos) * (5 - dire[i].tier) for i in range(5))

    # sum of tiers per team
    r_score = sum(player.tier for player in radiant)
    d_score = sum(player.tier for player in dire)
    bal_score = abs(r_score - d_score) / 4.

    # difference in lane tiers
    top_var = abs(radiant[2].tier + radiant[3].tier - dire[0].tier - dire[4].tier)
    mid_var = abs(radiant[1].tier - dire[1].tier)
    bot_var = abs(radiant[0].tier + radiant[4].tier - dire[2].tier - dire[3].tier)

    lane_score = max(max(top_var, mid_var * 2), bot_var) / 4.

    # some magic numbers here to determine the "balance" of the teams
    return 10. - bal_score - lane_score - ((r_pen + d_pen) * 0.9) - ((r_weighted_pen + d_weighted_pen) * 0.01)


def balance(player_list):
    """
    Input: List of 10 Players
    Output: Two lists, Radiant and Dire, each with 5 Players, and the balance score

    Will try to put each player in a position they marked.  Will rather put 1 player in incorrect position than
    let overall difference in tiers be more than 3, or difference in mid tiers more than 1.  If exact positions
    not possible, will give priority to those who selected more positions.
    """
    if len(player_list) != 10:
        print('Requires list of 10 Players')
        return [], [], 0.

    radiant_best, dire_best = [], []
    score = 0.

    for perm in itt.permutations(player_list):

        radiant, dire = perm[:5], perm[5:]

        if basicScore(perm) < score:
            continue

        perm_score = fullScore(perm)
        if perm_score > score:
            radiant_best = list(player.name for player in radiant)
            dire_best = list(player.name for player in dire)
            score = perm_score

    return radiant_best, dire_best, score



if __name__ == '__main__':

    # player_list = initPlayerList(?)

    test1 = [
        Player("a", [1, 2], 3),
        Player("b", [3], 2),
        Player("c", [1, 4, 5], 1),
        Player("d", [2, 3], 3),
        Player("e", [5], 3),
        Player("f", [2, 4, 5], 1),
        Player("g", [2, 3, 5], 2),
        Player("h", [4], 3),
        Player("i", [1], 1),
        Player("j", [2, 4], 2),
    ]

    test2 = [
        Player("a", [2, 3], 4),
        Player("b", [2, 3], 2),
        Player("c", [1, 4], 3),
        Player("d", [1, 4], 3),
        Player("e", [1, 4], 3),
        Player("f", [1, 4], 3),
        Player("g", [3, 4], 3),
        Player("h", [3, 4], 3),
        Player("i", [4, 5], 3),
        Player("j", [4, 5], 3),
    ]

    print(balance(test1))
    print(balance(test2))

