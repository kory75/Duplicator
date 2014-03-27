import kivy
from kivy.app import App
#from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.camera import Camera
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty            

from printrun.printcore import printcore
from printrun.gcoder import GCode
from printrun.printrun_utils import imagefile , lookup_file
#import gcode

class MenuScreen(Screen):
    pass

class PrintScreen(Screen):
    pass

class ScanScreen(Screen):
    pass
    
class FileScreen(Screen):
    pass
    
class ControllScreen(Screen):
    pass

class ModelScreen(Screen):
    pass
    
class ViewScreen(Screen):
    pass

class DuplicatorApp(App):
	#icon = 'icon.png'
    #title = 'Duplicator Ultimate 3D printing app - alpha'
    
	sm = 0
	def build(self):
		self.sm = ScreenManager()
		self.sm.add_widget(MenuScreen(name='menu'))
		self.sm.add_widget(PrintScreen(name='print'))
		self.sm.add_widget(ScanScreen(name='scan'))
		self.sm.add_widget(FileScreen(name='file'))
		self.sm.add_widget(ControllScreen(name='controll'))
		self.sm.add_widget(ModelScreen(name='model'))
		self.sm.add_widget(ViewScreen(name='view'))
		
		#connecttoprinter.bind(active=switchprinter)
		return self.sm
		
	def switchtoscreen(self,ScreenName):
		self.sm.current = ScreenName
		#self.sm.switch_to(self.sm.get_screen(ScreenName))
		#pass
		
	def connectprinter(self,activeswitch):
		if activeswitch:
			print('connecting')
			try:
				self.activeprinter=printcore('/dev/tty.usbmodem1411',115200)
				print('connected')
			except:
				print('Unable to connect!')
				#self.connectprinterswitch.active=0
				
		else: 
			print('disconnecting....');
			try:
				self.activeprinter.disconnect()
				print('Done');
			except:
				print('No printer')
				
				
	def homeprinter(self):
		self.activeprinter.send_now('G28')
		
	def homeX(self):
		self.activeprinter.send_now('G28 X')
		
	def homeY(self):
		self.activeprinter.send_now('G28 Y')
		
	def homeZ(self):
		self.activeprinter.send_now('G28 Z')
	

if __name__ == '__main__':
    DuplicatorApp().run()
    #pongApp().run()
    
	    
