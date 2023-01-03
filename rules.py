import random
import itertools
import pygame

def card_deal(req):
    """Deal cards to players"""
    var = []                                                                 
    for i in range(10):
        var.append(str(i))
        if i != 0:
            var.append(str(i))
    var.extend(['Skip', 'Skip', 'Reverse', 'Reverse', '+2', '+2'])           
    req.main_deck = list(itertools.product(var, req.color))                  
    for _ in range(4):                                                       
        req.main_deck.append(('Wild', 'Black'))
        req.main_deck.append(('+4', 'Black'))
    random.shuffle(req.main_deck)                                            

    while req.main_deck[-1] == ('+4', 'Black'):
        random.shuffle(req.main_deck)

    req.playing_deck.append(req.main_deck.pop())                              
    req.current_card = req.playing_deck[-1]                                   
    if req.current_card == ('Wild', 'Black'):                                      
        req.color_change = True                                              
    for i in range(4):                                              # TODO extended to input number of players in future versions
        for _ in range(7):
            req.players[i].append(req.main_deck.pop())

def play_card(req, card, player):
    """Play card"""
    if not req.played:

        if (card[0] == req.current_card[0] or card[1] == req.current_card[1]) and (card[0] not in ('+4', 'Wild')):        
            req.played, req.drawn = True, True                                     
            req.current_card = card                                                 
            req.playing_deck.append(card)                                          
            req.players[player].remove(card)                                        
            req.special_check = 0                                                   
            set_current_player(req, False)                                         

        if card == ('Wild', 'Black'):                                                     
            req.played, req.drawn = True, True                                     
            req.current_card = card                                                 
            req.color_change = True                                                 
            req.playing_deck.append(card)                                          
            req.players[player].remove(card)

        if card  == ('+4', 'Black'):
            for i in range(len(req.players[req.position])):
                if req.players[req.position][i][1] == req.current_card[1]:
                    break
            else:
                req.played, req.drawn = True, True                                      
                req.current_card = card                                                 
                req.color_change = True                                                
                req.playing_deck.append(card)                                           
                req.players[player].remove(card)
    
def set_current_player(req, defult):  
    """Set current player based on direction of play""" 
    req.random = random.randint(6, 100)
    if defult == True:
        req.position = (req.position + req.direction_check) % 4 
    if req.current_card[0] == 'Reverse' and req.special_check == 0:
        req.direction_check *= -1
        req.special_check = 1
    if req.current_card[0] == 'Skip' and req.special_check == 0:
        req.position = (req.position + req.direction_check) % 4
        req.special_check = 1
    

def take_card_from_main_deck(req, player):
    """Take card from main deck"""
    if not req.drawn:
        try:
            req.players[player].append(req.main_deck.pop())                       
            req.drawn = True                                                     
            set_current_player(req, False)                                        
        except IndexError:                                                       
            req.main_deck = req.playing_deck[:-1]                                 
            random.shuffle(req.main_deck)                                         
            req.playing_deck = [req.playing_deck[-1]]                             
            req.players[player].append(req.main_deck.pop())                       
            req.drawn = True                                                     
            set_current_player(req, False)                                        


def bot_move(req, sound):
    """Bot move"""
    req.shout_uno[req.position] = False
    if not req.classic:
        bot_discard_card(req, req.position, sound)
        bot_variant_card_draw(req, req.position, sound)
    if (req.current_card[0] == '+2' or req.current_card[0] == '+4') and req.special_check == 0:
        bot_play_24(req, req.position, sound)
        req.played_check = True
    else:
        flag = False
        for i in range(len(req.players[req.position])):
            if req.players[req.position][i][0] == req.current_card[0] or req.players[req.position][i][1] == req.current_card[1]:
                if req.players[req.position][i][0] not in ('+4', 'Wild'):
                    bot_play_card(req, req.players[req.position][i], req.position, sound)
                    set_current_player(req, False)
                    flag = True
                    break
                else:
                    pass
        if not flag:
            black_flag = False
            for i in range(len(req.players[req.position])):
                if req.players[req.position][i][1] == 'Black':
                    bot_play_black_card(req, req.players[req.position][i], req.position, sound)
                    black_flag = True
                    break
            if not black_flag:
                bot_take_card_from_main_deck(req, req.position, sound)
        bot_shout_uno(req, req.position, sound)

