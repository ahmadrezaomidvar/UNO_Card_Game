import pygame
from rules import *
from game import *
from settings import *


def main():
    """
    main function to run the game

    :return: None
    """
    # Create required objects
    game = Game()
    screen = game.screen
    image = Image()
    names = Names()
    buttons = Buttons()
    requirements = Requirements()                       
    game_status = GameStatus()                         
    player_play = PlayerPlay()
    computer_play = ComputerPlay()
    winner = Winner()
    sound = SoundEffects()                          

    playing = True                                      
    requirements.game_status = game_status.loading
    penalty_check = False                              

    card_deal(requirements)                             

    # Game play loop
    while playing:
        for event in pygame.event.get():
            
            game.quit(event)
            if game.check_mouse_click(event):
                mouse_pos = game.get_mouse_pos(event)
                buttons.play_button_is_clicked(mouse_pos, requirements, game_status)      
                buttons.home_button_is_clicked(mouse_pos, requirements, game_status)
                buttons.info_button_is_clicked(mouse_pos, requirements, game_status)  
                buttons.play_type_arrow_is_clicked(mouse_pos, requirements, game_status)    

                if requirements.player_is_playing:
                    player_play.shout_uno_is_clicked(mouse_pos, requirements, image)
                    player_play.checked_button_is_clicked(mouse_pos, requirements, image)
                    player_play.card_choose(mouse_pos, requirements, image)
                    player_play.main_deck_choose(mouse_pos, requirements, image)
                    player_play.color_choose(mouse_pos, requirements, image)

        # Home page
        if requirements.game_status == game_status.loading:
            game.load_home_screen(requirements, image, names)

        # Playing page
        elif requirements.game_status == game_status.playing:
            winner.check_for_winner(requirements, game_status)
            game.load_base_images(requirements ,image)
            game.load_text(requirements, names)

            # Play Round
            if requirements.player_is_playing:
                player_play.turn_check(requirements, image, screen)                           
                     
            else:
                if requirements.time_to_wait == requirements.game_speed:                               
                    penalty_check = False
                    computer_play.computer_turn(requirements, sound)

                else:
                    if not penalty_check:                    
                        uno_penalty(requirements, requirements.position)
                        penalty_check = True

                    requirements.time_to_wait += 1

                    computer_play.computer_turn_message(requirements)               
                    computer_play.computer_play_image(requirements, image, screen)  
        
        # Winner page
        elif requirements.game_status == game_status.winner and requirements.winner != -1:
            game.load_winner_screen(requirements, image, names)

        elif requirements.game_status == game_status.info:
            game.load_info_screen(image)
            
        game.update_screen()



if __name__ == '__main__':
    main()