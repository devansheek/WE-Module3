import pygame
import os

BLACK = (255,255,255)
WHITE = (0,0,0)
GREY  = (50,50,50)
RED  = (207,0,0)

class Card:
  def __init__(self, value, suit):
    self.value = value  # Integer representing card value (2-14)
    self.suit = suit  # String representing card suit (e.g., "Spades")

  def __str__(self):
    return f"{self.get_rank()} of {self.suit}"

  def get_rank(self):
    rank_map = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
    return rank_map.get(self.value, str(self.value))

class DiamondsGUI:
  def __init__(self, game):
    self.game = game
    self.screen_width = 800
    self.screen_height = 600
    self.font = pygame.font.SysFont(None, 24)  # Font for text display
    self.text_color = (255, 255, 255)  # White text color
    self.background_color = (0, 0, 128)  # Dark blue background
    self.card_width = 100  # Width of a card image on screen
    self.card_height = 140  # Height of a card image on screen
    self.card_back_image = pygame.image.load("card_back.png").convert_alpha()  # Load card back image
    self.card_images = self.load_card_images()  # Dictionary mapping (value, suit) to card image

  def load_card_images(self):
    # Load card images (replace with your image paths)
    images = os.path.join("images")
    for value in range(2, 15):
      for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]:
        image_path = f"{value}{suit[0]}.png"
        images[(value, suit)] = pygame.image.load(image_path).convert_alpha()
    return images

  def draw_text(self, surface, text, x, y):
    text_obj = self.font.render(text, True, self.text_color)
    surface.blit(text_obj, (x, y))

  def draw_card(self, surface, card, x, y):
    if card is None:
      surface.blit(self.card_back_image, (x, y))
    else:
      surface.blit(self.card_images[(card.value, card.suit)], (x, y))

  def draw_game_info(self, surface):
    # Display revealed Diamonds, player hand sizes, etc. (modify as needed)
    y_pos = 20
    self.draw_text(surface, f"Revealed Diamonds: {', '.join(str(d) for d in self.game.revealed_diamonds)}", 10, y_pos)
    for i, player in enumerate(self.game.players):
      y_pos += 30
      self.draw_text(surface, f"Player {i+1} ({player.suit}): {len(player.hand)} cards", 10, y_pos)

  def draw_human_hand(self, surface):
    # Display human player's hand cards
    card_spacing = 20
    x_pos = (self.screen_width - len(self.game.players[0].hand) * self.card_width - (len(self.game.players[0].hand) - 1) * card_spacing) // 2
    y_pos = self.screen_height - self.card_height - 20
    for card in self.game.players[0].hand:
      self.draw_card(surface, card, x_pos, y_pos)
      x_pos += self.card_width + card_spacing

  def run_game(self):
    pygame.init()
    screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    pygame.display.set_caption("Diamonds Game")
    clock = pygame.time.Clock()
    running = True

    
