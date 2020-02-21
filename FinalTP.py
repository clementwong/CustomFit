# FinalTP.py
# Made by Clement Wong, clementw
from DesignBoard import *
from TshirtDemo import * 
import pygame
class CustomFit (object): 
	def __init__ (self): 
		self.playing = True
		self. textboxes =[]
		self.images = []
		self.tshirt = None
		self.start = True
	def run (self):
		while (self.playing):

			designPygame = DesignPygame(self.textboxes, self.images, self.tshirt,self.start).run()
			#trying on the design
			if (designPygame ==None):
				self.playing=False
				break
			(self.textboxes, self.images, self.tshirt) = designPygame
			#quitted the program

			tshirtDisplay = TshirtDisplay(self.textboxes,self.images,self.tshirt).run()
			if (tshirtDisplay==None): 
				self.playing = False
				break
			self.start = False
			
customFit = CustomFit()
customFit.run()