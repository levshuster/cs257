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

try:
    connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
except Exception as e:
    print(e)
    exit()



@app.route('/')
def hello():
    return 'Hello, Citizen of CS257.'


'''    
    REQUEST: /games

    RESPONSE: a JSON list of dictionaries, each of which represents one
    Olympic games, sorted by year. Each dictionary in this list will have
    the following fields.

    id -- (INTEGER) a unique identifier for the games in question
    year -- (INTEGER) the 4-digit year in which the games were held (e.g. 1992)
    season -- (TEXT) the season of the games (either "Summer" or "Winter")
    city -- (TEXT) the host city (e.g. "Barcelona")
'''
@app.route('/games')
def get_games():

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

    return json.dumps(noc_regions_list)

@app.route('/movies')
def get_movies():
    ''' Returns the list of movies that match GET parameters:
        start_year, int: reject any movie released earlier than this year
        end_year, int: reject any movie released later than this year
        genre: reject any movie whose genre does not match this genre exactly
        If a GET parameter is absent, then any movie is treated as though
        it meets the corresponding constraint. (That is, accept a movie unless
        it is explicitly rejected by a GET parameter.)
    '''
    movie_list = []
    genre = flask.request.args.get('genre')
    start_year = flask.request.args.get('start_year', default=0, type=int)
    end_year = flask.request.args.get('end_year', default=10000, type=int)
    for movie in movies:
        if genre is not None and genre != movie['genre']:
            continue
        if movie['year'] < start_year:
            continue
        if movie['year'] > end_year:
            continue
        movie_list.append(movie)

    return json.dumps(movie_list)


@app.route('/help')
def get_help():
    return flask.render_template('help.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)

