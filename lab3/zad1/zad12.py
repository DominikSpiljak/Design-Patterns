import os
from importlib import import_module

def test():
	pets=[]
	# obiđi svaku datoteku kazala plugins 
	for mymodule in os.listdir('plugins'):
		moduleName, moduleExt = os.path.splitext(mymodule)
		# ako se radi o datoteci s Pythonskim kodom ...
		if moduleExt=='.py':
			# instanciraj ljubimca ...
			ljubimac=myfactory(moduleName)('Ljubimac '+str(len(pets)))
			# ... i dodaj ga u listu ljubimaca
			pets.append(ljubimac)

	# ispiši ljubimce
	for pet in pets:
		printGreeting(pet)
		printMenu(pet)

def myfactory(moduleName):
	module = import_module('plugins.{}'.format(moduleName))
	init = getattr(module, moduleName)
	return init

def printGreeting(pet):
	print('{} pozdravlja: {}'.format(pet.name(), pet.greet()))

def printMenu(pet):
	print('{} voli {}'.format(pet.name(), pet.menu()))

if __name__ == "__main__":
    test()