def bot_play_card(req, card, player, sound):
    """Bot play card"""
    req.special_check = 0                 
    req.playing_deck.append(card)
    req.current_card = card
    req.players[player].remove(card)
    random.shuffle(req.players[player])
    if req.bot_play_message:                        
        req.message = f'{req.bot_name_dict[player]} played {card[0]} {card[1]}'
    sound.play_card()

def bot_take_card_from_main_deck(req, player, sound):
    """Bot take card from main deck"""
    try:
        req.players[player].append(req.main_deck.pop())
        if req.bot_play_message:
            req.message = f'{req.bot_name_dict[player]} took a card from main deck'
    except IndexError:
        req.main_deck = req.playing_deck[:-1]
        random.shuffle(req.main_deck)
        req.playing_deck = [req.playing_deck[-1]]
        req.players[player].append(req.main_deck.pop())
        if req.bot_play_message:
            req.message = f'{req.bot_name_dict[player]} took a card from main deck'
    finally:
        sound.draw_card()

    if req.players[player][-1][1] == 'Black':
        bot_play_black_card(req, req.players[player][-1], player, sound)
    elif req.players[player][-1][0] == req.current_card[0] or req.players[player][-1][1] == req.current_card[1]:
        bot_play_card(req, req.players[player][-1], player, sound)
    else:
        set_current_player(req, False)

def play_color_card(req, player, color):
    """Play color card"""
    req.color_change = False
    req.current_card = (req.current_card[0], color)
    req.special_check = 0
    req.message = f'{color} card played'

def bot_play_black_card(req, card, player, sound):
    """Bot play black card"""
    req.special_check = 0
    req.playing_deck.append(card)
    req.current_card = card
    req.players[player].remove(card)                                               
    color_dict = {'Blue': 0, 'Green': 0, 'Red': 0, 'Yellow': 0, 'Black': 0}
    for i in range(len(req.players[player])):
        color_dict[req.players[player][i][1]] += 1
    sorted_color = sorted(color_dict.items(), key=lambda x: x[1], reverse=True)
    max_color = sorted_color[0][0]
    if max_color == 'Black':
        max_color = sorted_color[1][0]
    req.current_card = (req.current_card[0], max_color)
    if req.bot_play_message:
        req.message = f'{req.bot_name_dict[player]} played {card[0]} {card[1]}, color changed to {max_color}'
    random.shuffle(req.players[player])
    sound.play_card()

def bot_play_24(req, player, sound):
    """Play +2/+4"""
    req.special_check = 1
    if req.bot_play_message:
        req.message = f'{req.current_card[0]} played'
    if req.current_card[0] == '+2':
        for i in range(2):
            try:
                req.players[req.position].append(req.main_deck.pop())
            except IndexError:
                req.main_deck = req.playing_deck[:-1]
                random.shuffle(req.main_deck)
                req.playing_deck = [req.playing_deck[-1]]
                req.players[req.position].append(req.main_deck.pop())
    else:
        for i in range(4):
            try:
                req.players[req.position].append(req.main_deck.pop())
            except IndexError:
                req.main_deck = req.playing_deck[:-1]
                random.shuffle(req.main_deck)
                req.playing_deck = [req.playing_deck[-1]]
                req.players[req.position].append(req.main_deck.pop())
    if req.bot_play_message:
        req.message = f'{req.bot_name_dict[player]} draw {req.current_card[0]} cards'
    sound.draw_card()

def card_drawn_24(req, player):
    """Card drawn after +2/+4"""
    if req.current_card[0] == '+2':
        for i in range(2):
            try:
                req.players[player].append(req.main_deck.pop())
            except IndexError:
                req.main_deck = req.playing_deck[:-1]
                random.shuffle(req.main_deck)
                req.playing_deck = [req.playing_deck[-1]]
                req.players[player].append(req.main_deck.pop())
    else:
        for i in range(4):
            try:
                req.players[player].append(req.main_deck.pop())
            except IndexError:
                req.main_deck = req.playing_deck[:-1]
                random.shuffle(req.main_deck)
                req.playing_deck = [req.playing_deck[-1]]
                req.players[player].append(req.main_deck.pop())
    req.message = f'Player {player} draw {req.current_card[0]} cards'

