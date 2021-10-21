'''
    code by Lev Shuster
    due oct 21 2021 for cs257
    started oct 17th 2021
'''

import argparse, sys, psycopg2, config

# set to false if you don't want my program to install the dependency that my third option 
# relies on (you can test all the required content besides the "create your own operation" 
# without installing any additional dependencies")
SHOULD_INSTALL_WIKIPEDIA = True 


''' 
    set up get_parsed_argument and psycopg2 then direct parse results to 
    proper sql method.
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
        print_athletes(connection, str(arguments.athletes))
    elif arguments.country_info:
        print_country_info(connection)
    connection.close()


def get_parsed_argument():
    parser = argparse.ArgumentParser(description='Process data on ~60 years of olympics.               original data from https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results               Program by Lev Shuster')
    
    parser.add_argument('--athletes','-a',help='List the names of all the athletes from a specified NOC')
    parser.add_argument('--golds','-g',action='store_true',help='List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.')
    parser.add_argument('--country_info','-i',action='store_true',help='Displays the wikipedia introductions to each country that has exacly two gold metals. This is done so the user can learn about some of the less know countries sucsess at the olympics')

    return parser.parse_args()


def print_gold(connection):
    # SQL Call
    try:
        cursor = connection.cursor()
        query = "SELECT noc_regions.NOC_abbreviation, COUNT(CASE WHEN athlete_NOC_event_game_metal.metal = 'Gold' THEN 1 END) FROM noc_regions, athlete_NOC_event_game_metal WHERE noc_regions.NOC_abbreviation = athlete_NOC_event_game_metal.NOC_abbreviation GROUP BY noc_regions.NOC_abbreviation ORDER BY COUNT(CASE WHEN athlete_NOC_event_game_metal.metal = 'Gold' THEN 1 END)  DESC;"
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    # Display Results
    print('===== All NOCs and the number of their gold metals =====')
    for row in cursor:
        print(row[0], row[1])


def print_athletes(connection, input_NOC):
    # SQL Call
    try:
        cursor = connection.cursor()
        query =  '''SELECT athlete.whole_name FROM athlete, athlete_NOC_event_game_metal, noc_regions
                    WHERE athlete.id = athlete_NOC_event_game_metal.athlete_ID
                    AND   noc_regions.NOC_abbreviation=athlete_NOC_event_game_metal.NOC_abbreviation
                    AND  (noc_regions.NOC_abbreviation=%s OR noc_regions.NOC_name=%s)
                    GROUP BY athlete.whole_name
                    ORDER BY athlete.whole_name;'''
        cursor.execute(query, (input_NOC,input_NOC,))
    except Exception as e:
        print(e)
        exit()

    # Display Results
    print('===== List athletes from ' + input_NOC+'=====')
    for row in cursor:
        print(row[0])


'''
    this function is helpful because it gets the user to learn about the smaller/less sucsessful countries that have still sucseeded at the olympics
'''
def print_country_info(connection):
    NUMBER_OF_SENTENCES_TO_PRINT = 3
    NUMBER_OF_GOLD_METALS_TO_FOCUS_ON = 2

    if SHOULD_INSTALL_WIKIPEDIA:

        # Installs/Imports needed dependences and clears the output of pip
        import subprocess, os
        subprocess.check_call([sys.executable, "-m", "pip", "install", "wikipedia"])
        os.system('cls' if os.name=='nt' else 'clear')
        import wikipedia
        
        # SQL Call
        try:
            cursor = connection.cursor()
            query =  '''SELECT noc_regions.NOC_name FROM noc_regions,
                        (SELECT noc_regions.NOC_abbreviation, COUNT(CASE WHEN athlete_NOC_event_game_metal.metal = 'Gold' THEN 1 END) 
                        FROM noc_regions, athlete_NOC_event_game_metal 
                        WHERE noc_regions.NOC_abbreviation = athlete_NOC_event_game_metal.NOC_abbreviation 
                        GROUP BY noc_regions.NOC_abbreviation) AS metal_count
                        WHERE noc_regions.NOC_abbreviation = metal_count.NOC_abbreviation
                        AND metal_count.count = %s;'''
            cursor.execute(query, (NUMBER_OF_GOLD_METALS_TO_FOCUS_ON,))
        except Exception as e:
            print(e)
            exit()

        # Display Results
        for row in cursor:
            country = row[0]
            print("\n\n---Introduction to "+country+" from wikipedia---")
            try:
                print(wikipedia.summary(country, sentences = NUMBER_OF_SENTENCES_TO_PRINT))
            except wikipedia.exceptions.PageError:
                print("No Data Availible")
    else:
        print("To see my personal function please allow this program to dowload the wikipedia package by setting SHOULD_INSTALL_WIKIPEDIA to True")


if __name__ == '__main__':
    main(sys.argv[1:])