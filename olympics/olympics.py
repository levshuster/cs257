'''
    code by Lev Shuster
    due oct 21 2021 for cs257
    started oct 17th 2021
'''

import argparse, sys, psycopg2, config

# set to false if you don't want my program to install the dependency that my third option relies on
SHOULD_INSTALL_WIKIPEDIA = True 


''' 
    set up get_parsed_argument and psycopg2, direct parse results to 
    proper sql method, and then print the results.
'''
def main(argv):
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e)
        exit()

    arguments = get_parsed_argument()

    if arguments.golds:
        print_gold(connection)
    elif arguments.athletes:
        print_athletes(connection, arguments.athletes)
    elif arguments.country_info:
        print_country_info(connection)

def get_parsed_argument():
    parser = argparse.ArgumentParser(description='Process data on ~60 years of olympics.               original data from https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results               Program by Lev Shuster')
    
    # parse searches
    parser.add_argument('--athletes','-a',help='List the names of all the athletes from a specified NOC')
    parser.add_argument('--golds','-g',action='store_true',help='List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.')
    parser.add_argument('--country_info','-i',action='store_true',help='Displays the wikipedia introductions to each country that has exacly two gold metals')

    return parser.parse_args()


def print_gold(connection):
    # SQL Call
    try:
        cursor = connection.cursor()
        query = "SELECT noc_regions.NOC_name, COUNT(*) FROM noc_regions, athlete_NOC_event_game_metal WHERE noc_regions.NOC_abbreviation = athlete_NOC_event_game_metal.NOC_abbreviation AND athlete_NOC_event_game_metal.metal = 'Gold' GROUP BY noc_regions.NOC_name  ORDER BY COUNT(*) DESC;"
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    # Display Results
    print("golds")
    print('===== All NOCs and the number of their gold metals =====')
    for row in cursor:
        print(row[0], row[1])
        print()

def print_athletes(input_NOC):
    # SQL Call

    # Display Results
    print("athletes")

'''
    this function is helpful because it gets the user to learn about the smaller/less sucsessful countries that have still sucseeded at the olympics
'''
def print_country_info():
    if SHOULD_INSTALL_WIKIPEDIA:

        # Installs needed dependences and clears the output of pip
        import subprocess, os
        subprocess.check_call([sys.executable, "-m", "pip", "install", "wikipedia"])
        os.system('cls' if os.name=='nt' else 'clear')
        import wikipedia
        
        # SQL Call

        # Display Results
        print("country info")
    

if __name__ == '__main__':
    main(sys.argv[1:])