import random

class DiamondsPlayer:
  def __init__(self, suit):
    self.suit = suit  # Spades, Hearts, or Clubs
    self.hand = list(range(2, 15))  # List of remaining cards (2-14)
    self.revealed_diamonds = []  # Track revealed Diamonds throughout the game
    self.opponent_history = []  # Optional: Track recent opponent bids (if allowed)

  def bid(self, revealed_diamond):
    self.revealed_diamonds.append(revealed_diamond)

    # Dynamic Bidding Threshold based on Diamond value and hand size
    bid_threshold = self.calculate_bid_threshold(revealed_diamond, len(self.hand))

    # Play strategically based on hand and situation
    return self.play_strategic_card(bid_threshold)

  def calculate_bid_threshold(self, revealed_diamond, hand_size):
    # Adjust threshold based on Diamond value and remaining cards
    base_threshold = max(2, 5 - (hand_size // 3))  # Higher threshold for fewer cards
    return base_threshold + revealed_diamond // 2

  def play_strategic_card(self, threshold):
    # Analyze hand and consider bluffing for high-value Diamonds
    candidate_cards = [card for card in self.hand if card >= threshold]

    # Prioritize High Cards for Very High Diamonds (Aces, Kings)
    if len(candidate_cards) > 1 and self.revealed_diamonds[-2:] == [14, 13]:
      return max(candidate_cards)

    # Analyze remaining Diamonds in deck (estimate based on revealed Diamonds)
    remaining_diamonds = set(range(2, 15)) - set(self.revealed_diamonds)
    high_value_diamonds_left = len(remaining_diamonds & set([11, 12, 13, 14]))

    # Bluffing Strategy (more likely for low competition and high potential reward)
    bluff_chance = 30  # Adjust this value (0-100) based on desired risk tolerance
    if len(candidate_cards) > 1 and high_value_diamonds_left > 1 and len(self.hand) > 5:
      # Consider opponent history (if available)
      if self.opponent_history and self.opponent_history[-1] > revealed_diamond + 2:
        bluff_chance = 50  # Increase bluff chance if opponent might be overbidding

      if random.randint(1, 100) <= bluff_chance:
        return random.choice(candidate_cards[:-1])

    # High-Value Window Strategy (prioritize bids within a value range)
    high_value_window = [11, 12, 13]  # Adjust this window based on game stage
    if revealed_diamond in high_value_window and candidate_cards[-1] not in high_value_window:
      return candidate_cards[-1]  # Sacrifice a slightly higher card for the window

    # Sacrifice Play for Very Valuable Diamonds
    if revealed_diamond >= 13 and len(candidate_cards) > 1 and high_value_diamonds_left >= 2:
      sacrifice_chance = 20  # Adjust this value (0-100) based on risk tolerance
      if random.randint(1, 100) <= sacrifice_chance:
        return max(candidate_cards)

    # Play a random card from remaining candidates
    return random.choice(candidate_cards)

  def update_hand(self, played_card):
    self.hand.remove(played_card)

  def update_opponent_history(self, opponent_bid):
    self.opponent_history.append(opponent_bid)  # Optional: Track opponent bids