# How does it work?
The program creates a new log file every monday, which can be found in the `logs` folder.  
The format of the log file is `csv`, so it can easily be imported to **Excel** as shown below;  
  
![image](https://i.imgur.com/UjyuQN5.png)

# Video demos
## Registering new cards to the system
https://user-images.githubusercontent.com/25265212/126251793-2c10412d-8e5a-42e4-84ec-60b0f6c576a9.mp4

## Logging in action
https://user-images.githubusercontent.com/25265212/126251928-f49a8bf9-d490-4379-ad03-2b3fa92fa593.mp4

## Current things to do
- [ ] Try to trigger for errors and make the program more stable.
* I coded the entire project in a day, so I haven't had the chance to test for bugs and errors. It works stable so far but I want to make sure.  
  
# Setting up the GPIO Pins
## RFID-RC522

You can refer to [this](https://pimylifeup.com/wp-content/uploads/2017/08/RFID-GPIO-Connection.jpg) image.

| Name | Pin # | Pin name   |        
|------|-------|------------|
| SDA  | 24    | GPIO8      |
| SCK  | 23    | GPIO11     |
| MOSI | 19    | GPIO10     |
| MISO | 21    | GPIO9      |
| IRQ  | None  | None       |
| GND  | 39    | Ground     |
| RST  | 22    | GPIO25     |
| 3.3V | 1     | 3V3        |

## NeoPixel Ring - x12

| Name | Pin # | Pin name   |
|------|-------|------------|
| DIN  | 12    | GPIO18     |
| GND  | 14    | Ground     |
|  5V  | 2     | 5v Power   |

# Setting up the Raspberry Pi

* As the first thing, open up a terminal and type `sudo raspi-config` then enable the SPI interface from the **Interfacing options**.  
* Let's update the system and make sure the python is properly installed. Run the command below in a terminal.
> sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install python3-dev python3-pip
* Now let's install the python packages that we are going to use; run the command below in a terminal.
> sudo pip3 install spidev mfrc522 rpi_ws281x RPi.GPIO

# Program usage
* First you have to register the cards in the system. Run the command below, hover the card on the scanner, and the program will ask you to enter the name of the owner of that card. Once you enter a name, you will be given two choices. You can either type "yes" to continue registering cards, or you can type "no" to exit the program.
> sudo python3 register_cards.py
* If you've done registering the cards, now you can run the main program to start logging with the command below.
> sudo python3 read_cards.py
