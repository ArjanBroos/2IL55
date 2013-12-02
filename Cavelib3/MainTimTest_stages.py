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

################################################################
#Code, with respect to she functionality should be in here
################################################################

class CustomCaveApplication(caveapp.CaveApplication):

	def __init__(self,use_keyboard = True, desktop_mode = False):
		
		caveapp.CaveApplication.__init__(self,desktop_mode) #call constructor of super class, you have to do this explicitly in Python		
		self.wand = vizshape.addAxes() #load axis model to represent the wand (WALL FFS!)
		
		# Add skybox
		sky = viz.add(viz.ENVIRONMENT_MAP,'hell/necros_hell.jpg')
		skybox = viz.add('skydome.dlc')
		skybox.texture(sky)
		
		# First light added seems to be ignored....
		# Add lighting
		dummy = viz.addLight()
		light = viz.addLight()
		light.position(0, 0, 0)
		light.color([0.8, 0.8, 0.8])
		
		self.use_keyboard = use_keyboard #store if we want to use the keyboard
		#self.time = 0.0 #note that to 0.0 is important because it is a double precision floating point number
		
		self.speed = 400.0 #--four-- meters per second
		originTracker = self.cavelib.getOriginTracker()
		originTracker.setPosition([-100,100,200],viz.REL_LOCAL)
		self.yaw = 90
		self.startSet=0
		self.joystickpressed=0
		
	def stageAxes(self, NAxes):
		# Function for swinging the axes
		def swing(object, t, startAngle, endAngle):
			d = (math.sin(t[0]) + 1.0) / 2.0
			angle = startAngle + d * (endAngle - startAngle)
			object.setEuler([90,0,angle])
			t[0] += 0.03
		
		# Add axes
		nrAxes = NAxes
		self.axes = []
		self.axest = []
		for i in range(nrAxes):
			self.axes.append(viz.addChild('axe.OSGB', cache=viz.CACHE_CLONE))
			self.axes[i].setPosition([300+i*(6600/nrAxes),745,325], viz.REL_LOCAL)
			self.axes[i].setScale(225,225,325)
			self.axes[i].center(0,4.5,0)
			self.axest.append([float(i)])
			vizact.ontimer(0.03, swing, self.axes[i], self.axest[i], 120, 240)
		
		# Add ducky
		self.newduck = viz.addAvatar('duck.cfg')
		self.newduck.setScale([170,170,170])
		self.newduck.setPosition([7200,65,325],viz.REL_LOCAL)
		self.newduck.setEuler([-90,0,0])

		# Add proximity sensors
		manager = vizproximity.Manager()
		target = vizproximity.Target(viz.MainView)
		manager.addTarget(target)
		sensors = []
		for i in range(nrAxes):
			sensors.append(vizproximity.addBoundingBoxSensor(self.axes[i]))
			manager.addSensor(sensors[i])
		duckSensor = vizproximity.addBoundingBoxSensor(self.newduck,scale=(2.5,2.5,2.5))
		manager.addSensor(duckSensor)
		
		# Boolean variables to store trial results
		self.axesHit = []
		for i in range(nrAxes):
			self.axesHit.append(0)
		
		# Called when we enter a proximity
		def EnterProximity(e):
			for i in range(nrAxes):
				if e.sensor == sensors[i]:
					self.axesHit[i] += 1
					print "Hit axe #" + str(i) + " " + str(self.axesHit[i]) + " times!"
		
		manager.onEnter(None,EnterProximity)
		
		#Add info panel to display messages to participant
		self.instructions = vizinfo.InfoPanel(icon=False,key=None)
		
		vizact.onkeydown('g',manager.setDebug,viz.TOGGLE)  
		
		# Action for hiding/showing text
		DelayHide = vizact.sequence( vizact.waittime(8), vizact.method.visible(False) )
		Show = vizact.method.visible(True)
		
		#instructions.setText("Reach the duck."+str(self.time))
		
		self.startTime = viz.tick()
		
		yield viztask.waitTime(5)
		self.instructions.setText("Go to the duck, try to evade the axes.")
		self.instructions.runAction(DelayHide)
		
		
		# When finished
		yield vizproximity.waitEnter(duckSensor)
		
		self.elapsedTime = viz.tick() - self.startTime
		self.elapsedTime = str(round(self.elapsedTime,2))
		
		self.instructions.runAction(Show)
		yayString = "Thank you for your participation.\nYou hit the axes this many times: " + str(self.axesHit[0])
		for i in range(1, nrAxes):
			yayString += ", " + str(self.axesHit[i])
		yayString += ".\nTime is: " + str(self.elapsedTime)
		self.instructions.setText(yayString)
		#Show results of experiment
		print yayString
		
		
	def experiment(self):
		self.loadScene()
		yield viztask.waitTime(1)
		yield self.stageAxes(4)
		print "Stage 1"
		self.deleteScene()
		yield viztask.waitTime(3)
		
		self.returnToStart()
		yield self.stageAxes(6)
		print "Stage 2"
		self.deleteScene()
		yield viztask.waitTime(3)
		
		self.returnToStart()
		yield self.stageAxes(8)
		print "Stage 3"
		self.deleteScene()
		yield viztask.waitTime(3)
		
		self.returnToStart()
		yield self.stageAxes(10)
		print "Stage 4"
		self.deleteScene()
		yield viztask.waitTime(3)
		
	def returnToStart(self):
		originTracker = self.cavelib.getOriginTracker()
		originTracker.setPosition([-100,100,200])
		self.yaw = 90
		
	def loadScene(self):
		self.worldModel = viz.add('bridge3.OSGB') #load a world model         bridge3.OSGB  piazza.osgb
		self.worldModel.setScale(2,.3,1.5)
		
	def deleteScene(self):
		for axe in self.axes:
			axe.remove()
		self.newduck.remove()
		self.instructions.remove()
		
	def updateObjects(self,e):
		"""Set the world poses of the objects
		
		Especially those which are defined in the CAVE coordinate system.
		Since this function is called after the CAVE is moved (see movement of CAVE).
		"""
		
		#the delta time that has passed
		#you can use this value to advance your simulation
	#	elapsed = e.elapsed 
		
		#keep track of time	
		#this is just some time measurement
		#vizard probably has some clock function
		#there is no reason to prefer one time variable/function over the other
		#there is also no reason why the statement below is in this function and not in preUpdate
	#	self.time += elapsed
		
		#set the wand (i.e. one of the trackers NOT the wiimote)		
		#the wand is viewed as a coordinate system
		self.wand.setMatrix(self.cavelib.localMatrixToWorld(self.cavelib.getWandMatrix()))
		
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
		
		# Warning: this function is called using polling!
		
		if self.use_keyboard:
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

viz.setMultiSample(4)
viz.MainWindow.fov(60)
viz.MainView.getHeadLight().disable()
#viz.collision(viz.ON)
application.go()

viztask.schedule(application.experiment)
