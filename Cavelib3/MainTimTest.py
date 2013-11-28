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
	"""A custom CAVE application.
	
	You can choose to use or not use this object oriented construct.
	It is also possible to use cavelib3 without the caveapp.CaveApplication class.
	
	Note that this example application is intended to make things simple.
	It says ``intended`` ecause the object oriented layer may be confusing.
	Have a look at caveapp.py This will make things more clear.
	
	In python, if you redefine a function in a subclass, this function is virtual by default.
	The function in the subclass will be called instead of the function in the super class.
	
	If you think that caveapp.py can be improved upon, you can do so.
	Strictly caveapp.py is not part of the cavelib3.
	You should not have to alter the cavelib itself though.
	
	This construct is given as an example.
	Usually, people use vizard by using lots of callbacks.
	These callbacks, have an exectution order.
	Usually these exectution orders are not considered when writing an application, thereby introducing bugs.
	
	When using this class, you do not need to use any callbacks.
	There is just one __onUpdate function which gets called in caveapp.CaveApplication
	This call is distributed over several other calls of which the order is transparent.
	
	Another pitfall in vizard is automatic linking (of simulation objects).
	Instead of using link constructs, it is more transparent to set the world poses of objects at each frame.
	See updateObjects.
	
	A problem that arises with automatic linking of simulation objects is that links can have priorities.
	Priorities can be too low, causing the link to disfunction.
	
	If you have a conflicting transformation within the updateObjects function, then it is clear that only the last assignment will be used.
	Vizard wants to take care of many things, that is why it uses the link mechanism.
	However, other simulation tools usually do not have this.	
	In general, a simulation has an initialization function, an update function and a render function.
	This construct allows the user to initilialize and to update. Rendering is done automatically by vizard (after each update)(this is okay).
	"""
	
		
	def __init__(self,use_keyboard = True, desktop_mode = False):
		"""Initialization function."""
		
		caveapp.CaveApplication.__init__(self,desktop_mode) #call constructor of super class, you have to do this explicitly in Python		
		
		self.wand = vizshape.addAxes()#load axis model to represent the wand
	#	self.thing = viz.addChild('axe.OSGB') #load plant model to represent the thing      plant.osgb
	
		def swing(object, t, startAngle, endAngle):
			d = (math.sin(t[0]) + 1.0) / 2.0
			angle = startAngle + d * (endAngle - startAngle)
			object.setEuler([90,0,angle])
			t[0] += 0.03
			
		self.axe = viz.addChild('axe.OSGB', cache=viz.CACHE_CLONE)
		self.axe.setPosition([700,745,325],viz.REL_LOCAL)
		self.axe.setScale(225,225,325)
		self.axe.center(0,4.5,0)
		axe1t = [0.0]
		vizact.ontimer(0.03, swing, self.axe, axe1t, 120, 240)
		
		
		self.axe2 = viz.addChild('axe.OSGB') #load a horse model (this model will be animated in cave space)
		#self.axe2.setPosition([700,745,325],viz.REL_LOCAL)
		self.axe2.setEuler([90,0,180])
		#self.axe2.setScale(225,225,325)
		self.axe2.center(0,4.5,0)
		#self.axe2.addAction(vizact.spin(0,0,1,60,viz.FOREVER))
		
		self.axe3 = viz.addChild('axe.OSGB') #load a horse model (this model will be animated in cave space)
		self.axe3.setPosition([1800,745,325],viz.REL_LOCAL)
		self.axe3.setEuler([90,0,0])
		self.axe3.setScale(225,225,325)
		self.axe3.center(0,4.5,0)
		self.axe3.addAction(vizact.spin(0,0,1,75,viz.FOREVER))
		
		self.axe4 = viz.addChild('axe.OSGB') #load a horse model (this model will be animated in cave space)
		self.axe4.setPosition([1800,745,325],viz.REL_LOCAL)
		self.axe4.setEuler([90,0,180])
		self.axe4.setScale(225,225,325)
		self.axe4.center(0,4.5,0)
		self.axe4.addAction(vizact.spin(0,0,1,75,viz.FOREVER))
		
		self.axe5 = viz.addChild('axe.OSGB') #load a horse model (this model will be animated in cave space)
		self.axe5.setPosition([2700,745,325],viz.REL_LOCAL)
		self.axe5.setEuler([90,0,0])
		self.axe5.setScale(225,225,325)
		self.axe5.center(0,4.5,0)
		self.axe5.addAction(vizact.spin(0,0,1,80,viz.FOREVER))
		
		self.axe6 = viz.addChild('axe.OSGB') #load a horse model (this model will be animated in cave space)
		self.axe6.setPosition([2700,745,325],viz.REL_LOCAL)
		self.axe6.setEuler([90,0,180])
		self.axe6.setScale(225,225,325)
		self.axe6.center(0,4.5,0)
		self.axe6.addAction(vizact.spin(0,0,1,80,viz.FOREVER))
		
		newduck = viz.addAvatar('duck.cfg')
		newduck.setScale([170,170,170])

		#Place the new duck on the x-axis.
		#Each time the script goes through the loop, "eachnumber"
		#will be one larger so the ducks will fall in a line
		#along the x-axis
		newduck.setPosition([3700,65,325],viz.REL_LOCAL)
		newduck.setEuler([-90,0,0])

		
		manager = vizproximity.Manager()
		target = vizproximity.Target(viz.MainView)
		manager.addTarget(target)
		sensor = vizproximity.addBoundingBoxSensor(self.axe)
		manager.addSensor(sensor)
		sensor2 = vizproximity.addBoundingBoxSensor(self.axe2)
		manager.addSensor(sensor2)
		sensor3 = vizproximity.addBoundingBoxSensor(self.axe3)
		manager.addSensor(sensor3)
		sensor4 = vizproximity.addBoundingBoxSensor(self.axe4)
		manager.addSensor(sensor4)
		sensor5 = vizproximity.addBoundingBoxSensor(self.axe5)
		manager.addSensor(sensor5)
		sensor6 = vizproximity.addBoundingBoxSensor(self.axe6)
		manager.addSensor(sensor6)
		duckSensor = vizproximity.addBoundingBoxSensor(newduck,scale=(2.5,2.5,2.5))
		manager.addSensor(duckSensor)
		
		#Boolean variables to store trial results
		self.haxe = 0
		self.haxe2 = 0
		self.haxe3 = 0
		self.haxe4 = 0
		self.haxe5 = 0
		self.haxe6 = 0
		
		def EnterProximity(e):
			if e.sensor == sensor:
				self.haxe +=1
				print 'Hit first (total: ',self.haxe,' times)'
			elif e.sensor == sensor2:
				self.haxe2 +=1
				print 'Hit second (total: ',self.haxe2,' times)'
			elif e.sensor == sensor3:
				self.haxe3 +=1
				print 'Hit third (total: ',self.haxe3,' times)'
			elif e.sensor == sensor4:
				self.haxe4 +=1
				print 'Hit fourth (total: ',self.haxe4,' times)'
			elif e.sensor == sensor5:
				self.haxe5 +=1
				print 'Hit fifth (total: ',self.haxe5,' times)'
			elif e.sensor == sensor6:
				self.haxe6 +=1
				print 'Hit sixth (total: ',self.haxe6,' times)'
		
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
			
			yield vizproximity.waitEnter(duckSensor)
			instructions.runAction(Show)
			instructions.setText("Thank you for your participation.\nYou hit the following axis; number of times: "+str(self.haxe)+', '+str(self.haxe2)+', '+str(self.haxe3)+', '+str(self.haxe4)+', '+str(self.haxe5)+', '+str(self.haxe6)+"\nTime is: "+str(elapsedTime))
			#Show results of experiment
			print 'Hit axes following number of times: ',self.haxe,', ',self.haxe2,', ',self.haxe3,', ',self.haxe4,', ',self.haxe5,', ',self.haxe6

		viztask.schedule(destinationsTask())
		
		
