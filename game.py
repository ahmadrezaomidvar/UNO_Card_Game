import pygame
from rules import *
from settings import *
import random
import ptext
import os

class Game:
    """
    Class to create the game window
    """
    def __init__(self):
        self.pygame_init()
        self.screen = pygame.display.set_mode((1000, 700))
    
    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption('UNO-Developed by: COMP4008-Team-18')
        
    def quit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    def check_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
        return False
    
    def get_mouse_pos(self, event):
        return pygame.mouse.get_pos()

    def update_screen(self):
        pygame.display.update()

    def load_home_screen(self, req, image, names):
        self.screen.blit(image.home_screen, image.home_screen_pos)
        self.screen.blit(image.info_button, image.info_pos)
        self.screen.blit(image.play_button, image.play_pos)
        text = names.font.render("<", True, names.text_color)
        self.screen.blit(text, names.left_arrow_pos)
        text = names.font.render(">", True, names.text_color)
        self.screen.blit(text, names.right_arrow_pos)
        if req.classic:
            text = names.font.render("CLASSIC", True, names.text_color)
            self.screen.blit(text, names.play_type_pos)
        else:
            text = names.font.render("VARIANT", True, names.text_color)
            self.screen.blit(text, names.play_type_pos)

    def load_winner_screen(self, req, image, names):
        self.screen.blit(image.winner_screen, image.winner_screen_pos)
        text = names.font.render(req.winner_message, True, names.text_color)
        self.screen.blit(text, names.winner_message_pos)
        self.screen.blit(image.home_button2, image.home_button2_pos[0:2])
        ptext.draw(req.score_message, (names.score_message_pos), fontname=names.font_name, fontsize=names.font_size, color=names.text_color)

    def load_info_screen(self, image):
        self.screen.blit(image.info_screen, image.info_screen_pos)
        self.screen.blit(image.home_button, image.home_button3_pos[0:2])

    def load_base_images(self, req, image):
        self.screen.blit(image.background, image.background_pos)
        self.screen.blit(image.card_back, image.card_back_pos)
        self.screen.blit(image.home_button, image.home_button1_pos[0:2])
        if req.direction_check == 1:
            self.screen.blit(image.counter_clockwise, image.counter_clockwise_pos)
        else:
            self.screen.blit(image.clockwise, image.clockwise_pos)
        if req.dynamic_graphic:
            for i in range(-5, -1):
                try:
                    self.screen.blit(pygame.transform.rotate(pygame.image.load('images/' + req.playing_deck[i][0] + '_' + req.playing_deck[i][1] + '.png'), 30*(i+req.random)), \
                    image.playing_deck_pos)
                except:
                    pass
        try:
            self.screen.blit(pygame.transform.scale(pygame.transform.rotate(pygame.image.load('images/' + req.current_card[0] + '_' + req.current_card[1] + '.png'), 0), (77, (115/77*77))), \
            image.current_card_pos)
        except:
            self.screen.blit(pygame.image.load('images/' + req.current_card[0] + '.png'), image.current_card_pos)

        self.screen.blit(image.player_1, image.player_1_pos)
        self.screen.blit(image.player_2, image.player_2_pos)
        self.screen.blit(image.player_3, image.player_3_pos)
        self.screen.blit(image.player_4, image.player_4_pos)
        if req.color_change:
                self.screen.blit(image.red, image.red_pos)
                self.screen.blit(image.blue, image.blue_pos)
                self.screen.blit(image.green, image.green_pos)
                self.screen.blit(image.yellow, image.yellow_pos)
        for i in range(len(req.players[1])):
            self.screen.blit(image.card_back_right, (image.player_2_card_pos[0],  \
            image.player_2_card_pos[1] + i * image.player_2_card_pos[2]))              
        for i in range(len(req.players[2])):
            self.screen.blit(image.card_back_inverted, (image.player_3_card_pos[0] + i * image.player_3_card_pos[1], \
            image.player_3_card_pos[2]))               
        for i in range(len(req.players[3])):
            self.screen.blit(image.card_back_left, (image.player_4_card_pos[0], \
            image.player_4_card_pos[1] + i * image.player_4_card_pos[2]))                   
        for i in range(len(req.players[0])):
            self.screen.blit(pygame.image.load('images/' + req.players[0][i][0] + '_' + req.players[0][i][1] + '.png'), \
            (image.player_1_card_pos[0] + i * image.player_1_card_pos[1], image.player_1_card_pos[2]))  
            
    def load_text(self, req, names):
        text = names.font.render(names.player_1_name, True, names.text_color)
        self.screen.blit(text, names.player_1_text_pos)
        text = names.font.render(names.player_2_name, True, names.text_color)
        self.screen.blit(text, names.player_2_text_pos)
        text = names.font.render(names.player_3_name, True, names.text_color)
        self.screen.blit(text, names.player_3_text_pos)
        text = names.font.render(names.player_4_name, True, names.text_color)
        self.screen.blit(text, names.player_4_text_pos)
        text = names.font.render(req.message, True, names.text_color)
        self.screen.blit(text, names.playing_message_pos)                      

