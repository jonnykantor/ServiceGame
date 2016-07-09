import pygame, math, sys, os
from pygame.locals import *
from random import randint
from Globals import *

class CharacterObject(pygame.sprite.Sprite):
	def __init__(self, screen, images, starting_position, x_limits=None):
		pygame.sprite.Sprite.__init__(self)
		
		self.x_movement_limit_left = None
		self.x_movement_limit_right = None
		if x_limits != None:
			self.x_movement_limit_left = x_limits[0]
			self.x_movement_limit_right = x_limits[1]
			
		self.screen = screen
		self.images = images
		self.image = images[0]		
		self.pos = starting_position		
		
		self.rect = self.image.get_rect()		
		self.rect.center = self.pos		
		
		#image lists by direction
		self.left_images 	= self.images[:LEFT_3	+ 1	]		
		self.right_images 	= self.images[LEFT_3 	+ 1	:RIGHT_3 	+ 1	]
		#currently only using left/right animations
		'''
		self.idle_images 	= self.images[RIGHT_3	+ 1 :IDLE_3 	+ 1	]				
		self.up_images 		= self.images[IDLE_3 	+ 1	:UP_3 		+ 1	]
		self.down_images 	= self.images[UP_3 		+ 1	:DOWN_3 	+ 1	]
		'''
		
		#collision rectangles and stats
		self.bottom_collision_rect = pygame.Rect( self.rect.bottomleft, ( self.rect.width, FLOOR_HEIGHT - self.rect.bottom ) )		
		self.right_side_collision_rect = pygame.Rect( self.rect.topright, (RIGHT_RECT_WIDTH, self.rect.height-2) )
		self.left_side_collision_rect = pygame.Rect( (self.rect.left - LEFT_RECT_WIDTH, self.rect.top), self.rect.bottomleft )
		
		self.isCollidingRight = False
		self.isCollidingLeft = False
		self.isCollidingBottom = False
		
		#individual counters for individual image list current image position
		self.idle_ind 	= 0
		self.left_ind 	= 0
		self.right_ind 	= 0
		self.up_ind 	= 0
		self.down_ind 	= 0
		
		#jump stats
		self.jumpCounter 	= 0
		self.isAirborne 	= False
		self.fall_speed 	= 0
		self.jump_speed 	= 15
		
	def update(self, direction, left_side_collision_list, right_side_collision_list, bottom_collision_list):
		
		collide_left = self.left_side_collision_rect.collidelist(left_side_collision_list) 
		collide_right = self.right_side_collision_rect.collidelist(right_side_collision_list) 
		collide_bottom = self.bottom_collision_rect.collidelist(bottom_collision_list) 
		
		#test for collisions
		if collide_left == -1: self.isCollidingLeft = False
		else: self.isCollidingLeft = True
		if collide_right == -1: self.isCollidingRight = False
		else: self.isCollidingRight = True
		if collide_bottom == -1: self.isCollidingBottom = False
		else: self.isCollidingBottom = True			
		
		#jump indicated, not already in the air
		if direction == UP and not self.isAirborne:	
			self.jumpCounter = 5					
		
		if direction == LEFT:
			self.right_ind = 0			
			if collide_left == -1: #if not colliding to the left
				self.isCollidingLeft = False
				#update image for animation
				if self.left_ind == 15: self.left_ind = 0 
				else: self.left_ind += 1
				self.image = self.left_images[self.left_ind/5]					
			else: #colliding left				
				self.isCollidingLeft = True
		elif direction == RIGHT:
			self.left_ind = 0
			if collide_right == -1: #if not colliding tot he right
				self.isCollidingRight = False
				#update image for animation
				if self.right_ind == 15: self.right_ind = 0
				else: self.right_ind += 1
				self.image = self.right_images[self.right_ind/5]		
			else: #colliding right
				self.isCollidingRight = True
		
		#direction != left, direction != right, upward movement required from jump
		elif self.jumpCounter > 0:			
			self.isAirborne = True
			self.jumpCounter -= 1
			self.pos = (self.pos[0], self.pos[1]-self.jump_speed*self.jumpCounter)			
			
		#airborne from jump, or simply above the floor height, and not colliding with anything below
		elif self.isAirborne or self.pos[1] < FLOOR_HEIGHT:
							
			#extending collision rectangle from bottom of self.rect up to current fall_speed
			if collide_bottom != -1:				
				if ( abs(self.rect.bottom - bottom_collision_list[collide_bottom].top) ) <= ( self.fall_speed + 2 ):
					self.isCollidingBottom = True
					self.isAirborne = False
					self.fall_speed = 0
					self.pos = (self.pos[0], bottom_collision_list[collide_bottom].top - self.rect.height/2 - 1)							
			
			if self.pos[1] < FLOOR_HEIGHT:
				self.fall_speed += 2
				self.pos = (self.pos[0], self.pos[1]+self.fall_speed)
				
		#somehow below the floor, move back to floor	
		if self.pos[1] > FLOOR_HEIGHT: 
			self.isAirborne = False
			self.fall_speed = 0
			self.pos = (self.pos[0], FLOOR_HEIGHT)
				
		self.rect = self.image.get_rect()
		self.rect.center = self.pos		
		
		#re-set collision rects based on new character object self.rect location
		self.bottom_collision_rect = pygame.Rect( self.rect.bottomleft, ( self.rect.width, self.fall_speed ) ) 
		self.right_side_collision_rect = pygame.Rect( self.rect.topright, (RIGHT_RECT_WIDTH, self.rect.height-2) )
		self.left_side_collision_rect = pygame.Rect( (self.rect.left - LEFT_RECT_WIDTH, self.rect.top), (LEFT_RECT_WIDTH, self.rect.height-2) )		
	
