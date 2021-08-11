"""
DotaU Lobby Balancer
"""

from player import Player
import itertools as itt

def splitTeams(lst):
    """
    Returns all possible 5 player team combinations of lst
    Requires: len(lst) = 10
    """
    if len(lst) != 10:
        return
    else:
        first, rest = lst[0], lst[1:]
        # combinations that contain the first Player
        for in_, out in splitTeams(rest, 5 - 1):
            yield [first] + in_, out
        # combinations that do not contain the first Player
        for in_, out in splitTeams(rest, 5):
            yield in_, [first] + out

def initPlayerList():
    return [None]*10

def balance(player_list):
    """
    Input: List of 10 Players
    Output: Two lists, Radiant and Dire, each with 5 Players, and the balance score

    Will try to put each player in a position they marked.  Will rather put 1 player in incorrect position than
    let overall difference in tiers be more than 3, or difference in mid tiers more than 1.  If exact positions
    not possible, will give priority to those who selected more positions.
    """
    if len(player_list) != 10:
        return

    radiant_best, dire_best = [], []
    score = 0

    for perm in itt.permutations(player_list, 10):
        # split permutation into teams
        radiant, dire = perm[:5], perm[5:]

        # number of players in incorect position
        r_pen = sum((i + 1 not in radiant[i].pos) for i in range(5))
        d_pen = sum((i + 1 not in dire[i].pos) for i in range(5))

        if 10. - ((r_pen + d_pen) * 0.9) < score:
            continue

        # same as above, but weighted for number of positions selected
        r_weighted_pen = sum((i + 1 not in radiant[i].pos) * len(radiant[i].pos) for i in range(5))
        d_weighted_pen = sum((i + 1 not in dire[i].pos) * len(radiant[i].pos) for i in range(5))

        # sum of tiers per team
        r_score = sum(player.tier for player in radiant)
        d_score = sum(player.tier for player in dire)

        # difference in lane tiers
        top_var = abs(radiant[2].tier + radiant[3].tier - dire[0].tier - dire[4].tier)
        mid_var = abs(radiant[1].tier - dire[1].tier)
        bot_var = abs(radiant[0].tier + radiant[4].tier - dire[2].tier - dire[3].tier)

        lane_score = (top_var + (mid_var * 2) + bot_var) / 4.

        # some magic numbers here to determine the "balance" of the teams ! TODO: I'm not using r_score - d_score here??
        perm_score = 10. - lane_score - ((r_pen + d_pen) * 0.9) - ((r_weighted_pen + d_weighted_pen) * 0.01)

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

    # print(balance(test1))
    print(balance(test2))