class Buttons:
    """
    Class to create the buttons for the game
    """
    def __init__(self):
        self.play_pos = Image().play_pos 
        self.info_pos = Image().info_pos
        self.arrow_pos = Image().arrow_pos               
        self.home_button1_pos = Image().home_button1_pos             
        self.home_button2_pos = Image().home_button2_pos
        self.home_button3_pos = Image().home_button3_pos             
        
    def play_button_is_clicked(self, mouse_pos, req, game_status):
        if self.play_pos[0] < mouse_pos[0] < self.play_pos[0] + self.play_pos[2] \
            and self.play_pos[1] < mouse_pos[1] < self.play_pos[1] + self.play_pos[3] \
            and req.game_status == game_status.loading:
            req.game_status = game_status.playing
            SoundEffects().shuffle_card()
            return True
        return False
    
    def home_button_is_clicked(self, mouse_pos, req, game_status):
        if (self.home_button1_pos[0] < mouse_pos[0] < self.home_button1_pos[0] + self.home_button1_pos[2] \
            and self.home_button1_pos[1] < mouse_pos[1] < self.home_button1_pos[1] + self.home_button1_pos[3] \
            and req.game_status == game_status.playing) \
                or \
            (self.home_button2_pos[0] < mouse_pos[0] < self.home_button2_pos[0] + self.home_button2_pos[2] \
            and self.home_button2_pos[1] < mouse_pos[1] < self.home_button2_pos[1] + self.home_button2_pos[3] \
            and req.game_status == game_status.winner) \
                or \
            (self.home_button3_pos[0] < mouse_pos[0] < self.home_button3_pos[0] + self.home_button3_pos[2] \
            and self.home_button3_pos[1] < mouse_pos[1] < self.home_button3_pos[1] + self.home_button3_pos[3] \
            and req.game_status == game_status.info):
            game_reset(req)
            req.game_status = game_status.loading
            SoundEffects().return_button()
            return True
        return False

    def info_button_is_clicked(self, mouse_pos, req, game_status):
        if self.info_pos[0] < mouse_pos[0] < self.info_pos[0] + self.info_pos[2] \
            and self.info_pos[1] < mouse_pos[1] < self.info_pos[1] + self.info_pos[3] \
            and req.game_status == game_status.loading:
            req.game_status = game_status.info
            SoundEffects().click_button()
            return True
        return False

    def play_type_arrow_is_clicked(self, mouse_pos, req, game_status):
        if ((self.arrow_pos[0] < mouse_pos[0] < self.arrow_pos[0] + self.arrow_pos[1]) \
            or (self.arrow_pos[2] < mouse_pos[0] < self.arrow_pos[2] + self.arrow_pos[3])) \
            and self.arrow_pos[4] < mouse_pos[1] < self.arrow_pos[4] + self.arrow_pos[5] \
            and req.game_status == game_status.loading:
            if req.classic:
                req.classic = False
            else:
                req.classic = True
            SoundEffects().click_button()
            return True

