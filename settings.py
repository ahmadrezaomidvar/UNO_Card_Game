import pygame
from rules import *
import random
import ptext
import os


class Requirements:
    """
    Class to create the requirements for the game
    """
    def __init__(self):
        self.players = [[], [], [], []]                         # list of players, can be extended to input number of players in future versions TODO
        self.game_status = ''
        self.main_deck = []                                     # storing cards in deck
        self.playing_deck = []                                  # storing cards in play
        self.current_card = []                                  # storing current cards
        self.color = ['Red', 'Green', 'Blue', 'Yellow']         # storing colors
        self.played = False                                     # storing if card was played
        self.drawn = False                                      # storing if card was drawn
        self.position = 1                                       # storing position of player
        self.direction_check = -1                               # storing direction of play
        self.winner = -1                                        # storing winner
        self.message = 'Dealing cards...'                       # storing message to be displayed
        self.winner_message = ''                                # storing winner message
        self.score_message = ''                                 # storing scores message
        self.player_is_playing = False                          # storing if player is playing
        self.drawn = False                                      # User play status
        self.time_to_wait = -1                                  # Lag status
        self.game_speed = 150                                   # Game speed
        self.special_check = 0                                  # Special card status
        self.color_change = False                               # Color change status
        self.bot_name_dict = {1: f'{Names().player_2_name}', \
                              2: f'{Names().player_3_name}', \
                              3: f'{Names().player_4_name}'}    # Bot names
        self.played_check = False                               # Playing deck status
        self.random = random.randint(6, 100)                    # Random number
        self.classic = True                                     # Classic game status
        self.variant_played = False                             # Variant game status
        self.variant_drawn = False                              # Variant game status
        self.bot_play_message = True                            # Bot play message status
        self.score_dict = {}                                    # Score dictionary
        for i in range(len(self.players)):
            self.score_dict[i] = 0
        self.shout_uno = [True]*4                               # Shout uno status
        self.uno_shout_chance = 0.1                             # Uno not shouting chance
        self.dynamic_graphic = False                            # Dynamic graphic status

class GameStatus:
    """
    Class to create the game status
    """
    def __init__(self):
        self.loading = 'loading'                             
        self.playing = 'playing'                            
        self.info = 'info'                                          
        self.winner = 'winner'                                

