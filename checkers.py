import logging
import datetime

#Exception Classes
class TeamNameNotInTeamsList(Exception):
    pass


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


def write_player_list(players_list):
    ''' The purpose of the write_player_list function is to write a listed provided as an argument to a log text file.
        I wanted to test out writing a file instead of just logging, which this could have done instead.
    '''
    file1 = open("logs\\playerlist.txt", "a")
    file1.write("\n\n" + str(datetime.datetime.now()))
    for players in players_list:
        file1.write("\n" + players['name'] + " - " + players['team'])  


def print_player_list(players_list):
    ''' The purpose of the print_player_list is to have a command to print out all players and their teams in the console. Originally used for
        testing code. The write player list became more useful, but I'll keep this in case it becomes handy for something in the future.
    '''
    player_format = '{:^25} {:^25}'
    print(player_format.format("Player Name", "Team"))
    print("-"*50)
    for player in players_list:        
        if "team" not in player.keys():
            print(player_format.format(player['name'], "Unassigned"))
        else: print(player_format.format(player['name'], player['team']))

def print_team_roster(team_name, teams_list, players_list):
    ''' Takes an argument for a team name to print its roster. 
        
        Verifies that the team being searched is in the teams_list otherwise prints an error.

        Utilizes the players_list list to search for who is on what team by each player['team'] key value
        and prints the players that match.         
    '''
    try:
        if team_name in teams_list:
            team_format = '{:^25}'
            print(team_format.format(team_name))
            print("-"*25)
            for player in players_list:
                if team_name in player['team']:
                    print(team_format.format(player['name']))
        else:
            raise TeamNameNotInTeamsList("That is not a valid team.")
    except TeamNameNotInTeamsList as err:
        print(err)

def print_team_list(teams_list):
    teams_format = '{:^25}'
    print(teams_format.format("Active Teams"))
    print("-"*25)
    for team in teams_list:
        print(teams_format.format(team))        