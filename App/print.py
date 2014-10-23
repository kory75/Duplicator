from printrun.printcore import printcore
from printrun.gcoder import GCode
from printrun.utils import imagefile , lookup_file


class Print():
	printers = None
	gcode = None 
	
	def build(self):
		self.printers = None
	
	def doAction(self, action):	
		
class Printer():
	connection = None
	speed = None
	active = 0
	printing = 0
	driver = None
	
	def build(self):
		self.connection = None
		self.speed = None
		
	def connect(self,type,connection,speed):
		if type == "USB":
			self.connection = connection
			self.speed = speed
		
	def _send(self, code):
	
	def _sendNow(self, code):
	
	def startPrint(self,gcode):
	
	def disconnect(self):
	
	def _printing(self):
	
	def _run(self):