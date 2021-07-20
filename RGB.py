from rpi_ws281x import PixelStrip, Color
from time import sleep
import atexit


class LED:
	PIN        = 18     # GPIO pin connected to the pixels (18 uses PWM, 10 uses SPI /dev/spidev0.0)
	DMA        = 10     # DMA channel to use for generating signal (try 10)
	COUNT      = 12		# Number of LED pixels
	CHANNEL    = 0      # Set to '1' for GPIOs 13, 19, 41, 45 or 53
	INVERT     = False  # True to invert the signal (when using NPN transistor level shift)
	FREQ_HZ    = 800000 # LED signal frequency in hertz (usually 800khz)
	BRIGHTNESS = 100    # Set to 0 for darkest and 255 for brightest


class RGB:
	def __init__(self):
		"""Setups the LEDs and starts it."""
		self.strip = PixelStrip(LED.COUNT, LED.PIN, LED.FREQ_HZ, LED.DMA, LED.INVERT, LED.BRIGHTNESS, LED.CHANNEL)
		self.strip.begin()
		# Always clean the LEDs upon exiting.
		atexit.register(self.clear)


	def clear(self, slowly=True):
		"""Turns off the LEDs. Set to False if you don't want to turn them off one by one. Default is True."""
		slowly = 0 if not slowly else 50
		self.set_color(0, 0, 0, slowly)


	def set_color(self, red, green, blue, wait_ms=50):
		"""Set color across display a pixel at a time."""
		for i in range(LED.COUNT):
			self.strip.setPixelColor(i, Color(red, green, blue))
			self.strip.show()
			sleep(wait_ms / 1000)


	def wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)


	def rainbow(self, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		for j in reversed(range(256 * iterations)):
			for i in range(LED.COUNT):
				self.strip.setPixelColor(i, self.wheel((i + j) & 255))
			self.strip.show()
			sleep(wait_ms / 500)


	def rainbow_cycle(self, iterations=5):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		for j in reversed(range(256 * iterations)):
			for i in range(LED.COUNT):
				self.strip.setPixelColor(i, self.wheel(
					(int(i * 256 / LED.COUNT) + j) & 255))
			self.strip.show()
			sleep(1 / 1000)


	def theater_chase(self, red, green, blue, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		for j in range(iterations):
			for q in range(3):
				for i in range(0, LED.COUNT, 3):
					self.strip.setPixelColor(i + q, Color(red, green, blue))
				self.strip.show()
				sleep(wait_ms / 1000)
				for i in range(0, LED.COUNT, 3):
					self.strip.setPixelColor(i + q, 0)


	def theater_chase_rainbow(self, wait_ms=50):
		"""Rainbow movie theater light style chaser animation."""
		for j in range(256):
			for q in range(3):
				for i in range(0, LED.COUNT, 3):
					self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
				self.strip.show()
				sleep(wait_ms / 1000)
				for i in range(0, LED.COUNT, 3):
					self.strip.setPixelColor(i + q, 0)