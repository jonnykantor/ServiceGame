import pygame, os
from sys import platform

CLOCK = pygame.time.Clock()

class Directions(object):
	def __init__(self, left, right, down, up, direction_key_states, center, player_left_only, player_right_only, nudge_left, nudge_right):
		self.left = left
		self.right = right
		self.down = down
		self.up = up
		self.direction_key_states = direction_key_states
		self.center = center
		self.player_left_only = player_left_only
		self.player_right_only = player_right_only
		self.nudge_left = nudge_left
		self.nudge_right = nudge_right

class MenuButtonCommands(object):
	def __init__(self, back, quit, controls, options, restart):
		self.BACK_TO_GAME = back
		self.QUIT = quit
		self.CONTROLS = controls
		self.OPTIONS = options
		self.RESTART = restart

class ColorDefs(object):	
		GREY 			=	(128, 128, 128)
		DARK_GREY		=	(50, 50, 50)
		RED				=	(255, 0, 0)
		GREEN 			=	(0, 255, 0)
		BLUE 			=	(0, 0, 255)
		LIGHT_BLUE 		=	(125, 125, 255)
		BLACK 			=	(0, 0, 0)
		GOLD 			=	(255, 215, 0)
		WHITE 			=	(255, 255, 255)
		YELLOW 			=	(255, 255, 0)
		TEST_COL		= 	(230, 240, 250)

class DimensionsAndLimits(object):
	AT_LIMIT_LEFT = 1
	AT_LIMIT_RIGHT = 2
	move_speed_limit_denom = 2
	def __init__(	self, 
					screen_width, 
					screen_height, 
					char_collision_rect_left_width, 
					char_collision_rect_right_width ):

		self.screen_height = screen_height
		self.screen_width = screen_width
		self.left_rect_width = char_collision_rect_left_width
		self.right_rect_width = char_collision_rect_right_width
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		self.screen_rect = self.screen.get_rect()
		self.x_scroll_limit_left = self.screen_width/2
		self.x_scroll_limit_right = self.screen_width/2
		self.x_scroll_limits = (self.x_scroll_limit_left, self.x_scroll_limit_right)
		self.x_limit_test_pos = self.screen_width/2

class MovementMeasures(object):
	def __init__(self, background_speed, foreground_speed, nudge_amount):
		self.background_speed = background_speed
		self.foreground_speed = foreground_speed
		self.nudge_amount = nudge_amount

class DrawPositions(object):
	def __init__(self, character_y_pos, drum_kit_position, foreground_asset_positions, background_asset_positions_near, background_asset_positions_far):
		self.character_y_pos = character_y_pos
		self.drum_kit_position = drum_kit_position
		self.foreground_asset_positions = foreground_asset_positions
		self.background_asset_positions_near = background_asset_positions_near
		self.background_asset_positions_far = background_asset_positions_far

class TextObjectTypes(object):
	POINTS_FADING = 0
	SPEECH_BUBBLE = 1

class ArtAssets(object):
	slash = '/'

	def __init__(self, path):
		if platform == "Win32": 
			self.slash = "\\"
		self.path = path + self.slash
		self.drummer_path = "DRUMMER" + self.slash
		self.player_asset_fnames = []				#to be updated with player-chosen art-assets once those are actually drawn
		self.ai_character_asset_fnames = []			#to be updated with player-chosen art-assets once those are actually drawn
		self.foreground_asset_fnames = [
									'Foreground_Crowd_Shadows_1.png']
		self.background_asset_fnames_near = [
									'Drum_Kit_Plus_Stands.png',
									'Stage_Background_Near_1.png',
									'Background_Crowd_Outlines.png']
		self.background_asset_fnames_far = [
									'Stage_Background_Far_1.png',
									'DRUMMER/Drummer_Immobile_Area.png']	
		self.drummer_asset_fnames = [
									['DRUMMER_LEFT_Arm_Floor_Tom_Hit.png'],
									
									['DRUMMER_LEFT_Arm_Neutral_1.png',
									'DRUMMER_LEFT_Arm_Neutral_2.png'],
									
									['DRUMMER_LEFT_Hand_Up_1.png',
									'DRUMMER_LEFT_Hand_Up_2.png',
									'DRUMMER_LEFT_Hand_Up_3.png',
									'DRUMMER_LEFT_Hand_Up_4.png',
									'DRUMMER_LEFT_Hand_Up_5.png'],

									['DRUMMER_RIGHT_Arm_Neutral_1.png',
									'DRUMMER_RIGHT_Arm_Neutral_2.png'],

									['DRUMMER_RIGHT_Hand_Up_1.png',
									'DRUMMER_RIGHT_Hand_Up_2.png',
									'DRUMMER_RIGHT_Hand_Up_3.png',
									'DRUMMER_RIGHT_Hand_Up_4.png',
									'DRUMMER_RIGHT_Hand_Up_5.png'],

									['DRUMMER_High_Hat_UP.png',
									'DRUMMER_High_Hat_DOWN.png'],

									['DRUMMER_High_Hat_FOOT_UP.png',
									'DRUMMER_High_Hat_FOOT_DOWN.png'],

									['DRUMMER_Cymbal_LEFT_STILL.png',
									'DRUMMER_Cymbal_LEFT_HIT_1.png',
									'DRUMMER_Cymbal_LEFT_HIT_2.png',
									'DRUMMER_Cymbal_LEFT_HIT_1.png',
									'DRUMMER_Cymbal_LEFT_STILL.png',
									'DRUMMER_Cymbal_LEFT_HIT_REVERSE_1.png',
									'DRUMMER_Cymbal_LEFT_HIT_REVERSE_2.png',
									'DRUMMER_Cymbal_LEFT_HIT_REVERSE_1.png',
									'DRUMMER_Cymbal_LEFT_STILL.png'],

									['DRUMMER_Cymbal_RIGHT_STILL.png',
									'DRUMMER_Cymbal_RIGHT_HIT_1.png',
									'DRUMMER_Cymbal_RIGHT_HIT_2.png',
									'DRUMMER_Cymbal_RIGHT_HIT_1.png',
									'DRUMMER_Cymbal_RIGHT_STILL.png',
									'DRUMMER_Cymbal_RIGHT_HIT_REVERSE_1.png',
									'DRUMMER_Cymbal_RIGHT_HIT_REVERSE_2.png',
									'DRUMMER_Cymbal_RIGHT_HIT_REVERSE_1.png',
									'DRUMMER_Cymbal_RIGHT_STILL.png']
									]
