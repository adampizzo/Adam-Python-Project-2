import logging
import datetime

logging.basicConfig(filename='logs\\checks.log', level=logging.DEBUG)

def is_player_height_int(players_list, logging_enabled):
    '''This function tests whether the clean_player_height function's output actually changes it to int or not.'''        
    is_int = []
    for player in players_list:        
        if type(player['height']) == int:                
            is_int.append(True)
        else:
            is_int.append(False)
    if logging_enabled == True: 
        if all(is_int) == True:
            logging.info(f"Player data [height] has been converted to int successfully at {datetime.datetime.now()}.")
            return True            
        else:
            logging.warning(f"Player data [height] has not been converted to int successfully at {datetime.datetime.now()}.")
            return False
    else:
        if all(is_int) == True:
            return True            
        else:
            return False

def is_player_experience_bool(players_list, logging_enabled):
    '''This function tests whether the clean_player_experience function's output actually changes it to bool or not'''
    is_bool = []
    for player in players_list:            
        if type(player['experience']) == bool:
            is_bool.append(True)
        else:
            is_bool.append(False)
    if logging_enabled == True: 
        if all(is_bool) == True:
            logging.info(f"Player data [experience] has been converted to bool successfully at {datetime.datetime.now()}.")
            return True            
        else:
            logging.warning(f"Player data [experience] has not been converted to bool successfully at {datetime.datetime.now()}.")
            return False
    else:
        if all(is_bool) == True:
            return True            
        else:
            return False

def is_guardians_a_list(players_list, logging_enabled):
    '''This function tests whether the clean_player_guardians function's output actually changes the value to a list or not'''
    is_list = []
    for player in players_list:
        if type(player['guardians']) == list:
            is_list.append(True)
        else:
            is_list.append(False)
    if logging_enabled == True:
        if all(is_list) == True:
            logging.info(f"Player data [guardians] has been converted to list success at {datetime.datetime.now()}.")
            return True
        else:
            logging.warning(f"Player data [guardians] has not been converted to list success at {datetime.datetime.now()}.")
    else:
        if all(is_list) == True:
            return True
        else:
            return False
