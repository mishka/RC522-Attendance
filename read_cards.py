from RGB import RGB
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from pathlib import Path
from os import getcwd as cwd
from os.path import exists

import json, csv

from time import sleep
from datetime import datetime, timedelta


def time():
    return datetime.now().strftime('%H:%M:%S')


def date():
    return datetime.now().strftime('%d-%m-%Y')


def log(text):
    '''Prints with timestamp.'''
    print(f'| {date()} | {time()} | {text}')


def time_diff(time1, time2):
    '''Calculates the difference between two timestamps with "%d-%m-%Y %H:%M:%S" format.'''
    frmt = '%d-%m-%Y %H:%M:%S'
    return abs(datetime.strptime(time2, frmt) - datetime.strptime(time1, frmt))


def current_monday():
    '''Returns the date of this week's monday.'''
    now = datetime.now()
    monday = now - timedelta(days = now.weekday())
    return monday.strftime('%d-%m-%Y')


def check_weekly_file():
    '''If exists, returns the name of the weekly log file, if not, creates a new one.'''
    monday = current_monday()

    # Check if the log folder exists, if not create a new one
    Path(cwd() + '/logs').mkdir(parents = True, exist_ok = True)

    if exists(cwd() + f'/logs/{monday}.csv'):
        return monday + '.csv'
    else:
        log('This week\'s file doesn\'t exist, creating...')
        open(cwd() + f'/logs/{monday}.csv', 'w').close()
        return monday + '.csv'


def check_headers(csv_file):
    """Adds headers to the weekly log file if it's missing."""
    header = 'ID,USER,ARRIVED AT, LEFT AT,DURATION\n'
    with open(cwd() + f'/logs/{csv_file}', 'r') as f:
        header_exists = False if f.readline() != header else True
    
    if not header_exists:
        log('Adding header to the log file!')
        with open(cwd() + f'/logs/{csv_file}', 'a') as f:
            f.write(header)


def add_entry(id, user, time):
    # Get the log file ready
    log_file = check_weekly_file()
    check_headers(log_file)

    # Check if there is a previous entry, if so add it as an exit time
    # and calculate the duration difference of enter - exit times
    loines = []
    found_previous = False
    
    with open(cwd() + f'/logs/{log_file}', 'r') as r:
        for row in reversed(list(csv.reader(r))):
            if (','.join(row)).endswith(',,'):
                id_data, user_data, arrived_at = row[0], row[1], row[2]
                if int(id) == int(id_data):
                    found_previous = True
                    duration = time_diff(arrived_at, time)
                    loines.append(f'{id_data},{user_data},{arrived_at},{time},{duration}')
                else:
                    loines.append(','.join(row))
            else:
                loines.append(','.join(row))

    if found_previous:
        with open(cwd() + f'/logs/{log_file}', 'w') as f:
            for row in reversed(loines):
                f.write(row + '\n')
    else:
        with open(cwd() + f'/logs/{log_file}', 'a') as f:
            f.write(f'{id},{user},{time},,\n')


def get_username(id):
    '''Checks if the card is registered in the system.
    Returns False if the card is not registered.
    Returns the card owner name if it's registered'''
    
    with open(cwd() + '/cards.json', 'r') as f:
        data = json.load(f)
        user = data[str(id)]
        return user if user else False


print("Scanning for cards!\nPress CTRL-C to exit.")

reader = SimpleMFRC522()
RGB = RGB()

try:
    while(1):
        RGB.set_color(0, 255, 0, 20)
        
        id, _ = reader.read()
        
        RGB.clear()
        RGB.theater_chase(255, 43, 0)

        if id:
            user = get_username(id)
            
            if user:
                log(f'USER: {user} | CARD ID: {id}')
                add_entry(id, user, f'{date()} {time()}')
            else:
                log('THIS CARD IS NOT REGISTERED IN THE SYSTEM!!')
                log('PLEASE REGISTER THE CARD BEFORE TRYING TO USE IT!')

        RGB.set_color(255, 43, 0, 20)
        sleep(0.3)

except KeyboardInterrupt:
    GPIO.cleanup()