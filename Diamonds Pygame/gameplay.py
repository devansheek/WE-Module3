import random
from strategies import DiamondsPlayer, Deck

class DiamondsGame:
  def __init__(self, num_players=2):
    self.num_players = num_players
    self.players = [DiamondsPlayer(suit) for suit in ["Spades", "Hearts", "Clubs"]]  # Create AI players
    self.deck = Deck()  # Create a deck
    self.revealed_diamonds = []
    self.current_player = 0  # Track current player index

  def deal_cards(self):
    for player in self.players:
      player.hand = random.sample(self.deck.cards, 13)  # Deal 13 cards randomly
      self.deck.cards = [card for card in self.deck.cards if card not in player.hand]

  def play_round(self):
    revealed_diamond = self.deck.draw_card().value
    self.revealed_diamonds.append(revealed_diamond)

    bids = []
    for i in range(self.num_players):
      player_index = (self.current_player + i) % self.num_players  # Handle round-robin turns
      if player_index == 0:  # Human player turn (handled by GUI)
        bid = None  # Placeholder for human player bid (set by GUI)
      else:
        bid = self.players[player_index].bid(revealed_diamond)
      bids.append(bid)

    # Determine winner of the round based on bids (not implemented here)

    # Update players' hands and opponent history
    for i, player in enumerate(self.players):
      if bids[i] is not None:
        player.update_hand(bids[i])
      if i > 0:  # Update opponent history for AI players (except first player)
        player.update_opponent_history(bids[0])  # Assuming human is player 0

    self.current_player = (self.current_player + 1) % self.num_players

  def check_game_over(self):
    for player in self.players:
      if not player.hand:
        return True
    return False

  def get_game_info(self):
    # Prepare game information for display in GUI (modify as needed)
    info = f"Revealed Diamonds: {', '.join(str(d) for d in self.revealed_diamonds)}"
    for i, player in enumerate(self.players):
      info += f"\nPlayer {i+1} ({player.suit}): {len(player.hand)} cards"
    return info