class PlayerPlay:
    """
    Class to create the player play
    """
    def __init__(self):                
        pass
    
    def shout_uno_is_clicked(self, mouse_pos, req, image):
        if not req.shout_uno[req.position] and req.played:
            if image.uno_button_pos[0] < mouse_pos[0] < image.uno_button_pos[0] + image.uno_button_pos[2] \
                and image.uno_button_pos[1] < mouse_pos[1] < image.uno_button_pos[1] + image.uno_button_pos[3]:
                req.shout_uno[req.position] = True
                SoundEffects().uno_sound()
                return True
            return False

    def checked_button_is_clicked(self, mouse_pos, req, image):
        if req.played or req.drawn:
            if image.checked_pos[0] < mouse_pos[0] < image.checked_pos[0] + image.checked_pos[2] \
                and image.checked_pos[1] < mouse_pos[1] < image.checked_pos[1] + image.checked_pos[3]:
                req.player_is_playing = False
                req.variant_played, req.variant_drawn = False, False
                SoundEffects().click_button()
                return True
            return False

    def card_choose(self, mouse_pos, req, image):
        for i in range(len(req.players[0])):
            if image.player_cards_pos[0] + i * image.player_cards_pos[4] < mouse_pos[0] \
            < (image.player_cards_pos[0]+image.player_cards_pos[2]) + i * image.player_cards_pos[4] \
            and image.player_cards_pos[1] < mouse_pos[1] < (image.player_cards_pos[1]+image.player_cards_pos[3]):
                if not req.classic:
                    if not req.variant_played and not req.variant_drawn:
                        discard_card(req, req.players[0][i], 0)
                    elif req.variant_played and req.variant_drawn:
                        play_card(req, req.players[0][i], 0)
                else:
                    play_card(req, req.players[0][i], 0)
                SoundEffects().play_card()          

    def main_deck_choose(self, mouse_pos, req, image):
        if image.card_back_pos[0] <= mouse_pos[0] <= (image.card_back_pos[0] + image.card_back_pos[2]) \
        and image.card_back_pos[1] <= mouse_pos[1] <= (image.card_back_pos[1] + image.card_back_pos[3]):
            if not req.classic:
                if req.variant_played and not req.variant_drawn:
                    variant_card_draw(req, 0)
                elif req.variant_played and req.variant_drawn:
                    take_card_from_main_deck(req, 0)
            else:
                take_card_from_main_deck(req, 0)
            SoundEffects().draw_card()         

    def color_choose(self, mouse_pos, req, image):
        if req.color_change:
            if image.red_pos[0] <= mouse_pos[0] <= (image.red_pos[0] + image.red_pos[2]) \
            and image.red_pos[1] <= mouse_pos[1] <= (image.red_pos[1] + image.red_pos[3]):
                play_color_card(req, 0, 'Red')
                SoundEffects().click_button()
            if image.blue_pos[0] <= mouse_pos[0] <= (image.blue_pos[0] + image.blue_pos[2]) \
                and image.blue_pos[1] <= mouse_pos[1] <= (image.blue_pos[1] + image.blue_pos[3]):
                play_color_card(req, 0, 'Blue')
                SoundEffects().click_button()
            if image.green_pos[0] <= mouse_pos[0] <= (image.green_pos[0] + image.green_pos[2]) \
                and image.green_pos[1] <= mouse_pos[1] <= (image.green_pos[1] + image.green_pos[3]):
                play_color_card(req, 0, 'Green')
                SoundEffects().click_button()
            if image.yellow_pos[0] <= mouse_pos[0] <= (image.yellow_pos[0] + image.yellow_pos[2]) \
                and image.yellow_pos[1] <= mouse_pos[1] <= (image.yellow_pos[1] + image.yellow_pos[3]):
                play_color_card(req, 0, 'Yellow')
                SoundEffects().click_button()

    def turn_check(self, req, image, screen):
        if not req.classic:
            if not req.variant_played and not req.variant_drawn:
                req.message = "Choose a card to discard"
            elif req.variant_played and not req.variant_drawn:
                req.message = "Take a card from the main deck"
            elif req.variant_played and req.variant_drawn:
                req.message = "Play normal game..."
        else:
            req.message = "It's your turn"                         
        if not req.drawn and not req.played:
            if (req.current_card[0] == '+2' or req.current_card[0] == '+4') and req.special_check==0:                          
                card_drawn_24(req, 0)
                req.special_check=1
                req.player_is_playing = False
                SoundEffects().draw_card()
        screen.blit(image.checked, image.checked_pos[0:2])
        screen.blit(image.line, image.line1_pos)
        screen.blit(image.uno_button, image.uno_button_pos[0:2])

