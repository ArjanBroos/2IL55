"""
You are to reach the duck on other side.
"""
import cavelib3
import math
import viz
import vizshape
import caveapp #not strictly required
import vizact
import vizinfo
import vizproximity 
import viztask

#x = -left/+right
#y = -below/+above
#z = -behind/+in front

################################################################
#Placement of objects
################################################################

#object.method(x, y, z)

#object = viz.add("map/file.ext")							#Add object to scene
#object.setAxisAngle(0, 1, 0, 90)							#Set the direction of an object
#object.texture(viz.addTexture("textureMap/img.ext")) 		#Connect a texture to an object (.mtl file with the same name pastes the material over the object by itself)
#object.addAction(vizact.spin(0, 1, 0, 20))					#Arguments (x, y, z, speed), a negative number is used to spin in the opposite direction
#object.setScale(0.5, 0.5, 0.5)								#Scaling the object for each specific axis
#object.setPosition(0,2,0)									#Set the position of the object


################################################################
#Code, with respect to she functionality should be in here
################################################################




class CustomCaveApplication(caveapp.CaveApplication):

	def __init__(self,use_keyboard = True, desktop_mode = False):
		
		caveapp.CaveApplication.__init__(self,desktop_mode) #call constructor of super class, you have to do this explicitly in Python		
		
		self.wand = vizshape.addAxes() #load axis model to represent the wand (WALL FFS!)
		
		# Function for swinging the axes
		def swing(object, t, startAngle, endAngle):
			d = (math.sin(t[0]) + 1.0) / 2.0
			angle = startAngle + d * (endAngle - startAngle)
			object.setEuler([90,0,angle])
			t[0] += 0.03
		
		# Add axes
		nrAxes = 5
		axes = []
		axest = []
		for i in range(nrAxes):
			axes.append(viz.addChild('axe.OSGB', cache=viz.CACHE_CLONE))
			axes[i].setPosition([500*i,745,325], viz.REL_LOCAL)
			axes[i].setScale(225,225,325)
			axes[i].center(0,4.5,0)
			axest.append([float(i)])
			vizact.ontimer(0.03, swing, axes[i], axest[i], 120, 240)
		
		# Add ducky
		newduck = viz.addAvatar('duck.cfg')
		newduck.setScale([170,170,170])
		newduck.setPosition([3700,65,325],viz.REL_LOCAL)
		newduck.setEuler([-90,0,0])

		# Add proximity sensors
		manager = vizproximity.Manager()
		target = vizproximity.Target(viz.MainView)
		manager.addTarget(target)
		sensors = []
		for i in range(nrAxes):
			sensors.append(vizproximity.addBoundingBoxSensor(axes[i]))
			manager.addSensor(sensors[i])
		duckSensor = vizproximity.addBoundingBoxSensor(newduck,scale=(2.5,2.5,2.5))
		manager.addSensor(duckSensor)
		
		# Boolean variables to store trial results
		axesHit = []
		for i in range(nrAxes):
			axesHit.append(0)
		
		# Called when we enter a proximity
		def EnterProximity(e):
			for i in range(nrAxes):
				if e.sensor == sensors[i]:
					axesHit[i] += 1
					print "Hit axe #" + str(i) + " " + str(axesHit[i]) + " times!"
		
		manager.onEnter(None,EnterProximity)
		
		#Add info panel to display messages to participant
		instructions = vizinfo.InfoPanel(icon=False,key=None)
		
		#The following task directs the user where to go and waits until the user reaches each destination.
		def destinationsTask():

			# Action for hiding/showing text
			DelayHide = vizact.sequence( vizact.waittime(8), vizact.method.visible(False) )
			Show = vizact.method.visible(True)
			
			#instructions.setText("Reach the duck."+str(self.time))
			
			startTime = viz.tick()
			
			yield viztask.waitTime(5) 
			instructions.setText("Go to the duck, try to evade the axes.")
			instructions.runAction(DelayHide)
			
			
			elapsedTime = viz.tick() - startTime
			elapsedTime = str(round(elapsedTime,2))
			
			# When finished
			yield vizproximity.waitEnter(duckSensor)
			instructions.runAction(Show)
			yayString = "Thank you for your participation.\nYou hit the axes this many times: " + str(axesHit[0])
			for i in range(1, nrAxes):
				yayString += ", " + str(axesHit[i])
			yayString += ".\nTime is: " + str(elapsedTime)
			instructions.setText(yayString)
			#Show results of experiment
			print yayString

		viztask.schedule(destinationsTask())
		   
		vizact.onkeydown('g',manager.setDebug,viz.TOGGLE)  
		
		self.worldModel = viz.add('bridge3.OSGB') #load a world model         bridge3.OSGB  piazza.osgb
		self.worldModel.setScale(1,.3,1.5)
		
		self.use_keyboard = use_keyboard #store if we want to use the keyboard
		
		
		self.time = 0.0 #note that to 0.0 is important because it is a double precision floating point number
		#the variable above will be used to keep track of time
		#there may be a difference between the vizard clock and self.time
		#could be rounding error, could be something else
		
		
		self.speed = 400.0 #--four-- meters per second
		originTracker = self.cavelib.getOriginTracker()
		originTracker.setPosition([-100,100,200],viz.REL_LOCAL)
		self.yaw = 90
		
		
	def updateObjects(self,e):
		"""Set the world poses of the objects
		
		Especially those which are defined in the CAVE coordinate system.
		Since this function is called after the CAVE is moved (see movement of CAVE).
		"""
		
		#the delta time that has passed
		#you can use this value to advance your simulation
		elapsed = e.elapsed 
		
		#keep track of time	
		#this is just some time measurement
		#vizard probably has some clock function
		#there is no reason to prefer one time variable/function over the other
		#there is also no reason why the statement below is in this function and not in preUpdate
		self.time += elapsed
		
		
		#where is the horse located in the cave?
