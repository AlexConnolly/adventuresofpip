import pygame
import spritemanager

class GameScene(object):

	currentRoom = None
	rooms = []
	
	xLocation = 150
	yLocation = 100
	
	playerDirection = 1
	playerAnimationState = 1
	playerMoveSpeed = 2
	someMovementKeyPressed = False
	
	playerIsGhostActive = False
	playerGhostValue = 100

	hasEverAnimated = False
	
	isDebugMode = False
	
	showMessages = True
	
	messages = []
	
	interfaceFont = {}
	
	triggersAlreadyTriggered = []
	
	roomToLoad = None
	
	hasKey = False
	doorsUnlocked = False
	
	def NextMessage(self):
		if self.showMessages == False:
			return
			
		if len(self.messages) == 0:
			self.ShowMessages = False
			return
		
		self.messages.pop(0)
	
	def __init__(self):
	
		self.interfaceFont = pygame.font.SysFont('Comic Sans MS', 14)
	
		self.currentRoom = self.LoadScene(0)
		
		# startup messages
		
		self.messages.append({
			"title": "Huh... how did I end up here?",
			"body": "Not this again... Why does this always happen?"
		})
		
		self.messages.append({
			"title": "Well, I guess I better find what is going on",
			"body": "I can probably use my connection with the other side (E)..."
		});
		
		self.messages.append({
			"title": "To pass through this wall.",
			"body": "Let's see..."
		});
		
	def ResetRoom(self):
		self.hasKey = False
		self.doorsUnlocked = False

	def Update(self):	
		
		self.someMovementKeyPressed = False
	
		if self.roomToLoad is not None:
			self.currentRoom = self.roomToLoad
			self.roomToLoad = None
			self.ResetRoom()
		
		if "bots" in self.currentRoom:			
			for x in range(0, len(self.currentRoom["bots"])):			
			
				bot = self.currentRoom["bots"][x]
				print(bot["current_waypoint"])
				
				if "x" in bot:
					pass
				else:
					bot["x"] = bot["waypoints"][bot["current_waypoint"]]["x"]
					
				if "y" in bot:
					pass
				else:
					bot["y"] = bot["waypoints"][bot["current_waypoint"]]["y"]
				
				current_waypoint = bot["waypoints"][bot["current_waypoint"]]
				
				distance_x = abs(int(bot["x"]) - int(current_waypoint["x"]))
				distance_y = abs(int(bot["y"]) - int(current_waypoint["y"]))
				
				print(distance_y)
				print(distance_x)
				
				if (distance_x < (int(bot["speed"]) * 2)) and (distance_y < (int(bot["speed"]) * 2)):
					# we can move to next 
					
					if (len(bot["waypoints"]) - 1) == bot["current_waypoint"]:
						# last waypoint
						if "should_reverse" in bot:
							if bot["should_reverse"] == True:							
								bot["reversing"] = True
								bot["current_waypoint"] -= 1
							else:
								bot["current_waypoint"] = 0
						else:
							bot["reversing"] = True
							bot["current_waypoint"] -= 1
					else:
						if "reversing" in bot:
							if bot["reversing"] == True:
								bot["current_waypoint"] -= 1
							else:
								bot["current_waypoint"] += 1
						else:
							bot["current_waypoint"] += 1
						
					# fix just incase
					if bot["current_waypoint"] == -1:
						bot["current_waypoint"] = 1		
						bot["reversing"] = False
				else:					
					# only move if need to
					if (distance_x > (int(bot["speed"]) * 2)):
					
						moveX = int(bot["speed"])
					
						if(int(bot["x"]) > int(current_waypoint["x"])):
							moveX = moveX * -1
							
						bot["x"] += moveX
					
					else:
						bot["x"] = int(current_waypoint["x"])
						
					if (distance_y > (int(bot["speed"]) * 2)):					
					
						moveY = int(bot["speed"])
					
						if(int(bot["y"]) > int(current_waypoint["y"])):
							moveY = moveY * -1
							
						bot["y"] += moveY
					else:
						bot["y"] = int(current_waypoint["y"])
				
								
							
		# Calculate current colliders		
		worldSheet = spritemanager.SpriteManager.getSheet("world")
		
		self.currentRoom["colliders"] = []
		
		for x in range(0, len(self.currentRoom["objects"])):
			currentObject = self.currentRoom["objects"][x]			
			
			sprite = spritemanager.SpriteManager.getSpriteById(worldSheet, currentObject["id"])
			
			if sprite["passable"] == True:
				continue
				
			if ((currentObject["id"] == "6") and (self.doorsUnlocked == True)):
				continue	
				
			self.currentRoom["colliders"].append({"x": int(currentObject["x"]), "y": int(currentObject["y"]), "width": int(sprite["width"]), "height": int(sprite["height"]), "traversable": sprite["traversable"]})
	
		# Ghost update		
		if self.playerIsGhostActive == True:
			self.playerGhostValue -= 1
			
			if self.playerGhostValue <= 0:
				self.playerIsGhostActive = False
				
		if self.playerIsGhostActive == False:			
			if self.playerGhostValue < 100:
				self.playerGhostValue += 1				
	
			
		for event in pygame.event.get():
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.NextMessage()
					
		# Exit out as we get to movement
		if self.showMessages == True:
			return
	
		# Really lazy player update but guess what thats how life is
		destinedX = self.xLocation
		destinedY = self.yLocation
		
		keys = pygame.key.get_pressed()
		
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

		if keys[pygame.K_e]:
			if self.playerIsGhostActive == False and self.playerGhostValue == 100:
				self.playerIsGhostActive = True

				
		# Make sure theres no interraction with the world
		# The idea here is to test each one and say "hey does this fit" with the old co-ordinate and then move it if it is ok
		if not self.DoesCollideWithWorld(destinedX, self.yLocation):
			self.xLocation = destinedX
			
		if not self.DoesCollideWithWorld(self.xLocation, destinedY):
			self.yLocation = destinedY
			
		# Check if we collided with a trigger
		self.TriggerCollisionCheck()
		
	def TriggerHasAlreadyTriggered(self, trigger):
		for x in range(0, len(self.triggersAlreadyTriggered)):
			if self.triggersAlreadyTriggered[x]["id"] == trigger["id"]:
				return True
		return False
	
	# Checks if any triggers are triggered
	def TriggerCollisionCheck(self):
	
		if len(self.currentRoom["triggers"]) == 0:
			return
	
		for x in range(0, len(self.currentRoom["triggers"])):
			if self.DoesTriggerCollide(self.xLocation, self.yLocation, self.currentRoom["triggers"][x]):
				if not self.TriggerHasAlreadyTriggered(self.currentRoom["triggers"][x]):
					self.HandleTrigger(self.currentRoom["triggers"][x])		
					self.triggersAlreadyTriggered.append(self.currentRoom["triggers"][x])
			else:
				if self.TriggerHasAlreadyTriggered(self.currentRoom["triggers"][x]):
					# it has already triggered but wasnt this time, remove it
					self.triggersAlreadyTriggered.remove(self.currentRoom["triggers"][x])
					print("leave trigger")
				
	def HandleTrigger(self, trigger):
	
		print(trigger["id"])
		
		if trigger["id"] == "exit_cage_trigger":
			self.messages.append({
				"title": "Well, that wasn't difficult",
				"body": "Maybe I should head up these stairs and see what's going on?"
			})
			
			self.showMessages = True
			
		if trigger["id"] == "stair_trigger":
			self.roomToLoad = self.LoadScene(1)			

		if trigger["id"] == "attempt_down_stairs":
			self.messages.append({
				"title": "I don't want to go back down there!",
				"body": "Escaping doesn't involve going back on yourself..."
			})
			
			self.showMessages = True
			
		if trigger["id"] == "key_required":
		
			if self.doorsUnlocked == False:			
				if self.hasKey == True:
					self.doorsUnlocked = True
					self.hasKey = False
					
					self.messages.append({
						"title": "*Clink* ... and it's gone",
						"body": "Let's see what's up next!"
					})
				else:		
					self.messages.append({
						"title": "Hmm... This door looks like it's too dense to walk through",
						"body": "Maybe I could look around for a key..."
					})
				
				self.showMessages = True
					
		if trigger["id"] == "key_in_sight":
		
			if self.hasKey == False:
				self.messages.append({
					"title": "There! I can see a key!",
					"body": "I could probably use that, but I probably shouldn't be seen by these guys..."
				})
				
				self.showMessages = True			
		
					
		if trigger["id"] == "key_found":		
		
			if self.hasKey == False:		
				self.messages.append({
					"title": "Got it!",
					"body": "Now let's go see if it works!"
				})			
				self.hasKey = True
				
				self.showMessages = True
	
	def LoadScene(self, index):
		
		self.triggersAlreadyTriggered = []
		
		if index == 1:
		
			self.xLocation = 70
			self.yLocation = 180
			self.playerDirection = 1
			
			curRoom = {}
			
			curRoom["light"] = 0
			
			curRoom["color"] = (57, 72, 81)
			
			curRoom["triggers"] = [
				{
					"x": "10",
					"y": "235",
					"width": "100",
					"height": "25",
					"id": "attempt_down_stairs"
				},
				{
					"x": "160", 
					"y": "60",
					"width": "50",
					"height": "50",
					"id": "key_required",
					"is_checkpoint": True
				},
				{
					"id": "key_in_sight", 
					"x": "260", 
					"y": "410",
					"height": "50",
					"width": "50",
					"is_checkpoint": True
				},				
				{
					"id": "key_found", 
					"x": "660", 
					"y": "160",
					"height": "50",
					"width": "50",
					"is_checkpoint": True,
					"is_one_time": True
				},
			]
			
			curRoom["bots"] = [
				{
					"id": 1,
					"waypoints": [
						{"x": 375, "y": 160},
						{"x": 375, "y": 410}	
					],
					"speed": 1,
					"visibility": 70,
					"current_waypoint": 0
				},
				{
					"id": 1,
					"waypoints": [
						{"x": 475, "y": 160},
						{"x": 575, "y": 160},	
						{"x": 575, "y": 420},
						{"x": 475, "y": 420}						
					],
					"speed": 1,
					"visibility": 70,
					"current_waypoint": 0,
					"should_reverse": False
				}
			]
			
			curRoom["objects"] = [					
				
				# - floor				
				{"id": "2", "x": "210", "y": "60"}, 
				{"id": "2", "x": "260", "y": "60"}, 
				{"id": "2", "x": "310", "y": "60"}, 
				
				{"id": "2", "x": "260", "y": "10"}, 
				{"id": "2", "x": "260", "y": "-40"}, 
				{"id": "2", "x": "310", "y": "10"}, 
				{"id": "2", "x": "310", "y": "-40"}, 
				
				{"id": "2", "x": "10", "y": "60"}, 
				{"id": "2", "x": "60", "y": "60"}, 
				{"id": "2", "x": "110", "y": "60"}, 
				{"id": "2", "x": "160", "y": "60"}, 				
				
				{"id": "2", "x": "10", "y": "110"}, 
				{"id": "2", "x": "60", "y": "110"}, 
				{"id": "2", "x": "110", "y": "110"}, 
				{"id": "2", "x": "160", "y": "110"}, 
				
				{"id": "2", "x": "10", "y": "160"}, 
				{"id": "2", "x": "60", "y": "160"}, 
				{"id": "2", "x": "110", "y": "160"}, 
				{"id": "2", "x": "160", "y": "160"}, 
				
				{"id": "2", "x": "10", "y": "210"}, 
				{"id": "2", "x": "60", "y": "210"}, 
				{"id": "2", "x": "110", "y": "210"}, 
				{"id": "2", "x": "160", "y": "210"}, 
				
				{"id": "2", "x": "160", "y": "260"}, 
				{"id": "2", "x": "160", "y": "310"}, 
				{"id": "2", "x": "160", "y": "360"}, 
				{"id": "2", "x": "160", "y": "410"}, 
				
				{"id": "2", "x": "210", "y": "410"}, 
				{"id": "2", "x": "260", "y": "410"}, 
				{"id": "2", "x": "310", "y": "410"}, 
				{"id": "2", "x": "360", "y": "410"}, 
				{"id": "2", "x": "410", "y": "410"}, 
				{"id": "2", "x": "460", "y": "410"}, 
				{"id": "2", "x": "510", "y": "410"}, 
				{"id": "2", "x": "560", "y": "410"}, 
				{"id": "2", "x": "610", "y": "410"}, 
				{"id": "2", "x": "660", "y": "410"}, 				
				
				{"id": "2", "x": "210", "y": "360"}, 
				{"id": "2", "x": "260", "y": "360"}, 
				{"id": "2", "x": "310", "y": "360"}, 
				{"id": "2", "x": "360", "y": "360"}, 
				{"id": "2", "x": "410", "y": "360"}, 
				{"id": "2", "x": "460", "y": "360"}, 
				{"id": "2", "x": "510", "y": "360"}, 
				{"id": "2", "x": "560", "y": "360"}, 
				{"id": "2", "x": "610", "y": "360"}, 
				{"id": "2", "x": "660", "y": "360"}, 
				
				{"id": "2", "x": "210", "y": "310"}, 
				{"id": "2", "x": "260", "y": "310"}, 
				{"id": "2", "x": "310", "y": "310"}, 
				{"id": "2", "x": "360", "y": "310"}, 
				{"id": "2", "x": "410", "y": "310"}, 
				{"id": "2", "x": "460", "y": "310"}, 
				{"id": "2", "x": "510", "y": "310"}, 
				{"id": "2", "x": "560", "y": "310"}, 
				{"id": "2", "x": "610", "y": "310"}, 
				{"id": "2", "x": "660", "y": "310"}, 				
				
				{"id": "2", "x": "210", "y": "260"}, 
				{"id": "2", "x": "260", "y": "260"}, 
				{"id": "2", "x": "310", "y": "260"}, 
				{"id": "2", "x": "360", "y": "260"}, 
				{"id": "2", "x": "410", "y": "260"}, 
				{"id": "2", "x": "460", "y": "260"}, 
				{"id": "2", "x": "510", "y": "260"}, 
				{"id": "2", "x": "560", "y": "260"}, 
				{"id": "2", "x": "610", "y": "260"}, 
				{"id": "2", "x": "660", "y": "260"}, 				
				
				{"id": "2", "x": "210", "y": "210"}, 
				{"id": "2", "x": "260", "y": "210"}, 
				{"id": "2", "x": "310", "y": "210"}, 
				{"id": "2", "x": "360", "y": "210"}, 
				{"id": "2", "x": "410", "y": "210"}, 
				{"id": "2", "x": "460", "y": "210"}, 
				{"id": "2", "x": "510", "y": "210"}, 
				{"id": "2", "x": "560", "y": "210"}, 
				{"id": "2", "x": "610", "y": "210"}, 
				{"id": "2", "x": "660", "y": "210"}, 				
				
				{"id": "2", "x": "210", "y": "160"}, 
				{"id": "2", "x": "260", "y": "160"}, 
				{"id": "2", "x": "310", "y": "160"}, 
				{"id": "2", "x": "360", "y": "160"}, 
				{"id": "2", "x": "410", "y": "160"}, 
				{"id": "2", "x": "460", "y": "160"}, 
				{"id": "2", "x": "510", "y": "160"}, 
				{"id": "2", "x": "560", "y": "160"}, 
				{"id": "2", "x": "610", "y": "160"}, 
				{"id": "2", "x": "660", "y": "160"}, 
				
				# - left wall
				{"id": "1", "x": "-40", "y": "10"}, 
				{"id": "1", "x": "-40", "y": "60"}, 
				{"id": "1", "x": "-40", "y": "110"}, 
				{"id": "1", "x": "-40", "y": "160"}, 
				{"id": "1", "x": "-40", "y": "210"}, 
				{"id": "1", "x": "-40", "y": "260"}, 
				
				# - top wall
				{"id": "1", "x": "10", "y": "10"}, 
				{"id": "1", "x": "60", "y": "10"}, 
				{"id": "1", "x": "110", "y": "10"}, 
				{"id": "1", "x": "160", "y": "10"}, 
				
				# - bottom wall
				{"id": "1", "x": "10", "y": "260"}, 
				{"id": "1", "x": "60", "y": "260"}, 
				{"id": "1", "x": "110", "y": "260"}, 
				
				# - right wall
				{"id": "1", "x": "110", "y": "110"}, 
				{"id": "1", "x": "110", "y": "160"}, 
				{"id": "1", "x": "110", "y": "210"}, 				
				{"id": "1", "x": "110", "y": "260"}, 		
				{"id": "1", "x": "110", "y": "310"}, 	
				{"id": "1", "x": "110", "y": "360"}, 
				{"id": "1", "x": "110", "y": "410"}, 
				{"id": "1", "x": "110", "y": "460"}, 

				# bottom LONG wall
				{"id": "1", "x": "160", "y": "460"}, 
				{"id": "1", "x": "210", "y": "460"}, 
				{"id": "1", "x": "260", "y": "460"}, 
				{"id": "1", "x": "310", "y": "460"}, 
				{"id": "1", "x": "360", "y": "460"}, 
				{"id": "1", "x": "410", "y": "460"}, 
				{"id": "1", "x": "460", "y": "460"}, 
				{"id": "1", "x": "510", "y": "460"}, 
				{"id": "1", "x": "560", "y": "460"}, 
				{"id": "1", "x": "610", "y": "460"}, 
				{"id": "1", "x": "660", "y": "460"}, 
				{"id": "1", "x": "710", "y": "460"},
				
				
				# right right wall
				{"id": "1", "x": "710", "y": "160"},
				{"id": "1", "x": "710", "y": "210"},
				{"id": "1", "x": "710", "y": "260"},
				{"id": "1", "x": "710", "y": "310"},
				{"id": "1", "x": "710", "y": "360"},
				{"id": "1", "x": "710", "y": "410"},
					
					
				# right higher wall
				{"id": "1", "x": "260", "y": "110"},
				{"id": "1", "x": "310", "y": "110"},
				{"id": "1", "x": "360", "y": "110"},
				{"id": "1", "x": "410", "y": "110"},
				{"id": "1", "x": "460", "y": "110"},
				{"id": "1", "x": "510", "y": "110"},
				{"id": "1", "x": "560", "y": "110"},
				{"id": "1", "x": "610", "y": "110"},
				{"id": "1", "x": "660", "y": "110"},
				{"id": "1", "x": "710", "y": "110"},
					
				# floating wall	
				{"id": "1", "x": "210", "y": "110"},
				{"id": "1", "x": "210", "y": "160"},
				{"id": "1", "x": "210", "y": "210"}, 			
				{"id": "1", "x": "210", "y": "260"}, 		
				{"id": "1", "x": "210", "y": "310"}, 		
				{"id": "1", "x": "210", "y": "360"}, 
				
				# destination stair room
				{"id": "1", "x": "210", "y": "10"},
				{"id": "1", "x": "210", "y": "-40"},
				{"id": "1", "x": "210", "y": "-90"},
				{"id": "1", "x": "210", "y": "-140"},
				{"id": "1", "x": "260", "y": "-140"},
				{"id": "1", "x": "310", "y": "-140"},
				{"id": "1", "x": "360", "y": "-140"},
				{"id": "1", "x": "360", "y": "-90"},
				{"id": "1", "x": "360", "y": "-40"},
				{"id": "1", "x": "360", "y": "10"},
				{"id": "1", "x": "360", "y": "60"},
				{"id": "1", "x": "360", "y": "110"},
				
				# Cases		

				#1
				{"id": "7", "x": "310", "y": "210"},
				{"id": "7", "x": "310", "y": "260"},
				{"id": "7", "x": "310", "y": "310"},
				{"id": "7", "x": "310", "y": "360"},
				
				#2 
				{"id": "7", "x": "410", "y": "160"},
				{"id": "7", "x": "410", "y": "210"},
				{"id": "7", "x": "410", "y": "260"},
				{"id": "7", "x": "410", "y": "360"},
				{"id": "7", "x": "410", "y": "410"},
								
				#3
				{"id": "7", "x": "510", "y": "210"},
				{"id": "7", "x": "510", "y": "260"},
				{"id": "7", "x": "510", "y": "310"},
				{"id": "7", "x": "510", "y": "360"},				
				
				#4
				{"id": "7", "x": "610", "y": "160"},
				{"id": "7", "x": "610", "y": "210"},
				{"id": "7", "x": "610", "y": "260"},
				{"id": "7", "x": "610", "y": "360"},
				{"id": "7", "x": "610", "y": "410"},
				
				# key
				{"id": "8", "x": "675", "y": "175"},
				
				
				# door 				
				{"id": "6", "x": "210", "y": "60"},
								
				# - stair				
				{"id": "5", "x": "10", "y": "160"}, 	
				
				# - up stair
				{"id": "5", "x": "260", "y": "-90"},		
				
			]
			
			return curRoom
								
		if index == 0:
		
			curRoom = {}
			
			curRoom["light"] = 150
			curRoom["color"] = (0, 0, 0)
				
			# register the triggers
			curRoom["triggers"] = [
				{
					"x": "310",
					"y": "60",
					"width": "100",
					"height": "25",
					"id": "stair_trigger"
				},
				{
					"x": "260",
					"y": "160",
					"width": "50",
					"height": "100",
					"id": "exit_cage_trigger"
				}
			]
			
			# startup objects...
			curRoom["objects"] = [		
				
				
				# floor
				
				{"id": "2", "x": "10", "y": "60"}, 
				{"id": "2", "x": "60", "y": "60"}, 
				{"id": "2", "x": "110", "y": "60"}, 
				{"id": "2", "x": "160", "y": "60"}, 
				{"id": "2", "x": "210", "y": "60"}, 
				{"id": "2", "x": "260", "y": "60"}, 
				{"id": "2", "x": "310", "y": "60"}, 
				{"id": "2", "x": "360", "y": "60"}, 
				
				
				{"id": "2", "x": "10", "y": "110"}, 
				{"id": "2", "x": "60", "y": "110"}, 
				{"id": "2", "x": "110", "y": "110"}, 
				{"id": "2", "x": "160", "y": "110"}, 
				{"id": "2", "x": "210", "y": "110"}, 
				{"id": "2", "x": "260", "y": "110"}, 
				{"id": "2", "x": "310", "y": "110"}, 
				{"id": "2", "x": "360", "y": "110"}, 			
				
				{"id": "2", "x": "10", "y": "160"}, 
				{"id": "2", "x": "60", "y": "160"}, 
				{"id": "2", "x": "110", "y": "160"}, 
				{"id": "2", "x": "160", "y": "160"}, 
				{"id": "2", "x": "210", "y": "160"}, 
				{"id": "2", "x": "260", "y": "160"}, 
				{"id": "2", "x": "310", "y": "160"}, 
				{"id": "2", "x": "360", "y": "160"}, 
						

				{"id": "2", "x": "10", "y": "210"}, 
				{"id": "2", "x": "60", "y": "210"}, 
				{"id": "2", "x": "110", "y": "210"}, 
				{"id": "2", "x": "160", "y": "210"}, 
				{"id": "2", "x": "210", "y": "210"}, 
				{"id": "2", "x": "260", "y": "210"}, 
				{"id": "2", "x": "310", "y": "210"}, 
				{"id": "2", "x": "360", "y": "210"}, 
			
				# left wall
				{"id": "1", "x": "-40", "y": "10"}, 
				{"id": "1", "x": "-40", "y": "60"}, 
				{"id": "1", "x": "-40", "y": "110"}, 
				{"id": "1", "x": "-40", "y": "160"}, 
				{"id": "1", "x": "-40", "y": "210"}, 
				{"id": "1", "x": "-40", "y": "260"}, 
				
				# top wall
				{"id": "1", "x": "10", "y": "10"}, 
				{"id": "1", "x": "60", "y": "10"}, 
				{"id": "1", "x": "110", "y": "10"}, 
				{"id": "1", "x": "160", "y": "10"}, 
				{"id": "1", "x": "210", "y": "10"}, 
				{"id": "1", "x": "260", "y": "10"}, 
				{"id": "1", "x": "310", "y": "10"}, 
				{"id": "1", "x": "360", "y": "10"}, 
				{"id": "1", "x": "410", "y": "10"}, 
				
				# bottom wall
				{"id": "1", "x": "10", "y": "260"}, 
				{"id": "1", "x": "60", "y": "260"}, 
				{"id": "1", "x": "110", "y": "260"}, 
				{"id": "1", "x": "160", "y": "260"}, 
				{"id": "1", "x": "210", "y": "260"}, 
				{"id": "1", "x": "260", "y": "260"}, 
				{"id": "1", "x": "310", "y": "260"}, 
				{"id": "1", "x": "360", "y": "260"}, 
				{"id": "1", "x": "410", "y": "260"}, 
				
				# stair wall
				{"id": "1", "x": "260", "y": "60"}, 
				{"id": "1", "x": "260", "y": "110"}, 
				
				
				
				# right wall
				{"id": "1", "x": "410", "y": "60"}, 
				{"id": "1", "x": "410", "y": "110"}, 
				{"id": "1", "x": "410", "y": "160"}, 
				{"id": "1", "x": "410", "y": "210"}, 
				{"id": "1", "x": "410", "y": "260"}, 
				
				# cell
				
				# - cell walls
				{"id": "3", "x": "60", "y": "60"}, 
				{"id": "3", "x": "60", "y": "90"}, 
				{"id": "3", "x": "60", "y": "120"}, 			
				
				{"id": "3", "x": "210", "y": "60"}, 
				{"id": "3", "x": "210", "y": "90"}, 
				{"id": "3", "x": "210", "y": "120"}, 
				
				# - cell cage
				{"id": "4", "x": "90", "y": "120"}, 
				{"id": "4", "x": "120", "y": "120"}, 
				{"id": "4", "x": "150", "y": "120"}, 
				{"id": "4", "x": "180", "y": "120"}, 
				
				# objects
				
				# staircase
				{"id": "5", "x": "310", "y": "60"}, 
				
			]
			
			return curRoom
		
		
			
	def DoesTriggerCollide(self, xLoc, yLoc, collider):	
		colliderX = int(collider["x"])
		colliderY = int(collider["y"])		
								
		xTCollides = (((xLoc + 12) >= colliderX)) and ((xLoc + 12 <= colliderX + int(collider["width"])))
		xLCollides = (((xLoc - 12) >= colliderX)) and ((xLoc - 12 <= colliderX + int(collider["width"])))
								
		yTCollides = (((yLoc + 13) >= colliderY)) and ((yLoc + 13 <= colliderY + int(collider["height"])))
		yLCollides = (((yLoc - 13) >= colliderY)) and ((yLoc - 13 <= colliderY + int(collider["height"])))
									
		if ((xTCollides == True) or (xLCollides == True)) and ((yTCollides == True) or (yLCollides == True)):
			return True
		else:
			return False
		
	
	# This calculation is flawed since it doesnt use the draw offset (+ width of screen etc for centering)
	def DoesCollideWithWorld(self, xLoc, yLoc):
		
		for x in range(0, len(self.currentRoom["colliders"])):
				
			collider = self.currentRoom["colliders"][x]
			
			if (collider["traversable"] == True) and self.playerIsGhostActive:
				continue
			
			colliderX = int(collider["x"])
			colliderY = int(collider["y"])		
									
			xTCollides = (((xLoc + 12) >= colliderX)) and ((xLoc + 12 <= colliderX + int(collider["width"])))
			xLCollides = (((xLoc - 12) >= colliderX)) and ((xLoc - 12 <= colliderX + int(collider["width"])))
									
			yTCollides = (((yLoc + 13) >= colliderY)) and ((yLoc + 13 <= colliderY + int(collider["height"])))
			yLCollides = (((yLoc - 13) >= colliderY)) and ((yLoc - 13 <= colliderY + int(collider["height"])))
							
			if ((xTCollides == True) or (xLCollides == True)) and ((yTCollides == True) or (yLCollides == True)):
				return True
				
		return False	
	
	def Draw(self, screen, sprite_manager):
			
		screen.fill(self.currentRoom["color"])
	
		worldSheet = sprite_manager.getSheet("world")
	
		# Draw scene		
		for x in range(0, len(self.currentRoom["objects"])):
		
			currentObject = self.currentRoom["objects"][x]		
			
			# dont show key if we have key
			if ((currentObject["id"] == "8") and (self.hasKey == True)) or ((currentObject["id"] == "6") and (self.doorsUnlocked == True)):
				continue
			
			toDraw = sprite_manager.getSpriteById(worldSheet, currentObject["id"])		
			
			xDraw = (int(currentObject["x"]) - self.xLocation) + 430 # world x offset
			yDraw = (int(currentObject["y"]) - self.yLocation) + 320 # world y offset
			
			if (toDraw["traversable"] == True) and (self.playerIsGhostActive == True):
				worldSheet["image"].set_alpha(50)
			else:
				worldSheet["image"].set_alpha(255)
						
			screen.blit(worldSheet["image"], (xDraw, yDraw), (int(toDraw["x"]), int(toDraw["y"]), int(toDraw["width"]), int(toDraw["height"])))

	
		for x in range(0, len(self.currentRoom["colliders"])):
			collider = self.currentRoom["colliders"][x]
			
			if self.isDebugMode:
				pygame.draw.rect(screen, (0, 255, 0), (int(collider["x"]) + 430 - self.xLocation, int(collider["y"]) + 320 - self.yLocation, int(collider["width"]), int(collider["height"])), 1)
				
		for x in range(0, len(self.currentRoom["triggers"])):
			trigger = self.currentRoom["triggers"][x]
			
			if self.isDebugMode: 
				pygame.draw.rect(screen, (255, 0, 0), (int(trigger["x"]) + 430 - self.xLocation, int(trigger["y"]) + 320 - self.yLocation, int(trigger["width"]), int(trigger["height"])), 1)

		if self.someMovementKeyPressed:
			if self.playerAnimationState == 4:
				self.playerAnimationState = 1
			else:
				self.playerAnimationState += 1	

		# Draw bots
		if "bots" in self.currentRoom:
			botSheet = sprite_manager.getSheet("bot")
			
			for x in range(0, len(self.currentRoom["bots"])):
				bot = self.currentRoom["bots"][x]
				
				# Calculate facing direction
				bot["facingDirection"] = 1
				bot["animationState"] = 1
				
				if "x" not in bot:
					bot["x"] = bot["waypoints"][0]["x"]
					
				if "y" not in bot:
					bot["y"] = bot["waypoints"][0]["y"]
				
				# Calculate animation state				
				relativeX = int(bot["x"]) + 430 - self.xLocation
				relativeY = int(bot["y"]) + 320 - self.yLocation
				
				botSheetIndex = ((int(bot["facingDirection"]) - 1) * 4) + int(bot["animationState"])
				
				toDraw = sprite_manager.getSpriteById(botSheet, botSheetIndex)
				
				screen.blit(botSheet["image"], (relativeX, relativeY), (int(toDraw["x"]), int(toDraw["y"]), int(toDraw["width"]), int(toDraw["height"])))
				
				for y in range(0, len(bot["waypoints"])):
					waypoint = bot["waypoints"][y]
					
					if y is not 0:
						otherPoint = bot["waypoints"][y - 1]						
						pygame.draw.line(screen, (255, 131, 0), ((int(otherPoint["x"]) + 430 - self.xLocation + 25), int(otherPoint["y"]) + 320 - self.yLocation), (int(waypoint["x"]) + 430 - self.xLocation + 25, int(waypoint["y"]) + 320 - self.yLocation))
				
	
				
		# Draw Player
		playerSheet = sprite_manager.getSheet("player")
		
		playerSheetIndex = ((self.playerDirection - 1) * 4) + self.playerAnimationState
		
		toDraw = sprite_manager.getSpriteById(playerSheet, playerSheetIndex)	
		
		playerXPos = (860 / 2) - 12
		playerYPos = (640 / 2) - 13
						
		if self.playerIsGhostActive == True:
			playerSheet["image"].set_alpha(50)
		else:
			playerSheet["image"].set_alpha(255)
		
		screen.blit(playerSheet["image"], (playerXPos, playerYPos), (int(toDraw["x"]), int(toDraw["y"]), int(toDraw["width"]), int(toDraw["height"])))
		
		# Draw dark layer
		darkSurface = pygame.Surface((860, 640))
		darkSurface.set_alpha(self.currentRoom["light"])
		darkSurface.fill((0, 0, 0))
		
		screen.blit(darkSurface, (0, 0))
		
		# Draw UI
		pygame.draw.rect(screen, (59, 135, 135), (860 - 162, 8, 154, 19))
		pygame.draw.rect(screen, (89, 206, 206), (860 - 160, 10, (150 / 100) * self.playerGhostValue, 15))

		# Draw any messages that need to be display
		if self.showMessages == True:		
		
			if len(self.messages) == 0:
				self.showMessages = False
			else:	
				# Box
				pygame.draw.rect(screen, (234, 234, 234), (430 - 290, 640 - 160, 580, 100))
				
				# Heading
				headingSurface = self.interfaceFont.render(self.messages[0]["title"], False, (0, 0, 0))
				screen.blit(headingSurface, (430 - 270, 640 - 140))
				
				# Body
				headingSurface = self.interfaceFont.render(self.messages[0]["body"], False, (0, 0, 0))
				screen.blit(headingSurface, (430 - 270, 640 - 100))