import pygame

from scenes import gamescene
import spritemanager

def RunGame(width, height, fps, scene):
	pygame.init()
	
	screen = pygame.display.set_mode((width, height))
	clock = pygame.time.Clock()
	
	current_scene = scene
	
	# Load resources
	spritemanager.SpriteManager.loadDefinition('player', 'resources/images/player.png', [
		{"id": "1", "x": "0", "y": "0", "width": "24", "height": "26"},
		{"id": "2", "x": "24", "y": "0", "width": "24", "height": "26"},
		{"id": "3", "x": "48", "y": "0", "width": "24", "height": "26"},
		{"id": "4", "x": "74", "y": "0", "width": "24", "height": "26"},
		
		{"id": "5", "x": "0", "y": "26", "width": "24", "height": "26"},
		{"id": "6", "x": "24", "y": "26", "width": "24", "height": "26"},
		{"id": "7", "x": "48", "y": "26", "width": "24", "height": "26"},
		{"id": "8", "x": "74", "y": "26", "width": "24", "height": "26"},
		
		{"id": "9", "x": "0", "y": "52", "width": "24", "height": "26"},
		{"id": "10", "x": "24", "y": "52", "width": "24", "height": "26"},
		{"id": "11", "x": "48", "y": "52", "width": "24", "height": "26"},
		{"id": "12", "x": "74", "y": "52", "width": "24", "height": "26"},
		
		{"id": "13", "x": "0", "y": "78", "width": "24", "height": "26"},
		{"id": "14", "x": "24", "y": "78", "width": "24", "height": "26"},
		{"id": "15", "x": "48", "y": "78", "width": "24", "height": "26"},
		{"id": "16", "x": "74", "y": "78", "width": "24", "height": "26"},
	])
	
	spritemanager.SpriteManager.loadDefinition('world', 'resources/images/world.png', [
	{"id": "1", "x": "0", "y": "0", "width": "50", "height": "50"}, 
	{"id": "2", "x": "50", "y": "0", "width": "50", "height": "50"}
	])
	
	while current_scene != None:
	
		# Engine update procedure
		input_keys = pygame.key.get_pressed()		
		
		current_scene.Update()
		
		# Engine draw procedure
		screen.fill((0,0,0))
		current_scene.Draw(screen, spritemanager.SpriteManager)			
		pygame.display.flip()
		
		# Running through
		clock.tick(fps)

		
RunGame(860, 640, 60, gamescene.GameScene())		