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
from time import gmtime, strftime

################################################################
#Code, with respect to she functionality should be in here
################################################################

class CustomCaveApplication(caveapp.CaveApplication):

	def __init__(self,use_keyboard = True, desktop_mode = False):
		
		caveapp.CaveApplication.__init__(self,desktop_mode) #call constructor of super class, you have to do this explicitly in Python		
		#self.wand = vizshape.addAxes() #load axis model to represent the wand (WALL FFS!)
		
		# Add skybox
		sky = viz.add(viz.ENVIRONMENT_MAP,'alien/jajalien1.jpg')
		skybox = viz.add('skydome.dlc')
		skybox.texture(sky)
		
		# First light added seems to be ignored....
		# Add lighting
		dummy = viz.addLight()
		light = viz.addLight()
		light.position(0, 0, 0)
		light.color([0.8, 1, 0.8])
		
		self.use_keyboard = use_keyboard #store if we want to use the keyboard
		#self.time = 0.0 #note that to 0.0 is important because it is a double precision floating point number
		
		self.speed = 400.0 #--four-- meters per second
		originTracker = self.cavelib.getOriginTracker()
		#originTracker.setPosition([-100,100,0],viz.REL_LOCAL)
		self.returnToStart()
		self.yaw = 90
		self.startSet=0
		self.joystickpressed=0
		
		vizact.onkeydown(' ', viz.setDebugSound3D, viz.TOGGLE)
		
	def stageAxes(self, NAxes, relSpeed):
		# Function for swinging the axes
		def swing(object, t, startAngle, endAngle):
			d = (math.sin(t[0]) + 1.0) / 2.0
			angle = startAngle + d * (endAngle - startAngle)
			object.setEuler([90,0,angle])
			t[0] += 0.03 * relSpeed
		
		# Add axes
		beginPosition = 400
		endPosition = 6600
		nrAxes = NAxes
		self.axes = []
		self.axest = []
		self.swoosh = []
		for i in range(nrAxes):
			self.axes.append(viz.addChild('axe.OSGB', cache=viz.CACHE_CLONE))
			self.axes[i].setPosition([beginPosition+i*(endPosition/nrAxes),750,0], viz.REL_LOCAL)
			self.axest.append([float(i)])
			
			sound_node = viz.addGroup(pos=[beginPosition+i*(endPosition/nrAxes),75,0])
			self.swoosh.append(sound_node.playsound('swoosh.wav'))
			self.swoosh[i].minmax(0, 20)
			vizact.ontimer(3.14/relSpeed, self.swoosh[i].play)
			
			vizact.ontimer(0.03, swing, self.axes[i], self.axest[i], 120, 240)
		
		# Add ducky
		self.newduck = viz.addAvatar('duck.cfg')
		self.newduck.setScale([170,170,170])
		self.newduck.setPosition([7200,0,0],viz.REL_LOCAL)
		self.newduck.setEuler([-90,0,0])

		# Add proximity sensors
		manager = vizproximity.Manager()
		target = vizproximity.Target(viz.MainView)
		manager.addTarget(target)
		self.axesensors = []
		for i in range(nrAxes):
			self.axesensors.append(vizproximity.addBoundingBoxSensor(self.axes[i]))
			manager.addSensor(self.axesensors[i])
		duckSensor = vizproximity.addBoundingBoxSensor(self.newduck,scale=(2.5,2.5,3))
		manager.addSensor(duckSensor)
		
		# Boolean variables to store trial results
		self.axesHit = []
		for i in range(nrAxes):
			self.axesHit.append(0)
			
