import os
import wx
import urllib2
import json
import requests
import urllib
import  cStringIO



class MainWindow(wx.Frame):


    def __init__(self, parent, title):
    	#API calls to get data from 
    	r = requests.get("http://api.wunderground.com/api/0def10027afaebb7/forecast/q/TX/Dallas.json")
	f=urllib2.urlopen('http://api.wunderground.com/api/da8c1b0d02f335f8/geolookup/conditions/q/TX/Dallas.json')
	json_string = f.read()
	data=r.json()
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	temp_f = parsed_json['current_observation']['temp_f']
        icon= parsed_json['current_observation']['icon']
	
	
    	wx.Frame.__init__(self, parent, title=title, size=(400,250))
    	panel = wx.Panel(self, -1)
        wx.StaticText(panel, -1, "Current temperature in %s is: %s" % (location, temp_f), pos=(10, 12))
        
        if temp_f<20: display="It's freezing! Wear everything you have!"
        elif  20<temp_f<40: display="It's freezing! Wear everything you have!"
        elif 40<temp_f<50: display="It's freezing! Wear everything you have!"
        elif 50<temp_f<60: display="It's freezing! Wear everything you have!"
        elif 60<temp_f<70: display="It's freezing! Wear everything you have!"
        elif 70<temp_f<80: display="It's freezing! Wear everything you have!"

    	wx.StaticText(panel, -1, display, pos=(10, 40))
        
        #hacked together way to use the custom icons that Wunderground provides
        first = "http://icons.wxug.com/i/c/j/"
        second=icon
        third=".gif"
        last=first+second+third
        fp = urllib.urlopen(last)
        data = fp.read()
        fp.close()
        stream = cStringIO.StringIO(data)

        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        
        self.picture = wx.StaticBitmap(panel, -1, bmp, pos=(10, 70))
        
        menubar = wx.MenuBar()
        help = wx.Menu()
        help.Append(100, '&About')
        self.Bind(wx.EVT_MENU, self.OnAboutBox, id=100)
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)

        self.SetSize((250, 250))
        self.SetTitle('About dialog box')
        self.Centre()
        self.Show(True)
        

    def OnAboutBox(self, e):
        
        description = """Simple weather application to help you decide what to wear. 
Coded entirely in Python using wxPython and the Wunderground API.
"""

        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('logo.png', wx.BITMAP_TYPE_PNG))
        info.SetName('What should I wear?')
        info.SetVersion('0.1')
        info.SetDescription(description)
        info.SetCopyright('(C) Brandon Roeder')
        info.SetWebSite('http://www.brandonsroeder.com')
        info.AddDeveloper('Brandon Roeder')
        wx.AboutBox(info)


app = wx.App(False)
frame = MainWindow(None, "What should I wear?")
app.MainLoop()