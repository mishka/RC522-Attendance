from RGB import RGB
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from os import getcwd as cwd
from os.path import exists
import json


RGB = RGB()
reader = SimpleMFRC522()
GPIO.setwarnings(False)
cards = cwd() + '/cards.json'

# Check if the program is being executed for the first time, if so generate a new file #

if not exists(cards):
    print('Card information file doesn\'t exist, creating..')
    with open(cards, 'w') as f:
        json.dump({}, f)


try:    
    while(1):
        RGB.set_color(255, 255, 0)
        print('Waiting for card input!\n')
        
        id, _ = reader.read()
        id = str(id)

        if id:
            print('Card found! Card ID is:', id)
            card_owner = input('Please enter the name of the new owner: ')
            
            # It will break the csv file if they put a comma here, so remove it if there's one!
            if ',' in card_owner:
                card_owner = card_owner.replace(',' ' ')
            
            with open(cards, 'r') as f:
                data = json.load(f)

            with open(cards, 'w') as f:
                data[id] = card_owner
                json.dump(data, f, indent=4, sort_keys=True)
            
            RGB.set_color(0, 255, 0)
            print('\nRegistered the card successfully!')
            choice = input('\nWould you like to register another card?\nType "yes" to continue, "no" to exit: ')

            if choice == 'yes':
                continue
            else:
                GPIO.cleanup()
                quit()

except KeyboardInterrupt:
    GPIO.cleanup()