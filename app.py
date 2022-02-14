import copy
import random
import pdb
import time
import checkers
import config
import constants


class TeamNameNotInTeamsList(Exception):
    pass

'''if num_teams % num_players != 0:
        try:
            cut_players = input("\nThere are not enough players to have an even amount on all teams. Do you want to cut any players? (1 for Yes, 2 for No)\n")
            cut_players = int(cut_players)                
            if cut_players == 1:
                how_to_cut_players = input("Do you want to cut inexperienced players or random players")
    balance_by_experience = False
    
    experienced_players, non_experienced_players = get_experienced_players(players)

    
    for experienced_player in experienced_players:
    
    '''       
def sleep():
    time.sleep(.5)


def clean_data(players_list):
    '''The purpose of the clean_data function is to clean up the provided players list
    
    The data it cleans is converting the height field to an integer, the experience field to a bool, and the guardians field into a list.

    Each part of the function also runs a test function that checks to see whether the data has actually been converted into the correct
    and output it into a checks.log file into a log folder in the documents check.log.

    Returns the final changed player list.
    '''

    for player in players_list:            
        height = player['height'].split()[0]
        height = int(height)
        player['height'] = height
    checkers.is_player_height_int(players_list, config.logging_enabled)
    
    for player in players_list:
        if player['experience'] == 'YES':
            player['experience'] = True                
        elif player['experience'] == 'NO':            
            player['experience'] = False
    checkers.is_player_experience_bool(players_list, config.logging_enabled)
    
    for player in players_list:
        if "and" in player['guardians']:
            player['guardians'] = player['guardians'].split(" and ")                
        else:                
            player['guardians'] = [player['guardians']]
    checkers.is_guardians_a_list(players_list, config.logging_enabled)
    
    return players_list
        

def get_experienced_players(players_list):
    experienced_players = []
    non_experienced_players = []
    for players in players_list:
            if players['experience'] == True:
                experienced_players.append(players)
            else:
                non_experienced_players.append(players)
    return experienced_players, non_experienced_players


def add_players_to_team(teams_list, players_list):
    '''Performs the function to add players to a team'''
    num_teams = len(teams_list)
    counter = 0

    for players in players_list:
            if counter >= num_teams:
                counter = 0
            players['team'] = teams_list[counter]
            counter += 1
    return players_list


def print_player_list(players_list):
    player_format = '{:^25} {:^25}'
    print(player_format.format("Player Name", "Team"))
    print("-"*50)
    for player in players_list:        
        if "team" not in player.keys():
            print(player_format.format(player['name'], "Unassigned"))
        else: print(player_format.format(player['name'], player['team']))


def print_team_list(teams_list):
    teams_format = '{:^25}'
    print(teams_format.format("Active Teams"))
    print("-"*25)
    for team in teams_list:
        print(teams_format.format(team))
        

def get_num_players_on_a_team(team, players_list):
    num_players = 0    
    #pdb.set_trace()
    for player in players_list:
        if player['team'] == team:
            num_players += 1                    
    return num_players

def print_team_roster(team_name, teams_list, players_list):
    ''' Takes input for a team name to print its roster. 
        
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
    

def balance_teams(teams_list, players_list, balanced, randomize):
    '''This function will add players to each team either randomly and/or assigning them in a balanced manner based off their experience value'''    

    if balanced == False:
        if randomize == False: #Not Balanced and Not Random
            return add_players_to_team(teams_list, players_list)
        else: #Not Balanced and Random
            shuffled_players_list = random.sample(players_list, len(players_list))
            return add_players_to_team(teams_list, shuffled_players_list)                                    
    else:
        if randomize == False: #Balanced and not Random
            experienced_players, non_experienced_players = get_experienced_players(players_list)
            experienced_players = add_players_to_team(teams_list, experienced_players)
            non_experienced_players = add_players_to_team(teams_list, non_experienced_players)
            final_list = experienced_players + non_experienced_players
            return final_list
        else: #Balanced and Random            
            experienced_players, non_experienced_players = get_experienced_players(players_list)
            shuffled_experienced_players = random.sample(experienced_players, len(experienced_players))
            shuffled_non_experienced_players = random.sample(non_experienced_players, len(non_experienced_players))
            shuffled_experienced_players = add_players_to_team(teams_list, shuffled_experienced_players)
            shuffled_non_experienced_players = add_players_to_team(teams_list, shuffled_non_experienced_players)
            final_list = shuffled_experienced_players + shuffled_non_experienced_players            
            return final_list

def get_team(team_selection, teams_list):
    return teams_list[int(team_selection) - 1]



def display_team_stats(team_selection, teams_list, players_list):
    #team = teams_list[int(team_selection) - 1]
    team = get_team(team_selection, teams_list)

    print(f"Team: {team} Stats")
    print("-"*25)
    
    #Total Players
    print(f"Total players: {get_num_players_on_a_team(team, players_list)}")
    #Experienced and Inexperienced Player Totals
    experienced_players, non_experienced_players = get_experienced_players(players_list)
    print(f"Total experienced: {len(experienced_players)}")
    print(f"Total inexperienced: {len(non_experienced_players)}")
    #Average height

    #Players on team
    print(", ".join(get_players_on_team(team_selection, teams_list, players_list)))

    #players_on_team = ", ".join(get_players_on_team(team_selection, teams_list, players_list))
    #print(f"Players on Team: {players_on_team}")
    #Guardians of players on team.

    
def get_players_on_team(team_selection, teams_list, players_list):
    team = get_team(team_selection, teams_list)
    players = []   

    for player in players_list:
        if player['team'] == team:
            #players += (f"{player['name']}, ")
            players.append(player['name'])
            
    return players


def start_program():    
    teams = copy.deepcopy(constants.TEAMS) #the assignment statement only links the variable. We don't want to link, we want a new copy.
    players = copy.deepcopy(constants.PLAYERS)   

    players = clean_data(players)
    players = balance_teams(teams, players, True, True)
    
    continue_running = True

    while continue_running == True:
        print("Welcome to the Basketball Team Stats Tool!\n")
        sleep()
        menu_options = ["Display Team Stats", "Quit"]
        print("-"*5 + "Menu" + "-"*5 + "\n")
        sleep()
        print("Menu Options:".center(15))
        for counter, option in enumerate(menu_options, 1):
            print("{}) {}".format(counter, option))    
        sleep()
        user_selection = input("\nEnter an option:  ")
        try:
            if user_selection == "1": #display teams options
                for counter, team in enumerate(teams, 1):
                    print("{}) {}".format(counter, team))
                sleep()
                team_option_selection = input("\nEnter an option:  ")
                display_team_stats(team_option_selection, teams, players)
            elif user_selection == "2": #Quit
                sleep()
                print("\nThank you for using the Basketball Team Stats Tool!")
                sleep()
                print("Have a great day!")
                sleep()
                continue_running = False
            else:
                raise ValueError(f"\n{user_selection} is not a valid selection. Please try again\n")
        except ValueError as err:
            sleep()
            print(err)
            sleep()                
        finally:
            pass




    





if __name__ == '__main__': #Dunder main
    start_program()
    
    
    
    
    
    

    

    
    
    
    

  

    


    