class AICharacterObject(CharacterObject):
	def __init__(self, screen, images, starting_position, ai_type = 0):
		CharacterObject.__init__(self, screen, images, starting_position)
		self.char_type = ai_type
	
	def update(self, direction, left_side_collision_list, right_side_collision_list, bottom_collision_list):
		move_speed = BACKGROUND_SPEED
		if direction == LEFT and self.isCollidingLeft == False: 					
			self.pos = (self.pos[0] - move_speed, self.pos[1])
		elif direction == RIGHT and self.isCollidingRight == False: 			
			self.pos = (self.pos[0] + move_speed, self.pos[1])
		elif direction == PLAYER_LEFT_ONLY: 
			self.pos = (self.pos[0] + move_speed, self.pos[1])
			direction = None
		elif direction == PLAYER_RIGHT_ONLY: 
			self.pos = (self.pos[0] - move_speed, self.pos[1])
			direction = None
		super(AICharacterObject, self).update(direction, left_side_collision_list, right_side_collision_list, bottom_collision_list)	
	
class PlayerObject(CharacterObject):
	def __init__(self, screen, images, starting_position):
		CharacterObject.__init__(self, screen, images, starting_position)
	
	def update(self, direction, left_side_collision_list, right_side_collision_list, bottom_collision_list):		
		move_speed = BACKGROUND_SPEED
		if direction == LEFT:
			if self.pos[0] > SCREEN_WIDTH/2 + move_speed:
				self.pos = (self.pos[0] - move_speed, self.pos[1])				
			elif self.pos[0] > SCREEN_WIDTH/2:
				self.pos = (SCREEN_WIDTH/2, self.pos[1])
		elif direction == RIGHT:
			if self.pos[0] < SCREEN_WIDTH/2 - move_speed:
				self.pos = (self.pos[0] + move_speed, self.pos[1])				
			elif self.pos[0] < SCREEN_WIDTH/2:
				self.pos = (SCREEN_WIDTH/2, self.pos[1])
		elif direction == PLAYER_LEFT_ONLY:
			self.pos = (self.pos[0] - move_speed, self.pos[1])
			direction = LEFT
		elif direction == PLAYER_RIGHT_ONLY:
			self.pos = (self.pos[0] + move_speed, self.pos[1])
			direction = RIGHT		
		super(PlayerObject, self).update(direction, left_side_collision_list, right_side_collision_list, bottom_collision_list)