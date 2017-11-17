import pygame

class GameScene(object):

	currentRoom = None
	rooms = []
	
	xLocation = 0
	yLocation = 0
	
	playerDirection = 1
	playerAnimationState = 1
	playerMoveSpeed = 2
	someMovementKeyPressed = False

	hasEverAnimated = False
	
	def __init__(self):
		self.currentRoom = {}
		self.currentRoom["objects"] = [
			{"id": "1", "x": "-40", "y": "10"}, 
			{"id": "1", "x": "-40", "y": "60"}, 
			{"id": "1", "x": "10", "y": "10"}, 
			{"id": "1", "x": "60", "y": "10"}, 
			{"id": "2", "x": "10", "y": "60"}, 
			{"id": "2", "x": "60", "y": "60"}
		]

	def Update(self):
	
		# Really lazy player update but guess what thats how life is
		destinedX = self.xLocation
		destinedY = self.yLocation
		
		for event in pygame.event.get():
			pass
		
		keys = pygame.key.get_pressed()
		
		self.someMovementKeyPressed = False
		
		# Player key input
		if keys[pygame.K_a]:
			destinedX -= self.playerMoveSpeed
			self.playerDirection = 4
			self.someMovementKeyPressed = True
			
		if keys[pygame.K_w]:
			destinedY -= self.playerMoveSpeed
			self.playerDirection = 2
			self.someMovementKeyPressed = True
			
		if keys[pygame.K_d]:
			destinedX += self.playerMoveSpeed
			self.playerDirection = 3
			self.someMovementKeyPressed = True
			
		if keys[pygame.K_s]:
			destinedY += self.playerMoveSpeed
			self.playerDirection = 1	
			self.someMovementKeyPressed = True			
				
		# Make sure theres no interraction with the world
		if not self.DoesXIntersectWithWorld(destinedX):
			self.xLocation = destinedX
			
		if not self.DoesYIntersectWithWorld(destinedY):
			self.yLocation = destinedY

	def DoesXIntersectWithWorld(self, x):
		return False
		
	def DoesYIntersectWithWorld(self, y):
		return False	
	
	def Draw(self, screen, sprite_manager):
	
		worldSheet = sprite_manager.getSheet("world")
	
		# Draw scene
		for x in range(0, len(self.currentRoom["objects"])):
		
			currentObject = self.currentRoom["objects"][x]		
			
			toDraw = sprite_manager.getSpriteById(worldSheet, currentObject["id"])		
			
			xDraw = int(currentObject["x"]) - self.xLocation
			yDraw = int(currentObject["y"]) - self.yLocation
			
			screen.blit(worldSheet["image"], (xDraw, yDraw), (int(toDraw["x"]), int(toDraw["y"]), int(toDraw["x"]) + int(toDraw["width"]), int(toDraw["y"]) + int(toDraw["height"])))

				
		if self.someMovementKeyPressed:
			print("some key pressed")
			if self.playerAnimationState == 4:
				self.playerAnimationState = 1
			else:
				print("reached")
				self.playerAnimationState += 1
				self.hasEverAnimated = True
				
		
		playerSheet = sprite_manager.getSheet("player")
		
		playerSheetIndex = ((self.playerDirection - 1) * 4) + self.playerAnimationState
		
		toDraw = sprite_manager.getSpriteById(playerSheet, playerSheetIndex)	
		
		playerXPos = (860 / 2) - 12
		playerYPos = (640 / 2) - 13
		
		screen.blit(playerSheet["image"], (playerXPos, playerYPos), (int(toDraw["x"]), int(toDraw["y"]), int(toDraw["width"]), int(toDraw["height"])))