class Image:
    """
    Class to create the images for the game
    """
    def __init__(self):
        self.card_size = (77, 115)
        self.background = pygame.image.load('images/background.png')
        self.background_pos = (0, 0)
        self.home_screen = pygame.image.load('images/home_screen.png')
        self.home_screen_pos = (0, 0)    
        self.winner_screen = pygame.image.load('images/winner_screen.png')
        self.winner_screen_pos = (0, 0)
        self.home_button = pygame.image.load('images/home_button.png')
        self.home_button2 = pygame.image.load('images/home_button2.png')
        self.home_button1_pos = (0, 0, 114, 50)                              # Playing Home button
        self.home_button2_pos = (380, 500, 230, 106)                         # Winning Home button         
        self.home_button3_pos = (443, 630, 114, 50)                          # Info Home button 
        self.play_button = pygame.image.load('images/play_button.png')       
        self.play_pos = (330, 500, 330, 80)
        self.info_screen = pygame.image.load('images/info_screen.png')
        self.info_screen_pos = (0, 0)
        self.info_pos = (886, 0, 114, 50)
        self.info_button = pygame.image.load('images/info_button.png')
        self.arrow_pos = (400, 20, 600, 20, 400, 20)                       # (x1, x1_gap, x3, x3_gap, y1, y1_gap)  
        self.clockwise = pygame.image.load('images/clockwise.png')
        self.clockwise_pos = (420, 350)
        self.counter_clockwise = pygame.image.load('images/counter_clockwise.png')
        self.counter_clockwise_pos = (420, 190)
        self.card_back = pygame.image.load('images/card_back.png')
        self.card_back_pos = (270, 300, self.card_size[0], self.card_size[1])
        self.card_back_left = pygame.image.load('images/card_back_left.png')
        self.card_back_right = pygame.image.load('images/card_back_right.png')
        self.card_back_inverted = pygame.image.load('images/card_back_inverted.png')
        self.current_card_pos = (490, 280)
        self.playing_deck_pos = (460, 280)
        self.checked = pygame.image.load('images/checked.png')
        self.checked_pos = (780, 570, 90, 90)
        self.uno_button = pygame.image.load('images/uno_button.png')
        self.uno_button_pos = (880, 570, 90, 90)
        self.red = pygame.image.load('images/Small_Red.png')
        self.red_pos = (280, 500, 50, 50)
        self.green = pygame.image.load('images/Small_Green.png')
        self.green_pos = (335, 500, 50, 50)
        self.blue = pygame.image.load('images/Small_Blue.png')
        self.blue_pos = (390, 500, 50, 50)
        self.yellow = pygame.image.load('images/Small_Yellow.png')
        self.yellow_pos = (445, 500, 50, 50)
        self.line = pygame.image.load('images/line.png')
        
        player_images = ['images/player_1.png', 'images/player_2.png', 'images/player_3.png', 'images/player_4.png']
        random.shuffle(player_images)
        self.player_1 = pygame.image.load(player_images[0])
        self.player_1_pos = (120, 560)
        self.player_1_card_pos = (220, 60, 560)                     # (x, gap, y)
        self.player_cards_pos = (self.player_1_card_pos[0], self.player_1_card_pos[2], self.player_1_card_pos[1], self.card_size[1], self.player_1_card_pos[1])             # (x, y, width, height, gap)
        self.player_2 = pygame.image.load(player_images[1])
        self.player_2_pos = (830, 40)
        self.player_2_card_pos = (830, 160, 30)                     
        self.player_3 = pygame.image.load(player_images[2])
        self.player_3_pos = (280, 60)
        self.player_3_card_pos = (380, 30, 60)                     
        self.player_4 = pygame.image.load(player_images[3])
        self.player_4_pos = (60, 120)
        self.player_4_card_pos = (60, 250, 30)
        self.line1_pos = (self.player_1_pos[0]+9, self.player_1_pos[1]+90)
        self.line2_pos = (self.player_2_pos[0]+9, self.player_2_pos[1]+90)
        self.line3_pos = (self.player_3_pos[0]+9, self.player_3_pos[1]+90)
        self.line4_pos = (self.player_4_pos[0]+9, self.player_4_pos[1]+90)                     
            
class Names:
    """
    Class to create the names for the game
    """
    def __init__(self):
        self.font_name = 'font/BoldMarker-vmonA.ttf'
        self.font_size = 24
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.text_color = (56, 166, 224)
        self.player_1_text_pos = (Image().player_1_pos[0]+20, Image().player_1_pos[1]+90)
        self.player_2_text_pos = (Image().player_2_pos[0]+10, Image().player_2_pos[1]+90)
        self.player_3_text_pos = (Image().player_3_pos[0]+15, Image().player_3_pos[1]+90)
        self.player_4_text_pos = (Image().player_4_pos[0]+15, Image().player_4_pos[1]+90)
        self.player_1_name = 'You'                       #input('Enter your name: ')
        self.player_2_name = 'Chloe'
        self.player_3_name = 'Hong'
        self.player_4_name = 'Muda'
        self.playing_message_pos = (200, 500)
        self.winner_message_pos = (370, 100)
        self.score_message_pos = (50, 50)
        self.play_type_pos = ((Image().arrow_pos[0] + (Image().arrow_pos[2]-Image().arrow_pos[0])/3), Image().arrow_pos[4])
        self.left_arrow_pos = (Image().arrow_pos[0], Image().arrow_pos[4])
        self.right_arrow_pos = (Image().arrow_pos[2], Image().arrow_pos[4])