#		for i in range(nrAxes):
#			sensors.append(vizproximity.addBoundingBoxSensor(self.axes[i]))
#			manager.addSensor(sensors[i])
		
		holeCoordinates = [
		[695,0,95],
		[695,0,-98],
		[1331,0,-1.5],
		[1957,0,98],
		[2443,0,-5],
		[2927,0,-108],
		[3716,0,-55],
		[4666,0,49],
		[5465,0,95],
		[5465,0,-104],
		[5951,0,-7]]
		
		self.holesensor = []
		k=-1
		for hole in holeCoordinates:
			k+=1
			self.holesensor.append(vizproximity.Sensor(vizproximity.Box([50,300,100],center=hole),source=viz.Matrix.translate(0,0,0)))
			manager.addSensor(self.holesensor[k])
			
		
		self.holesHit = []
		for i in range(len(self.holesensor)):
			self.holesHit.append(0)
		
		# Called when we enter a proximity
		def EnterProximity(e):
			for i in range(nrAxes):
				if e.sensor == sensors[i]:
					self.axesHit[i] += 1
					print "Hit axe #" + str(i) + " " + str(self.axesHit[i]) + " times!"
					
			for i in range(len(self.holesensor)):
				if e.sensor == self.holesensor[i]:
					self.holesHit[i] += 1
					print "Hit hole #" + str(i) + " " + str(self.holesHit[i]) + " times!"
		
		manager.onEnter(None,EnterProximity)
		
		#Add info panel to display messages to participant
		self.instructions = vizinfo.InfoPanel(icon=False,key=None)
		
		vizact.onkeydown('g',manager.setDebug,viz.TOGGLE)  
		
		# Action for hiding/showing text
		DelayHide = vizact.sequence( vizact.waittime(8), vizact.method.visible(False) )
		Show = vizact.method.visible(True)
		
		#instructions.setText("Reach the duck."+str(self.time))
		self.startTime = viz.tick()
		
		
		print "done with scene, awaiting duck"
		print "----------Begin stage "+str(self.stage)+"----------"
		# When finished
		yield vizproximity.waitEnter(duckSensor)
		
		self.elapsedTime = viz.tick() - self.startTime
		self.elapsedTime = str(round(self.elapsedTime,2))
		yayString = "Total number of axes hit: "
		if NAxes>0: yayString += str(self.axesHit[0])
		for i in range(1, nrAxes):
			yayString += ", " + str(self.axesHit[i])
		yayString += ".\nTime is: " + str(self.elapsedTime)
		print yayString
		self.tracking_data.write(yayString)
		print "----------End stage----------"
		
	def activateHeadTracking(self, activate):
		self.recording.setEnabled(activate)

		
	def setStage(self,stage,NAxes,relSpeed,holes,waittime):
		self.stage = stage
		if holes == True:
			self.bridge = viz.add('bridgeHoles.OSGB')
		else:
			self.bridge = viz.add('bridge.OSGB')
		
		self.tracking_data.write("Stage "+str(stage)+"\n")
		yield self.activateHeadTracking(True)
		yield self.stageAxes(NAxes,relSpeed)
		yield self.activateHeadTracking(False)
		
		yield self.deleteScene()
		yield viztask.waitTime(waittime)
		yield self.returnToStart()
		
	def returnToStart(self):
		originTracker = self.cavelib.getOriginTracker()
		originTracker.setPosition([0,75,0])
		self.yaw = 90
		
	def deleteScene(self):
		for axe in self.axes:
			axe.remove()
		self.newduck.remove()
		self.bridge.remove()
		self.instructions.remove()
		for swoosh in self.swoosh:
			swoosh.remove()
			
	def recordHeadTracking(self,stage):
		fileName = self.participant + "-" + str(stage) + ".txt"
		self.tracking_data = open(fileName, 'a')  #'+str(subject)+'
		self.tracking_data.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\n")
		
		#Get the tracking data.
		def getData():
			orientation = viz.MainView.getEuler()
			orientation[0] += 90
			orientation[1] += -90
			position = viz.MainView.getPosition()
			#Make a string out of the data.
			data = str(orientation) + '\t' + str(position) + '\n'  #str(subject) + '\t' + 
			#Write it to the tracking file.
			self.tracking_data.write(data)

		self.recording = vizact.ontimer(0.2, getData)
		
		
	def experiment(self):
		waittime = 0.5
		
		self.participant = raw_input("Participant name: ")
		print "Participant = ", self.participant
		
		nAxes = 0
		axeSpeed = 1
		stage = 0
		yield self.recordHeadTracking(stage)
		yield self.setStage(stage,nAxes,axeSpeed,True,waittime)
		nAxes = 5
		
		stage = 1
		yield self.recordHeadTracking(stage)
		yield self.setStage(stage,nAxes,axeSpeed,False,waittime)
		
		stage = 2
		yield self.recordHeadTracking(stage)
		yield self.setStage(stage,nAxes,axeSpeed,True,waittime)
		
		stage = 3
		axeSpeed = 2
		yield self.recordHeadTracking(stage)
		yield self.setStage(stage,nAxes,axeSpeed,False,waittime)
		
		stage = 4
		yield self.recordHeadTracking(stage)
		yield self.setStage(stage,nAxes,axeSpeed,True,waittime)
		
		stage = 5
		axeSpeed = 3
		yield self.recordHeadTracking(stage)
		yield self.setStage(stage,nAxes,axeSpeed,False,waittime)
		
		stage = 6
		yield self.recordHeadTracking(stage)
		yield self.setStage(stage,nAxes,axeSpeed,True,waittime)
		
		
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
				
			#if viz.iskeydown('q'): 
				#result[1] -= 1.0
				
			#if viz.iskeydown('e'): 
				#result[1] += 1.0
				
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
