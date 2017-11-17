import pygame

class SpriteManager(object):

	sheets = [];
	
	@staticmethod 
	def getSpriteById(manager, id):
	
		for x in range(0, len(manager["definitions"])):
			item = manager["definitions"][x]
			
			if int(item["id"]) == int(id):
				return item

	@staticmethod
	def loadDefinition(name, file, definitions):
		image = pygame.image.load(file)
		
		sheet_definition = {}
		
		sheet_definition["image"] = image
		sheet_definition["name"] = name
		sheet_definition["definitions"] = definitions
						
		SpriteManager.sheets.append(sheet_definition)
		
	@staticmethod
	def getSheet(name):
		for x in range(0, len(SpriteManager.sheets)):
			man = SpriteManager.sheets[x]
			
			if man["name"] == name:
				return man
	
		
	