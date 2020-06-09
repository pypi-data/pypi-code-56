import pandas as pd

from pyjack21.shoe import Shoe, Card, Rank, Suit
from pyjack21.player import Player, Hand

class BlackJackTable:
    def __init__(self, hands=1, decks=6, player_count=4,
                 payroll=None):
        self.hands_to_play = hands
        self.hands_played = 0
        self.players = []
        if payroll == None:
            payroll = []
            for i in range(player_count):
                payroll.append(500)

        for i in range(player_count):
            self.players.append(Player(payroll=payroll[i]))
        self.dealer = Player()
        self.deck_count = decks
        self.shoe = Shoe(self.deck_count)
        self.shoe.shuffle()
        self.shoe_threshold = len(self.players) * 6
        self.df = self.__initialize_data()

    def run(self):
        while self.hands_played < self.hands_to_play:
            self.play_hand()
            # self.output_table_status()

    def play_hand(self):

        self.wager()
        self.deal()
        hand = self.hands_played + 1

        dealer_card = self.dealer.dealer_card()

        # data collection
        # --------------------------------------
        self.df.loc[hand, 'dealer_card'] = dealer_card.char_rep()
        self.df.loc[hand, 'dealer_hand'] = self.dealer.hands[0].hand_value()
        for i in range(len(self.players)):
            self.df.loc[hand, f'hand_{i}'] = self.players[i].hands[0].hand_key()
        # --------------------------------------

        # handle dealer blackjack
        if self.dealer.hands[0].hand_value() == 21:
            # print(f'DEALER BLACKJACK!!!')
            for player in self.players:
                player.pay(0)

        else:
            # have each player play
            for i in range(len(self.players)):
                player = self.players[i]

                # check if player is playing
                if player.wager == 0:
                    continue

                # data collection
                self.df.loc[hand, f'init_move_{i}'] = player.move(self.shoe, player.hands[0], dealer_card)

                # first check for blackjack
                if player.move(self.shoe, player.hands[0], dealer_card) == "BLACKJACK":
                    player.pay(player.wager * 2.5)
                    player.wager = 0

                # then play hand
                self.__play_player_hand(player, 0, dealer_card)



            while self.dealer.hands[0].hand_value() < 17:
                self.dealer.hands[0].deal(self.shoe.deal())

            # print(f'DEALER: {self.dealer.hand_value()}')

            # data collection
            self.df.loc[hand, 'dealer_final_hand'] = self.dealer.hands[0].hand_value()
            
            # 
            for player in self.players:
                for i in range(len(player.hands)):
                    
                    # player bust
                    if player.hands[0].hand_value() > 21:
                        player.pay(0)
                    
                    # dealer bust
                    elif self.dealer.hands[0].hand_value() > 21:
                        player.pay(player.wager * 2)

                    # player hand higher    
                    if self.dealer.hands[0].hand_value() < player.hands[i].hand_value():
                        player.pay(player.wager * 2)
                    
                    # push
                    elif self.dealer.hands[0].hand_value() == player.hands[i].hand_value():
                        player.pay(player.wager)
                    
                    # player lost
                    else:
                        player.pay(0)

                player.wager = 0 # reset the player wagers

        for i in range(len(self.players)):
            self.df.loc[hand, f'payroll_{i}'] = self.players[i].payroll
            hand_earnings = self.df.loc[hand, f'payroll_{i}'] - self.df.loc[hand-1, f'payroll_{i}']
            self.df.loc[hand, f'hand_earnings_{i}'] = hand_earnings
            hand_result = ""
            if hand_earnings > 0:
                hand_result = "W"
            elif hand_earnings < 0:
                hand_result = "L"
            else:
                hand_result = "P"

            self.df.loc[hand, f'hand_result_{i}'] = hand_result

        self.clear_table()
        self.hands_played = self.hands_played + 1


    def wager(self):
        for player in self.players:
            player.bet()

    def deal(self):
        self.shoe.burn()
        card_hand = Hand()
        card_hand.deal(self.shoe.deal())
        card_hand.deal(self.shoe.deal())
        self.dealer.deal_hand(card_hand)
        for player in self.players:
            if player.wager != 0:
                card_hand = Hand()
                card_hand.deal(self.shoe.deal())
                card_hand.deal(self.shoe.deal())
                player.deal_hand(card_hand)

    def clear_table(self):
        self.dealer.hands = []
        for player in self.players:
            player.hands = []
        if self.shoe.cards_left() < self.shoe_threshold:
            self.shoe = Shoe(self.deck_count)
            self.shoe.shuffle()

    '''
    def output_table_status(self):
        # for player in self.players:
            # print(f'Player payroll: {player.payroll}')
    '''

    def __play_player_hand(self, player, hand_index, dealer_card): 
        while player.move(self.shoe, player.hands[hand_index], dealer_card) not in ["BUST", "S", "BLACKJACK"]:
            if player.move(self.shoe, player.hands[hand_index], dealer_card) == "H":
                player.hands[hand_index].deal(self.shoe.deal())
            elif player.move(self.shoe, player.hands[hand_index], dealer_card) == "D":
                player.hands[hand_index].deal(self.shoe.deal())
                if player.payroll >= player.wager:
                    player.payroll -= player.wager
                    player.wager = player.wager * 2
                    break
            elif player.move(self.shoe, player.hands[hand_index], dealer_card) == "P":
                if player.payroll >= player.wager:
                    card_hand = Hand()
                    card_hand.deal(player.hands[hand_index].hand.pop())
                    player.hands[hand_index].deal(self.shoe.deal())
                    card_hand.deal(self.shoe.deal())
                    player.hands.append(card_hand)
                    split_hand_index = len(player.hands) - 1
                    self.__play_player_hand(player, split_hand_index, dealer_card)

    def __initialize_data(self):
        df = pd.DataFrame()
        df.loc[0, 'dealer_card'] = 'NaN'
        df.loc[0, 'dealer_hand'] = 'NaN'
        df.loc[0, 'dealer_final_hand'] = 'NaN'
        for i in range(len(self.players)):
            player = self.players[i]
            df.loc[0, f'payroll_{i}'] = player.payroll
            df.loc[0, f'hand_{i}'] = 'NaN'
            df.loc[0, f'init_move_{i}'] = 'NaN' 
        return df

    def to_csv(self, csv):
        table.df.to_csv(csv)


if __name__ == "__main__":
    table = BlackJackTable(hands=500)
    table.run()
    print(table.df)
    table.to_csv('output.csv')