#		axe_position_in_cave_space = viz.Vector(math.cos(self.time), 1, math.sin(self.time))
		
		#convert the location (without orientation and scale) into a translation matrix
		#(having default orientation and scale)
#		axe_matrix_in_cave_space = viz.Transform.translate(axe_position_in_cave_space)
		
		#rotate the horse
		#note that pre euler is used
		#this means first rotate and than apply the translation transformation
#		axe_matrix_in_cave_space.preEuler(self.time / math.pi * -180.0,0,0)
		
		#convert the horse matrix to world space and assign it to the model
		
#		self.axe.setMatrix(self.cavelib.localMatrixToWorld(axe_matrix_in_cave_space))
		
		#set the wand (i.e. one of the trackers NOT the wiimote)		
		#the wand is viewed as a coordinate system
		self.wand.setMatrix(self.cavelib.localMatrixToWorld(self.cavelib.getWandMatrix()))
		
		#set the thing
		#the thing is the plant model
		#its motion is defined by the second tracker
	#	self.thing.setMatrix(self.cavelib.localMatrixToWorld(self.cavelib.getThingMatrix()))
		
		
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_BOTTOM_LEFT)) + " " ,
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_BOTTOM_RIGHT)) + " " ,
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_TOP_LEFT)) + " " ,
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_TOP_RIGHT)) + " " ,
		#print str(self.cavelib.getBalanceBoard(self.cavelib.BALANCE_BOARD_TOTAL))		
		
	def preUpdate(self,e):
		"""This function is executed before the updates are done."""
		pass
		
	def postUpdate(self,e):
		"""This function is exectuted after the updates are done."""		
		pass
						
	def	leftPressed(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			return viz.iskeydown(viz.KEY_LEFT) #keyboard input
		
		return caveapp.CaveApplication.leftPressed(self) #wiimote input
			
	def	rightPressed(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			return viz.iskeydown(viz.KEY_RIGHT)#keyboard input
		
		return caveapp.CaveApplication.rightPressed(self) #wiimote input
			
	def	upPressed(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			return viz.iskeydown(viz.KEY_UP)#keyboard input
		
		return caveapp.CaveApplication.upPressed(self) #wiimote input
			
	def	downPressed(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			return viz.iskeydown(viz.KEY_DOWN)#keyboard input
		
		return caveapp.CaveApplication.downPressed(self) #wiimote input
			
	def	joystick(self):
		"""Virtual function to use keyboard if indicated.
		
		This function can be omitted.
		If this function is omitted, the wiimote will always be used.
		"""
		if self.use_keyboard:
			
			#keyboard input
			
			result = [0.0,0.0,0.0]
			
			if viz.iskeydown('a'): 
				result[0] -= 1.0
				
			if viz.iskeydown('d'): 
				result[0] += 1.0
				
			if viz.iskeydown('q'): 
				result[1] -= 1.0
				
			if viz.iskeydown('e'): 
				result[1] += 1.0
				
			if viz.iskeydown('s'): 
				result[2] -= 1.0
				
			if viz.iskeydown('w'): 
				result[2] += 1.0
				
			if viz.iskeydown('r'):
				self.speed = self.speed * 1.01
				
			if viz.iskeydown('f'):
				self.speed = self.speed * 0.99
				
			return result
		
		return caveapp.CaveApplication.joystick(self) #wiimote input
		
	
################################################################
#Cave functionality
################################################################
#Param: True = DesktopMode on
#		False = DesktopMode off

print "Constructing the application class."
application = CustomCaveApplication(use_keyboard=True, desktop_mode=True) #boolean indicated wheter or not to use the keyboard instead of the wiimote

print "Setting the number of samples per pixel."

#Add ambient sound
piazzaSound = viz.addAudio('piazza.mp3')
#piazzaSound.play()
#piazzaSound.loop()


viz.setMultiSample(4)
viz.MainWindow.fov(60)
#viz.collision(viz.ON)

#viz.MainView.move([31,0,-71])
#viz.MainView.setEuler([0,30,0])
#import vizshape
#vizshape.addAxes()



application.go()

