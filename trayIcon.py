#! /usr/bin/python
import pygtk
pygtk.require("2.0")
import gtk
import os
import threading
import subprocess
import multiprocessing
import time

class trayIcon:
  
  #On left-click event
  def openBrowser(self, widget):
    return
  
  def setImage(self, icon):
    self.icon.set_from_file(icon)
    
  def setText(self, text):
    self.icon.set_tooltip(text)
    
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
    #Initilize the updating thread
    self.icon = gtk.StatusIcon()
    #Tooltip is the mouseover text, should be changes to CPU frequencies
    self.icon.set_tooltip("Max frequency: 100mhz")
    self.setImage("cpufreq-100.png")
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


#Need a threaded class to run in the background and update every second, changing the image and setting the text
#Need to figure out how many CPUs there are
class UpdateThread( threading.Thread ):
  def run ( self ):
    #Frequency to compare current speed
    self.compFreq = self.maxFreq - self.minFreq
    while(1):
        #print 'Update core frequencies'
        self.text = ''
        #Update the text
        for i in range(0, self.cpus):
            self.freq[i] = self.getCurFreq(i)
            self.text += 'Core '+str(i)+': '+str(self.freq[i])+'Mhz\n'
        self.tray.setText(self.text.strip())
        #print self.text
        #Determine what image is best
        self.tmp = float(max(self.freq)) / float(self.maxFreq)
        #print self.tmp
        if(self.tmp >= 0.75):
            self.tray.setImage("cpufreq-100.png")
        elif(self.tmp >= 0.50):
            self.tray.setImage("cpufreq-75.png")
        elif(self.tmp >= 0.25):
            self.tray.setImage("cpufreq-50.png")
        else:
            self.tray.setImage("cpufreq-25.png")
        #print 'Sleeping...'
        time.sleep(2)
    return
    
  def setTray(self, tray):
    self.tray = tray
    
  def setNumCPUs(self, num):
    self.freq = range(num)
    self.cpus = num
  
  def getMaxFreq(self):
    # cpufreq-info -l | awk '{print $2}'
    # Max freq value
    self.p = subprocess.Popen(['cpufreq-info', '-l'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    self.maxFreq = int(self.p.stdout.readline().split()[1]) / 1000
    return self.maxFreq
    
  def getMinFreq(self):
    # cpufreq-info -l | awk '{print $1}'
    # Max freq value
    self.p = subprocess.Popen(['cpufreq-info', '-l'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    self.minFreq = int(self.p.stdout.readline().split()[0]) / 1000
    return self.minFreq

  
  def getCurFreq(self, core = 0):
    # cpufreq-info -c # -f
    self.p = subprocess.Popen(['cpufreq-info', '-c', str(core), '-f'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return int(self.p.stdout.readline()) / 1000
  
  def __init__(self, tray):
    threading.Thread.__init__(self)
    self.setTray(tray)
    self.getMaxFreq()
    self.getMinFreq()
    self.setNumCPUs(multiprocessing.cpu_count())
  

if __name__=="__main__":
  gtk.gdk.threads_init()
  icon = trayIcon()
  update = UpdateThread(icon).start()
  gtk.main()
