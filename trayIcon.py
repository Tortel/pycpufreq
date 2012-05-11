#! /usr/bin/python
import pygtk
pygtk.require("2.0")
import gtk
import os
import threading
import subprocess

class trayIcon:
  
  #On left-click event
  def openBrowser(self, widget):
    self.icon.set_from_file("cpufreq-100.png")
      
  def openWindow(self, widget):
    return

  def exitProgram(self, widget, data = None):
    if data:
        data.set_visible(False)
    gtk.main_quit()
    exit()


  def showMenu(self, widget, button, time, data = None):
    #On right click, open the options menu
    if button == 3:
        if data:
            data.show_all()
            data.popup(None, None, None, 3, time) 

  def __init__(self):
    #Get the max freq
    self.updater = UpdateThread()
    self.maxFreq = self.updater.getMaxFreq();
    self.icon = gtk.StatusIcon()
    #Tooltip is the mouseover text, should be changes to CPU frequencies
    self.icon.set_tooltip("Max frequency: "+self.maxFreq)
    self.icon.set_from_file("cpufreq-100.png")
    self.icon.connect("activate", self.openBrowser)
    self.menu = gtk.Menu()
    #First menu item
    self.menuItem = gtk.MenuItem("Change Settings")
    self.menuItem.connect('activate', self.openWindow)
    self.menu.append(self.menuItem)
    self.menuItem = gtk.MenuItem()
    self.menu.append(self.menuItem)
    #Exit menu option
    self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    self.menuItem.connect('activate', self.exitProgram, self.icon)
    self.menu.append(self.menuItem)
    self.icon.connect("popup-menu",self.showMenu,self.menu)


    
def main():
  gtk.main()


#Need a threaded class to run in the background and update every second, changing the image and setting the text
#Need to figure out how many CPUs there are
class UpdateThread( threading.Thread ):
  def run ( self ):
    return
  
  def getMaxFreq(self):
    # cpufreq-info -l | awk '{print $2}'
    # Max freq value
    self.p = subprocess.Popen(['cpufreq-info', '-l', '|', 'awk', '\'{print $2}\''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return self.p.stdout.readline()

  
  def getCurFreq(self):
    # cpufreq-info -c # -f
    return


  

if __name__=="__main__":
  icon = trayIcon()
  main()