class ComputerPlay:
    """
    Class to create the computer play
    """
    def __init__self():
        pass

    def computer_turn(self, req, sound):
        set_current_player(req, True)                       
        if req.position == 0:
            req.player_is_playing = True
            req.shout_uno[0] = False

        else:
            req.played = False
            req.drawn = False
            req.variant_played = False
            req.variant_drawn = False
            bot_move(req, sound)

        req.time_to_wait = 0

    def computer_turn_message(self, req):
        if not req.bot_play_message:                           
            if (req.position + req.direction_check) % 4 == 1:
                req.message = f'{Names().player_2_name} is playing'        
            elif (req.position + req.direction_check) % 4 == 2:
                req.message = f'{Names().player_3_name} is playing'       
            elif (req.position + req.direction_check) % 4 == 3:
                req.message = f'{Names().player_4_name} is playing'  

    def computer_play_image(self, req, image, screen):
        if (req.position + req.direction_check) % 4 == 1:
            screen.blit(image.line, image.line2_pos)      
        elif (req.position + req.direction_check) % 4 == 2:
            screen.blit(image.line, image.line3_pos)       
        elif (req.position + req.direction_check) % 4 == 3:
            screen.blit(image.line, image.line4_pos)      
            
class Winner:
    """
    Class to create the winner
    """
    def __init__(self):
        pass

    def check_for_winner(self, req, game_status):              
        for i in range(len(req.players)):
            if len(req.players[i]) == 0:
                req.winner = i
                if req.winner == 0:
                    req.winner_message = "You won this round!"
                    SoundEffects().winner_sound()  
                else:
                    req.winner_message = f'{req.bot_name_dict[req.winner]} won this round!'
                    SoundEffects().loser_sound()
                score_calculation(req)
                req.game_status = game_status.winner
                return True
        return False

class SoundEffects:
    """
    Class to create the sound effects
    """
    def __init__(self):
        self.volume = 0.2
    def click_button(self):
        pygame.mixer.Sound(os.path.join('sound', 'click_button.wav')).play()
    def shuffle_card(self):
        pygame.mixer.Sound(os.path.join('sound', 'shuffle_card.mp3')).play()
    def winner_sound(self):
        pygame.mixer.Sound(os.path.join('sound', 'winner_sound.mp3')).play()
    def loser_sound (self):
        pygame.mixer.Sound(os.path.join('sound', 'loser_sound.wav')).play()
    def return_button(self):
        pygame.mixer.Sound(os.path.join('sound', 'return_button.wav')).play()
    def open_game(self):
        pygame.mixer.Sound(os.path.join('sound', 'open_game.wav')).play()
    def play_card(self):
        pygame.mixer.Sound(os.path.join('sound', 'play_card.wav')).play()
    def uno_sound(self):
        pygame.mixer.Sound(os.path.join('sound', 'uno_sound.ogg')).play()
    def draw_card(self):
        pygame.mixer.Sound(os.path.join('sound', 'draw_card.wav')).play()