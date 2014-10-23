import os
import cv
import cv2
import kivy

#from pcl.pcl.pcl import *
from kivy.app import App
#from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition, SlideTransition
from kivy.uix.widget import Widget
#from kivy.uix.camera import Camera
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty    
#from kivy.uix.tabbedpanel import *
#from renderer.renderer import *
from kivy.uix.settings import *
from kivy.config import ConfigParser
from kivy.uix.progressbar import ProgressBar
from os.path import dirname, join 
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.popup import Popup
from kivy.uix.image import Image


from printrun.printcore import printcore
from printrun.gcoder import GCode
from printrun.utils import imagefile , lookup_file
#from printrun.gcoder_line import GLine
#import gcode

class MenuScreen(Screen):
    pass

class PrintScreen(Screen):
    pass

class ScanScreen(Screen):
    pass
    
class ShareScreen(Screen):
    pass
    
class ConfigScreen(Screen):
    pass

class PlaterScreen(Screen):
    pass
    
class ViewScreen(Screen):
    pass

class FileGcodeLoadScreen(Screen):
	pass

class CVCamera(Image):
    pass

class DuplicatorApp(App):
	#icon = 'icon.png'
	title = 'Duplicator - Ultimate 3D Printing App'
	#use_kivy_settings = False
	sm = 0
	gcode = None 
	
	'''
	def build_config(self, config):
		
		config.setdefaults('general', 
			{
				'app_background_color': '000000',
				'app_width': '640'
			}
		)
	
		config.setdefaults('printer', 
			{
        		'printer_com_port': '/dev/tty.usbmodem1411',
	            'printer_com_speed': '115200',
	            'printer_extruder_count': '2',
	            'printer_heated_bed': '70',
	            'printer_extruder_1_temp': '220',
	            'printer_extruder_2_temp': '220',
	            'printer_bed_temp': '70'
			}
		)
     '''

	
	def build_settings(self, settings):
		settings.add_json_panel('General Panel', self.config, join(dirname(__file__),'settings/settings_general.json' ) )
		settings.add_json_panel('Printer panel', self.config, join(dirname(__file__),'settings/settings_printer.json') )
		settings.add_json_panel('Scanner panel', self.config, join(dirname(__file__),'settings/settings_scanner.json') )
	
	
	def build(self):
		self.config = ConfigParser()
		self.config.read(join( dirname(__file__),'duplicator.ini') )
		
		print( self.config.get('general','app_background_color') )
		
		#if not self.config.has_section("general"):
		#    self.config.add_section("general")
	
		self.activeprinter = None
		self.printer_pause = 0
		
		
		
		self.sm = ScreenManager()
		self.sm.add_widget(MenuScreen(name='Menu'))
		self.sm.add_widget(PrintScreen(name='Print'))
		self.sm.add_widget(ScanScreen(name='Scan'))
		self.sm.add_widget(ShareScreen(name='Share'))
		self.sm.add_widget(ConfigScreen(name='Config'))
		self.sm.add_widget(PlaterScreen(name='Plater'))
		self.sm.add_widget(ViewScreen(name='View'))
		self.sm.add_widget(FileGcodeLoadScreen(name='FileGcodeLoad'))
		

		self.menu_bar = Factory.MenuBar()
		self.sm.get_screen('Menu').ids.window_layout.add_widget(self.menu_bar)
		self.menu_bar.ids.short_message.text = 'Duplicator Started\nReady for action.'
		
		self.cam1 = cv2.VideoCapture(0)
        
		
		return self.sm	
		
	def switchtoscreen(self,ScreenName):
		if ScreenName == 'Menu':
			self.sm.transition = SlideTransition(direction='left')
		elif ScreenName == 'FileGcodeLoad':
			self.sm.transition = SlideTransition(direction='up')
		else:
			if(self.sm.current=='FileGcodeLoad'):
				self.sm.transition = SlideTransition(direction='down')
			else:
				self.sm.transition = SlideTransition(direction='right')
		
		#print(self.sm.current)
		print(ScreenName)
		if(ScreenName != 'FileGcodeLoad') and (self.sm.current!='FileGcodeLoad'):
			self.sm.get_screen(self.sm.current).ids.window_layout.remove_widget(self.menu_bar)
			self.sm.get_screen(ScreenName).ids.window_layout.add_widget(self.menu_bar)
		self.sm.current = ScreenName
		
		
	def connectprinter(self,activeswitch):
		if activeswitch:
			self.menu_bar.ids.short_message.text = 'disconnecting....'
			try:
				self.activeprinter.disconnect()
				self.menu_bar.ids.short_message.text = 'Done'
				self.sm.get_screen('Print').ids.connectprinterswitch.active=0
				self.activeprinter = None
				self.menu_bar.ids.indicator_printer.color = (0,0,0,.3)
			except:
				self.menu_bar.ids.short_message.text = 'No printer!'
				self.sm.get_screen('Print').ids.connectprinterswitch.active=0
				self.menu_bar.ids.indicator_printer.color = (1,0,0,1)
		else: 
			#print(self.sm.get_screen('Print').ids)
			#print('connecting....')
			self.menu_bar.ids.short_message.text ='connecting....'
			try:
				#self.config.get('printer','printer_com_port'),self.config.get('printer','printer_com_speed')
				self.activeprinter=printcore('/dev/tty.usbmodem1411','115200')
				#print('connected')
				self.menu_bar.ids.short_message.text = 'connected'
				self.sm.get_screen('Print').ids.connectprinterswitch.active=1
				self.sm.get_screen('Print').ids.connectprinterswitch.state = 'down'
				self.menu_bar.ids.indicator_printer.color = (0,1,0,1)
			except:
				self.menu_bar.ids.short_message.text = 'Unable to connect!'
				#print('Unable to connect!')
				self.sm.get_screen('Print').ids.connectprinterswitch.active=0
				self.sm.get_screen('Print').ids.connectprinterswitch.state = 'normal'
				self.menu_bar.ids.indicator_printer.color = (1,0,0,1)
				
	def homeprinter(self):
		self.Send('G28')
		#if self.activeprinter != None:
			#self.activeprinter.send('G28')
		
	def homeX(self):
		if self.activeprinter != None:
			self.activeprinter.send('G28 X')
		
	def homeY(self):
		if self.activeprinter != None:
			self.activeprinter.send('G28 Y')
		
	def homeZ(self):
		if self.activeprinter != None:
			self.activeprinter.send('G28 Z')
			
	def pause(self):
		if self.activeprinter != None:
			if self.printer_pause:
				self.activeprinter.pause()
				self.sm.get_screen('Print').ids.connectprinterswitch.state = 'normal'
			else:
				self.activeprinter.resume()
				self.sm.get_screen('Print').ids.connectprinterswitch.state = 'down'
	
	def emergencyStop(self):	
		if self.activeprinter != None:
			self.activeprinter.send_now('M112')		
	
	def send(self,code):
		if self.activeprinter != None:
			self.activeprinter.send(code)
			
	def move(self,axes,distance):
		if self.activeprinter != None:
			self.activeprinter.send('G1 '+axes+' '+distance)

	def cameraSwitch(self):
		if(self.sm.get_screen('Scan').ids.camera_button.state=='normal'):
			#self.sm.get_screen('Scan').ids.scan_camera.play=True
			#self.sm.get_screen('Scan').ids.scan_camera.resolution=(640, 480)
			#self.sm.get_screen('Scan').ids.scan_camera.index=0
			self.sm.get_screen('Scan').ids.camera_button.color = (1,1,1,1)
			self.menu_bar.ids.indicator_scanner.color = (1,1,0,1)
			self.menu_bar.ids.indicator_camera.color = (0,1,0,1)
			#ret, frame = cam.read()
			#Clock.schedule_interval(self.camUpdate, 1.0/33.0)
		else:
			#self.sm.get_screen('Scan').ids.scan_camera.play=False
			self.sm.get_screen('Scan').ids.camera_button.color = (0,0,0,1)
			self.menu_bar.ids.indicator_scanner.color = (1,1,1,.3)
			self.menu_bar.ids.indicator_camera.color = (1,1,1,.3)

	def closeSettingsScreen(self):		
		App.close_settings()

	def printGcodeFile(self):
		if self.activeprinter != None:
			if self.gcode != None:
				self.activeprinter.startprint(self.gcode,0)
				self.menu_bar.ids.indicator_printer.color = (1,1,0,1)
			else:
				self.menu_bar.ids.indicator_printer.color = (0,1,0,1)
				self.menu_bar.ids.short_message.text = 'No File Loaded!'
		else:
			self.menu_bar.ids.indicator_printer.color = (1,1,1,.33)
			self.menu_bar.ids.short_message.text = 'No Printer Connected!'
	
	def reset(self):
		if self.activeprinter != None:
			self.activeprinter.reset()		

	def show_gcode_load(self):
		self.switchtoscreen('FileGcodeLoad')

	def cancelFileGcodeLoad(self):
		self.switchtoscreen('Print')

	def load_gcode(self, path, filename):
		with open(os.path.join(path, filename[0])) as stream:
			gcode_string = stream.read()
		
		self.sm.get_screen('Print').ids.gcode_file_name.text = filename[0]
		
		self.gcode = gcode_string.split('\n')
		#print(self.gcode.lines)
		self.switchtoscreen('Print')
		
		

if __name__ == '__main__':
    DuplicatorApp().run()
    #pongApp().run()
        
