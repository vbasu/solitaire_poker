'''
solitaire_poker.py

plays a game of solitaire poker
Rules:

'''

from __future__ import print_function
import random

class Card():

    def __init__(self, index, rank_name=None, suit_name=None):
        self.suit_index_to_name = {0: 'C', 1:'D', 2:'H', 3:'S'}
        self.rank_index_to_name = {
                        0 : '2',
                        1 : '3',
                        2 : '4',
                        3 : '5',
                        4 : '6',
                        5 : '7',
                        6 : '8',
                        7 : '9',
                        8 : 'T',
                        9 : 'J',
                        10 : 'Q',
                        11 : 'K',
                        12 : 'A'}
        self.suit_name_to_index = {v : k for k, v in
                self.suit_index_to_name.iteritems()}
        self.rank_name_to_index = {v : k for k, v in
                self.rank_index_to_name.iteritems()}

        if not index is None:
            self.suit_index = index / 13
            self.rank_index = index % 13
            self.suit_name = self.suit_index_to_name[self.suit_index]
            self.rank_name = self.rank_index_to_name[self.rank_index]
        else:
            self.suit_name = suit_name
            self.rank_name = rank_name
            self.suit_index = self.suit_name_to_index[self.suit_name]
            self.rank_index = self.rank_name_to_index[self.rank_name]

class Solitaire_Poker():

    def __init__(self):
        self.deck = None
        self.player_hand = []
        self.dealer_hand = []

    def shuffle_deck(self):
        deck = range(51)
        random.shuffle(deck)
        self.deck = map(lambda x: Card(x), deck)

    def rule_specification(self):
        pass

    def deal(self):
        pass

    def evaluate_5_card_hand(self, hand):
        hand_ranks = {
                    "straight flush" : 9,
                    "four of a kind" : 8,
                    "full house" : 7,
                    "flush" : 6,
                    "straight" : 5,
                    "three of a kind" : 4,
                    "two pair" : 3,
                    "one pair" : 2,
                    "high card" : 1}

        hand_type = None
        tiebreaker = None

        hand = sorted(hand, key=lambda x: x.rank_index)
        rank_frequencies = {}
        for c in hand:
            if c.rank_index not in rank_frequencies:
                rank_frequencies[c.rank_index] = 1
            else:
                rank_frequencies[c.rank_index] += 1

        is_flush = True
        for i in [1,2,3,4]:
            if not hand[i].suit_name == hand[0].suit_name:
                is_flush = False
                break

        is_straight = True
        for i in [0,1,2,3]:
            if not hand[i].rank_index == i:
                is_straight = False
                break
        if not hand[4].rank_index == 12:
            is_straight = False
        elif is_straight:
            tiebreaker = [3]

        if not is_straight:
            is_straight = True
            for i in [0,1,2,3]:
                if not hand[i].rank_index == hand[i+1].rank_index-1:
                    is_straight = False
                    break

        if is_straight and is_flush:
            hand_type = "straight flush"
            if not tiebreaker:
                tiebreaker = [hand[4].rank_index]
            return hand_ranks[hand_type], tiebreaker
        elif is_flush:
            hand_type = "flush"
            tiebreaker = map(lambda x: x.rank_index, hand)
            tiebreaker.reverse()
            return hand_ranks[hand_type], tiebreaker
        elif is_straight:
            hand_type = "straight"
            if not tiebreaker:
                tiebreaker = [hand[4].rank_index]
            return hand_ranks[hand_type], tiebreaker

        if max(rank_frequencies.values()) == 4:
            hand_type = "four of a kind"
            tiebreaker = []
            quadruple = None
            single = None
            for r in rank_frequencies:
                if rank_frequencies[r] == 4:
                    quadruple = r
                if rank_frequencies[r] == 1:
                    single = r
            tiebreaker = [quadruple, single]

        elif max(rank_frequencies.values()) == 3:
            if min(rank_frequencies.values()) == 2:
                hand_type = "full house"
                tiebreaker = []
                triple = None
                double = None
                for r in rank_frequencies:
                    if rank_frequencies[r] == 3:
                        triple = r
                    if rank_frequencies[r] == 2:
                        double = r
                tiebreaker = [triple, double]

            else:
                hand_type = "three of a kind"
                tiebreaker = []
                triple = None
                kickers = []
                for r in rank_frequencies:
                    if rank_frequencies[r] == 3:
                        triple = r
                    else:
                        kickers.append(r)
                tiebreaker.append(triple)
                kickers.sort(reverse=True)
                tiebreaker += kickers

        elif max(rank_frequencies.values()) == 2:
            if len(rank_frequencies) == 3:
                hand_type = "two pair"
                tiebreaker = []
                doubles = []
                kickers = []
                for r in rank_frequencies:
                    if rank_frequencies[r] == 2:
                        doubles.append(r)
                    else:
                        kickers.append(r)
                doubles.sort(reverse=True)
                tiebreaker = doubles + kickers

            else:
                hand_type = "one pair"
                doubles = []
                kickers = []
                for r in rank_frequencies:
                    if rank_frequencies[r] == 2:
                        doubles.append(r)
                    else:
                        kickers.append(r)
                kickers.sort(reverse=True)
                print(doubles, kickers)
                tiebreaker = doubles + kickers

        else:
            hand_type = "high card"
            tiebreaker = map(lambda x: x.rank_index, hand)
            tiebreaker.reverse()

        print(hand_type, tiebreaker)
        return hand_ranks[hand_type], tiebreaker

    def evaluate_dealer_hand(self, hand):
        pass

def generate_subsets(S, k): #if k > len(S) this will blow up
    if k == 0:
        return [[]]
    if k == len(S):
        return [S]
    without_first_element = generate_subsets(S[1:], k)
    with_first_element = generate_subsets(S[1:], k-1)
    with_first_element = [k + [S[0]] for k in with_first_element]
    return with_first_element + without_first_element


def main():
    SP = Solitaire_Poker()
    hand = [Card(None, 'A', 'D'), Card(None, 'A', 'S'), Card(None, '5', 'D'),
            Card(None, '2', 'D'), Card(None, '4', 'D')]
    hand_rank, tiebreaker = SP.evaluate_5_card_hand(hand)
    print(hand_rank, tiebreaker)

if __name__ == "__main__":
    main()