def game_reset(req):
    """Reset game"""
    req.players = [[], [], [], []]                        
    req.game_status = ''
    req.main_deck = []                                     
    req.playing_deck = []                                  
    req.current_card = []                                  
    req.played = False                                     
    req.drawn = False                                      
    req.position = 1                                       
    req.direction_check = -1                               
    req.winner = -1                                        
    req.message = 'Dealing cards...'                       
    req.winner_message = ''                                
    req.player_is_playing = False                          
    req.drawn = False                                      
    req.time_to_wait = -1                                  
    req.special_check = 0                                  
    req.color_change = False                               
    req.played_check = False
    req.variant_play = False                               
    req.variant_draw = False  
    req.score_message = '' 
    req.shout_uno = [True]*4                          
    card_deal(req)                              

def discard_card(req, card, player):
    """Play card"""
    req.playing_deck.insert(0, card)                                          
    req.players[player].remove(card)
    req.variant_played = True
    
def variant_card_draw(req, player):
    """Take card from main deck"""
    try:
        req.players[player].append(req.main_deck.pop())                       
        req.variant_drawn = True                                                     
    except IndexError:                                                       
        req.main_deck = req.playing_deck[:-1]                                 
        random.shuffle(req.main_deck)                                         
        req.playing_deck = [req.playing_deck[-1]]                             
        req.players[player].append(req.main_deck.pop())                       
        req.variant_drawn = True
    
def bot_discard_card(req, player, sound):
    """Play card"""
    card = random.sample(req.players[player], 1)[0]
    req.playing_deck.insert(0, card)                                          
    req.players[player].remove(card)
    sound.play_card()

def bot_variant_card_draw(req, player, sound):
    """Take card from main deck"""
    try:
        req.players[player].append(req.main_deck.pop())                                                                           
    except IndexError:                                                       
        req.main_deck = req.playing_deck[:-1]                                 
        random.shuffle(req.main_deck)                                         
        req.playing_deck = [req.playing_deck[-1]]                             
        req.players[player].append(req.main_deck.pop())
    finally:
        sound.draw_card()

def score_calculation(req):
    """Calculate score"""
    
    for i in range(len(req.players)):
        for j in range(len(req.players[i])):
            if req.players[i][j][0] == 'Skip' or req.players[i][j][0] == 'Reverse' or req.players[i][j][0] == '+2':
                req.score_dict[i] += 20
            elif req.players[i][j][1] == 'Black':
                req.score_dict[i] += 50
            else:
                req.score_dict[i] += int(req.players[i][j][0])
    for i in range(len(req.players)):
        req.score_message += str(f'Player {i} score: {req.score_dict[i]}\n')
    for i in range(len(req.players)):
        if req.score_dict[i] >= 500:
            winner = min(req.score_dict, key=req.score_dict.get)
            req.score_message += str(f'Final Winner: Player {winner} with score: {req.score_dict[winner]}\n')
            for k in range(len(req.players)):
                req.score_dict[k] = 0
            break

def bot_shout_uno(req, player, sound):
    """Bot shout uno"""
    if len(req.players[player]) == 1:
            if random.uniform(0, 1) > req.uno_shout_chance:
                req.shout_uno[player] = True
                req.message = f'{req.bot_name_dict[player]} shouted UNO!!!'
                sound.uno_sound()

def uno_penalty(req, player):
    if len(req.players[req.position]) == 1 and not req.shout_uno[req.position]:
        req.message = f'Player {req.position} forgot to shout UNO!!!'
        for i in range(4):
            try:
                req.players[player].append(req.main_deck.pop())                       
            except IndexError:                                                       
                req.main_deck = req.playing_deck[:-1]                                 
                random.shuffle(req.main_deck)                                         
                req.playing_deck = [req.playing_deck[-1]]                             
                req.players[player].append(req.main_deck.pop())        
                            
                        