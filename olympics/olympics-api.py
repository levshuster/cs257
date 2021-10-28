'''
    Lev Shuster
    10/25/21

    looping to create a dictonary was loosly based on code Anthony DeBarro's 
    code at https://anthonydebarros.com/2020/09/06/generate-json-from-sql-using-python/
'''

# to set up flask server
import sys, argparse, flask, json

# to acsess sql database
import psycopg2, config

 
app = flask.Flask(__name__)

def get_connection():
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e)
        exit()
    return connection



# @app.route('/')
# def hello():
#     return 'Hello, Citizen of CS257.'


# '''    
#     REQUEST: /games

#     RESPONSE: a JSON list of dictionaries, each of which represents one
#     Olympic games, sorted by year. Each dictionary in this list will have
#     the following fields.

#     id -- (INTEGER) a unique identifier for the games in question
#     year -- (INTEGER) the 4-digit year in which the games were held (e.g. 1992)
#     season -- (TEXT) the season of the games (either "Summer" or "Winter")
#     city -- (TEXT) the host city (e.g. "Barcelona")
# '''
@app.route('/games')
def get_games():
    connection = get_connection()

    # SQL Call
    try:
        cursor = connection.cursor()
        query =  '''SELECT game.id, game.year, game.season, game.city FROM game
                    ORDER BY game.year;'''
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    # Convert Results to JSON format
    olympics_games_list = []
    for row in cursor:
        olympics_game = {}
        olympics_game['id'] = int(row[0])
        olympics_game['year'] = int(row[1])
        olympics_game['season'] = row[2]
        olympics_game['city'] = row[3]

        olympics_games_list.append(olympics_game)

    connection.close()    
    return json.dumps(olympics_games_list)


'''
    REQUEST: /nocs

    RESPONSE: a JSON list of dictionaries, each of which represents one
    National Olympic Committee, alphabetized by NOC abbreviation. Each dictionary
    in this list will have the following fields.

    abbreviation -- (TEXT) the NOC's abbreviation (e.g. "USA", "MEX", "CAN", etc.)
    name -- (TEXT) the NOC's full name (see the noc_regions.csv file)
'''
@app.route('/nocs')
def get_nocs():

    connection = get_connection()

    # SQL Call
    try:
        cursor = connection.cursor()
        query =  '''SELECT noc_regions.NOC_abbreviation, noc_regions.NOC_name FROM noc_regions
                    ORDER BY noc_regions.NOC_abbreviation;'''
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    # Convert Results to JSON format
    noc_regions_list = []
    for row in cursor:
        noc_region = {}
        noc_region['abbreviation'] = row[0]
        noc_region['name'] = row[1]

        noc_regions_list.append(noc_region)

    connection.close()    
    return json.dumps(noc_regions_list)



'''
    REQUEST: /medalists/games/<games_id>?[noc=noc_abbreviation]

    RESPONSE: a JSON list of dictionaries, each representing one athlete
    who earned a medal in the specified games. Each dictionary will have the
    following fields.

    athlete_id -- (INTEGER) a unique identifier for the athlete
    athlete_name -- (TEXT) the athlete's full name
    athlete_sex -- (TEXT) the athlete's sex as specified in the database ("F" or "M")
    sport -- (TEXT) the name of the sport in which the medal was earned
    event -- (TEXT) the name of the event in which the medal was earned
    medal -- (TEXT) the type of medal ("gold", "silver", or "bronze")

    If the GET parameter noc=noc_abbreviation is present, this endpoint will return
    only those medalists who were on the specified NOC's team during the specified
    games.
'''
@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):


    connection = get_connection()

    noc = flask.request.args.get('noc')

    query = '''SELECT athlete.id, athlete.whole_name, athlete.sex, event.sport, event.athletic_event, athlete_NOC_event_game_metal.metal
    FROM athlete, event, athlete_NOC_event_game_metal, game
    WHERE athlete_NOC_event_game_metal.event_ID = event.id
    AND athlete_NOC_event_game_metal.athlete_ID = athlete.id 
    AND athlete_NOC_event_game_metal.game_ID = game.ID
    AND game.ID = ''' + games_id

    # if noc:
    #     query += ' AND athlete_NOC_event_game_metal.NOC_abbreviation = ' + noc
    
    query += ' ORDER BY athlete.whole_name;'

    # SQL Call
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    # Convert Results to JSON format
    athletes_list = []
    for row in cursor:
        athlete = {}
        athlete['athlete_id'] = int(row[0])
        athlete['athlete_name'] = row[1]
        athlete['athlete_sex'] = row[2]
        athlete['sport'] = row[3]        
        athlete['event'] = row[4]
        athlete['medal'] = row[5]

        if athlete['medal'] != "NA":
            athletes_list.append(athlete)

    connection.close()    
    return json.dumps(athletes_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A Flask application/API to handle the olympics database')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)

