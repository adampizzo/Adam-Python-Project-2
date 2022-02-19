# Importing Calls
import copy
import random
import os
import sys
import time
import checkers
import config
import constants


# General Utility Functions
def sleep():
    ''' The purpose of the sleep function is to cut down on me writing
        time.sleep(x) multiple times. If I ever need to change the pauses
        it will just be changing this function.'''
    time.sleep(.5)


def get_menu_items(options_list):
    ''' The purpose of the set_menu_items function is to set the menu
        items for the program. If they ever need to be changed, this
        function can be called to do that.'''
    return options_list


def add_dots():
    ''' The purpose of the add_dots function is to print 10 periods
        in a row. This function is cosmetic and is to cut down on
        typing this code over and over again.'''
    for _ in range(10):
        print(".", end="")
        time.sleep(.08)


def clear():
    ''' The purpose of the clear function is to determine what the
        operating system and then clear the screen.'''
    if sys.platform == "win32":
        os.system('cls')
    else:
        os.system('clear')


# Data Utility Functions
def clean_data(players_list):
    '''The purpose of the clean_data function is to clean up the provided players
    list.

    The data it cleans is converting the height field to an integer, the
    experience field to a bool, and the guardians field into a list.

    Each part of the function also runs a test function that checks to see
    whether the data has actually been converted into the correct and output
    it into a checks.log file into a log folder in the documents check.log.

    Returns the final changed player list.'''
    add_dots()
    print("Correcting player height" + "."*10)
    sleep()
    for player in players_list:
        height = player['height'].split()[0]
        height = int(height)
        player['height'] = height
    if checkers.is_player_height_int(players_list, config.logging_enabled):
        add_dots()
        print("Success. Player height has been corrected" + "."*10 + "\n")
        bool_height_cleaned = True
    sleep()

    add_dots()
    print("Correcting player experince" + "."*10)
    sleep()
    for player in players_list:
        if player['experience'] == 'YES':
            player['experience'] = True
        elif player['experience'] == 'NO':
            player['experience'] = False
    if checkers.is_player_experience_bool(players_list, config.logging_enabled):
        add_dots()
        print("Success. Player experience has been corrected" + "."*10 + "\n")
        bool_experience_cleaned = True
    sleep()

    add_dots()
    print("Correcting player guardian entries" + "."*10)
    for player in players_list:
        if "and" in player['guardians']:
            player['guardians'] = player['guardians'].split(" and ")
        else:
            player['guardians'] = [player['guardians']]
    if checkers.is_guardians_a_list(players_list, config.logging_enabled):
        add_dots()
        print("Success. Player guardians have been corrected" + "." * 10 + "\n")
        bool_guardians_cleaned = True
    sleep()
    if bool_height_cleaned and bool_experience_cleaned and bool_guardians_cleaned:
        add_dots()
        print("All data has been successfully cleaned. Intializing balance selections." + "." * 10)
        time.sleep(2)
    else:
        sys.exit()
    clear()
    return players_list


def balance_teams(teams_list, players_list, balanced, randomize):
    ''' This function will add players to each team either randomly and/or assigning
        them in a balanced manner based off their experience value.

        By default, the options in config.py set this to balanced = True and
        randomize = False, however, the user can be asked to specify their
        selections as well by modifying the ask_balanced_randomized variable in config.py.
    '''
    if not balanced:
        if not randomize:  # Not Balanced and Not Random
            return add_players_to_team(teams_list, players_list)
        else:  # Not Balanced and Random
            shuffled_players_list = random.sample(players_list, len(players_list))
            return add_players_to_team(teams_list, shuffled_players_list)
    else:
        if not randomize:  # Balanced and not Random
            experienced_players, non_experienced_players = get_players_by_experience(players_list)
            experienced_players = add_players_to_team(teams_list, experienced_players)
            non_experienced_players = add_players_to_team(teams_list, non_experienced_players)
            final_list = experienced_players + non_experienced_players
            return final_list
        else:  # Balanced and Random
            experienced_players, non_experienced_players = get_players_by_experience(players_list)
            shuffled_experienced_players = random.sample(experienced_players, len(experienced_players))
            shuffled_non_experienced_players = random.sample(non_experienced_players, len(non_experienced_players))
            shuffled_experienced_players = add_players_to_team(teams_list, shuffled_experienced_players)
            shuffled_non_experienced_players = add_players_to_team(teams_list, shuffled_non_experienced_players)
            final_list = shuffled_experienced_players + shuffled_non_experienced_players
            return final_list


