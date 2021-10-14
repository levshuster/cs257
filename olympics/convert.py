'''
    code by lev shuster
    due oct 14 2021 for cs257
    started oct 11th 2021
    
    ditched age because didn't emprove usability and dramatically increased complexity
    original data from https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results

'''
import os #used by the display_status function
import csv

existing_athletes = set() #stores all the athlete id #s that have already been processed
existing_game_years = dict() #stores all the diffrent olimpics and their ids
existing_event = dict() #stores all the olimpic events and their ids


# used to provide unique IDs 
game_counter = -1
event_counter = -1


def parse_athlete_events(athlete_events_input_file_name):
    reader = csv.reader(open(athlete_events_input_file_name))
    next(reader)    # skip header row

    athlete_writer = create_destination_csv('athlete.csv')
    game_writer = create_destination_csv('game.csv')
    event_writer = create_destination_csv('event.csv')
    link_list_writer = create_destination_csv('metalAthleteTeam.csv')

    for row in reader:
        working_row = parsed_row(row)

        # set to true if you want % progress updates
        display_status(working_row, True)

        create_athlete(working_row, athlete_writer)
        game = create_game(working_row, game_writer)
        event = create_event(working_row, event_writer)
        create_link_list(working_row, event, game, link_list_writer)

'''
    create_athlete will contain:   id, last name, full name, and sex
'''
def create_athlete(row, writer):
    athlete_id = row.id
    if athlete_id not in existing_athletes:
        existing_athletes.add(athlete_id)
        writer.writerow([athlete_id, row.name.split()[-1], row.name, row.sex])

'''
    create_game will contain:   id, year, season, and city
'''
def create_game(row, writer):
    game_year_and_season = row.year + row.season
    global game_counter
    if game_year_and_season not in existing_game_years:
        game_counter = game_counter +1
        existing_game_years[game_year_and_season] = game_counter
        writer.writerow([game_counter, row.year, row.season, row.city])
        return game_counter
    else:        
        return existing_game_years[game_year_and_season]

'''
    create_event will contain:   id, sport, event
'''
def create_event(row, writer):
    sport_event_game_id = row.sport + row.event
    global event_counter
    if sport_event_game_id not in existing_event:
        event_counter = event_counter +1
        existing_event[sport_event_game_id] = event_counter
        writer.writerow([event_counter, row.sport, row.event])
        return event_counter
    else:        
        return existing_event[sport_event_game_id]

'''
    create_link_list will contain:   id, event_id, metal
'''
def create_link_list(row, event, game, writer):
    writer.writerow([row.id, event, game, row.metal])





class parsed_row:
    '''
        0 ID - Unique number for each athlete
        1 Name - Athlete's name
        2 Sex - M or F
        3 Age - Integer
        4 Height - In centimeters
        5 Weight - In kilograms
        6 Team - Team name
        7 NOC - National Olympic Committee 3-letter code
        8 Games - Year and season
        9 Year - Integer
       10 Season - Summer or Winter
       11 City - Host city
       12 Sport - Sport
       13 Event - Event
       14 Medal - Gold, Silver, Bronze, or NA
    '''
    def __init__(self, raw_row):
        self.id = int(raw_row[0])
        self.name = raw_row[1]
        self.sex = raw_row[2]
        self.NOC = raw_row[7]
        self.year = raw_row[9]
        self.season = raw_row[10]
        self.city = raw_row[11]
        self.sport = raw_row[12]
        self.event = raw_row[13]
        self.metal = raw_row[14]

def create_destination_csv(destination_file_name):
    return csv.writer(open(destination_file_name, 'w'))


'''
    because my old thinkpad takes minutes to process here is a progress method 
    so I don't need to keep calling wc -l athlete.csv to make sure everything is 
    progresssing
'''
def display_status(row, display_should_run):
    if display_should_run:
        NUMBER_OF_ATHLETE_IDS = 134000
        if row.id % 2000 == 0:
            last_percentage_displayed = row.id
            os.system('cls' if os.name=='nt' else 'clear')
            print(int(row.id/NUMBER_OF_ATHLETE_IDS * 100), " percent complete")

if __name__ == '__main__':
    parse_athlete_events('athlete_events.csv')
