'''
    code by lev shuster
    due oct 21 2021 for cs257
    started oct 17th 2021
'''

import argparse, wikipedia, sys

''' 
    set up get_parsed_argument and psycopg2, direct parse results to 
    proper sql method, and then print the results.
'''
def main(argv):
    arguments = get_parsed_argument()
    if arguments.golds:
        print_gold()
    elif arguments.athletes:
        print_athletes(arguments.athletes)
    elif arguments.country_info:
        print_country_info()

def get_parsed_argument():
    parser = argparse.ArgumentParser(description='Process data on ~60 years of olympics.               original data from https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results               Program by Lev Shuster')
    
    # parse searches
    parser.add_argument('--athletes','-a',help='List the names of all the athletes from a specified NOC')
    parser.add_argument('--golds','-g',action='store_true',help='List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.')
    parser.add_argument('--country_info','-i',action='store_true',help='Displays the wikipedia introductions to each country that has exacly two gold metals')

    return parser.parse_args()


def print_gold():
    print("golds")

def print_athletes(input_NOC):
    print("athletes")

'''
    this function is helpful because it gets the user to learn about the smaller/less sucsessful countries that have sucseeded at the olympics
'''
def print_country_info():
    #installs needed dependences and clears the output of pip
    import subprocess, os
    subprocess.check_call([sys.executable, "-m", "pip", "install", "wikipedia"])
    os.system('cls' if os.name=='nt' else 'clear')
    print("country info")
    

if __name__ == '__main__':
    main(sys.argv[1:])