# Player Utility Functions
def get_players_by_experience(players_list):
    ''' The purpose of the get_players_by_experience function is to take a
        list of players and return two separate lists based on their
        experience. One list will only be for players who have True
        for their experience dictionary key value. The other list will
        be for players who have False for their experience dictionary
        key value.'''

    experienced_players = []
    non_experienced_players = []
    for players in players_list:
            if players['experience']:
                experienced_players.append(players)
            else:
                non_experienced_players.append(players)
    return experienced_players, non_experienced_players


def get_num_players_by_experience(team_name, players_list):
    ''' The purpose of get_num_players_by_experience function takes
        the team that they are on and the player list as well as if they are.
        experienced or not. It then returns the length of a list of all players
        on that list.'''

    total_experienced_players = []
    total_non_experienced_players = []

    experienced_players, non_experienced_players = get_players_by_experience(players_list)
    for exp_player in experienced_players:
        if exp_player['team'] == team_name:
            total_experienced_players.append(exp_player)

    for non_exp_player in non_experienced_players:
        if non_exp_player['team'] == team_name:
            total_non_experienced_players.append(non_exp_player)

    return(len(total_experienced_players), len(total_non_experienced_players))


def add_players_to_team(teams_list, players_list):
    ''' The purpose of the add_players_to_team function is to add players to a
        team by cycling through all of the available teams and adding a player
        to the team with the index of the current team list and incrementing
        the counter. When the counter reaches the amount of teams there are
        in teams_list, then it will set the counter to 0.

        This also writes the players it adds to each team to a file under
        the log folder, if logging is enabled.'''

    num_teams = len(teams_list)
    counter = 0
    for players in players_list:
        if counter >= num_teams:
            counter = 0
        players['team'] = teams_list[counter]
        counter += 1
    if config.logging_enabled:
        checkers.write_player_list(players_list)
    return players_list


# Team Utility Functions
def get_num_players_on_a_team(team, players_list):
    ''' The purpose of the get_num_players_on_a_team function is to take the
        team and player list, and count how many players there are that are
        on that team. They are counted by append each player that is on that
        team into a list and then returning len() on the list.'''

    num_players_on_team = []
    for player in players_list:
        if player['team'] == team:
            num_players_on_team.append(player)
    return len(num_players_on_team)


def average_team_height(team, players_list):
    ''' The purpose of the average_team_height function is to take the
        team and player list, and then add up all players height on the
        team. Then we divide that by the number of players on the team.
        We return the rounded height.'''

    players_on_team = get_num_players_on_a_team(team, players_list)
    combined_height = 0
    for player in players_list:
        if player['team'] == team:
            combined_height += player['height']
    return round(combined_height / players_on_team)


def get_players_guardians_on_team(team, players_list):
    ''' The purpose of the get_players_guardians_on_team function is
        to take the team and player list, and then print out all guardians
        for players whose team matches the entered team.'''

    guardians_list = []
    for player in players_list:
        if player['team'] == team:
            guardians_list += player['guardians']
    return ", ".join(guardians_list) + "\n"


def get_player_names_on_team(team, players_list):
    ''' The purpose of the get_player_names_on_team is to take the team and
        player list, and then print out all of the player names of
        the players on the team whose team matches the entered team.'''

    players = []

    for player in players_list:
        if player['team'] == team:
            players.append(player['name'])
    return ", ".join(players)


def get_team_index(team_selection, teams_list):
    ''' The purpose of get_team_index function is to take a team selection
        from the menu selection screen and return the actual index of the team.'''

    return teams_list[int(team_selection) - 1]


def display_team_stats(team_selection, teams_list, players_list):
    ''' The purpose of display_team_stats is to display the Team name, the total
        amount of players on the team, the total amount of expeirenced and
        inexperienced players on the team, the average height of the team, and
        the guardians of the players on the team.'''

    team = get_team_index(team_selection, teams_list)
    print(f"Team: {team} Stats")
    print("-"*25)
    sleep()
    # Total Players
    print(f"Total players: {get_num_players_on_a_team(team, players_list)}")
    sleep()
    # Experienced and Inexperienced Player Totals
    num_exp_player, num_non_exp_player = get_num_players_by_experience(team, players_list)
    print(f"Total experienced: {num_exp_player}")
    sleep()
    print(f"Total inexperienced: {num_non_exp_player}")
    sleep()
    # Average height
    print(f"The average height of the players on the {team} is: {average_team_height(team, players_list)} inches.")
    sleep()
    # Players on team
    print(f"Players on the {team}: ")
    print(get_player_names_on_team(team, players_list))
    sleep()
    # Guardians of players on team.
    print(f"Guardians of Players on the {team}: ")
    print(get_players_guardians_on_team(team, players_list))
    print()
    sleep()
    checkers.write_team_stats(team, players_list)