#		#Change state of avatar to talking when the user gets near
#		def EnterProximity(e):
#			avatar.state(4)
#
#		#Change state of avatar to idle when the user moves away
#		def ExitProximity(e):
#			avatar.state(1)
#
#		manager.onEnter(sensor,EnterProximity)
#		manager.onExit(sensor,ExitProximity)
		   
		vizact.onkeydown('g',manager.setDebug,viz.TOGGLE)  
		
		#Add an object.
		#object = viz.add('wheelbarrow.ive')
		#Change the center of the object to 1m away from the origin.
		#object.center( 1, 0, 0 )
		#Spin the object around the new center.
		#object.addAction( vizact.spin(0,1,0,90) ) 
		
		#Add a parent.
		parent = viz.add( 'wheelbarrow.ive' )
		#Add a child to that parent.
		child = parent.add( 'duck.wrl' )
		#Set the position of the child.
		child.setPosition( 0,.35, -.05, viz.ABS_PARENT )
		#Spin the parent around in a circle.
		parent.center(1,0,0)
		parent.addAction(vizact.spin(0,1,0,90,viz.FOREVER)) 
		
	#	self.axe.color(0.5,0.5,0.5)#make the horse gray
		
	#	self.horse.disable(viz.LIGHTING) #disable the shading of the horse
		
		self.worldModel = viz.add('bridge3.OSGB') #load a world model         bridge3.OSGB  piazza.osgb
		self.worldModel.setScale(1,.3,1.5)
		
	#	self.headLight = viz.MainView.getHeadLight() #disable the headlight
	#	self.headLight.disable() #the headlight is disabled because the piazza.osgb is already shaded
		
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