def initiate_data():
    ''' The purpose of initiate_data is set the initial variables as well as
        determine how the users want to balance their teams.'''

    config.teams = copy.deepcopy(constants.TEAMS)  # The assignment statement only links the variable. We don't want to link, we want a new copy.
    config.players = copy.deepcopy(constants.PLAYERS)

    clear()
    print(" "*10 + "Welcome User\n")
    sleep()
    add_dots()
    print("Intializing Data Cleaning" + "."*10 + "\n")
    config.players = clean_data(config.players)

    if config.ask_balanced_randomized:
        # Only run this code if the variable in config is True.
        # Otherwise, it will run the basic balanced but not
        # randomized code (Or whatever we've set those variables to in config.)
        add_dots()
        print("Preparing to Balance Teams" + "."*10 + "\n")
        sleep()
        while True:
            try:
                print("When balancing the teams, would you like to balance them by experience?")
                print("1) Yes")
                print("2) No")
                balance_teams_input = input("\n Enter an option:  ")
                balance_teams_input = int(balance_teams_input)
            except ValueError:
                print(f"\n{balance_teams_input} is not a valid selection. Please try again\n")
            else:
                if balance_teams_input == 1:
                    balance_teams_by_experience = True
                else:
                    balance_teams_by_experience = False
                sleep()
                break
        print("\n")
        while True:
            try:
                print("When balancing the teams, would you like to randomize the order of players?")
                print("1) Yes")
                print("2) No")
                randomize_teams_input = input("\n Enter an option:  ")
                randomize_teams_input = int(randomize_teams_input)
            except ValueError:
                print(f"\n{randomize_teams_input} is not a valid selection. Please try again\n")
            else:
                if randomize_teams_input == 1:
                    randomize_teams = True
                else:
                    randomize_teams = False
                sleep()
                break
        print("\n")
        add_dots()
        print("Balancing Teams", end="")
        add_dots()
        print()
        sleep()
        config.players = balance_teams(config.teams, config.players, balance_teams_by_experience, randomize_teams)
        add_dots()
        print("Balancing Teams completed" + "."*10)
        time.sleep(2)
    else:
        config.players = balance_teams(config.teams, config.players, config.balanced, config.randomized)
    clear()


def start_program():
    ''' The purpose of the start_program function is to run
        the bulk of the program after the data has been
        initialized and cleaned up.

        Sets up the main menu. Ask to either display a
        team or quit. If diplaying a team, runs the
        display_team_stats function to show all of the data.
        Asks the user if they want to continue or quit.'''

    continue_running = True
    while continue_running:
        print("Welcome to the Basketball Team Stats Tool!\n")
        sleep()
        print("-"*5 + "Menu" + "-"*5 + "\n")
        sleep()
        print("Menu Options:".center(15))
        for counter, option in enumerate(config.menu_items, 1):
            print("{}) {}".format(counter, option))
        sleep()
        user_selection = input("\nEnter an option:  ")
        try:
            while True:
                if user_selection == "1":  # Display teams options
                    print("\nSelect which team you would like to see stats for:\n")
                    sleep()
                    for counter, team in enumerate(config.teams, 1):
                        print("{}) {}".format(counter, team))
                    sleep()
                    team_option_selection = input("\nEnter an option:  ")
                    clear()
                    display_team_stats(team_option_selection, config.teams, config.players)
                    sleep()
                    print("Do you want to see another team?")
                    print("1) Yes")
                    print("2) No")
                    user_selection = input("\nEnter an option:  ")
                elif user_selection == "2":  # Quit
                    sleep()
                    print("\nThank you for using the Basketball Team Stats Tool!\n")
                    sleep()
                    print("Have a great day!")
                    sleep()
                    continue_running = False
                    break
                else:
                    raise ValueError(f"\n{user_selection} is not a valid selection. Please try again\n")
        except ValueError as err:
            sleep()
            print(err)
            sleep()
            clear()

if __name__ == '__main__':  # Dunder main
    initiate_data()
    start_program()
