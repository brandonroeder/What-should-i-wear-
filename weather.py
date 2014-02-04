import os
import wx
import urllib2
import json
import requests
import urllib
import  cStringIO
from pyzipcode import ZipCodeDatabase



class Weather(wx.Frame):


    def __init__(self, parent, title):
    	#API calls to get data from 
		
    	wx.Frame.__init__(self, parent, title=title, size=(450,280))
    	self.panel = wx.Panel(self, -1)
        
        self.lblname = wx.StaticText(self.panel, label="Please enter zipcode:", pos=(10, 170))
        self.editname = wx.TextCtrl(self.panel, size=(140, -1), pos=(10, 190))
        self.button = wx.Button(self.panel, label="Enter", pos=(150,187))
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)  
        
        #code for the menu bar
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&Settings')
        help = wx.Menu()
        help.Append(100, '&About')
        self.Bind(wx.EVT_MENU, self.OnAboutBox, id=100)
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        self.Centre()
        self.Show(True)
        
        #code for the about box
    def OnAboutBox(self, e):
        
        description = """Simple weather application to help you decide what to wear. 
Coded entirely in Python using wxPython and the Wunderground API.
"""

        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('logo.png', wx.BITMAP_TYPE_PNG)) #wunderground logo
        info.SetName('What should I wear?')
        info.SetVersion('0.1')
        info.SetDescription(description)
        info.SetCopyright('(C) Brandon Roeder')
        info.SetWebSite('http://www.brandonsroeder.com')
        info.AddDeveloper('Brandon Roeder')
        wx.AboutBox(info)

    def OnButton(self, e):
        #using zip code database to lookup city info
        zipcode=(self.editname.GetValue())
        zcdb = ZipCodeDatabase()
        zipcode1 = zcdb[zipcode]

        city=zipcode1.city
        state=zipcode1.state
                
        #another hacked up way so that user can specify zip
        conditions= 'http://api.wunderground.com/api/da8c1b0d02f335f8/geolookup/conditions/q/'
        forecasturl= 'http://api.wunderground.com/api/0def10027afaebb7/forecast/q/'
        stateurl= state+ '/'
        cityurl= city+'.json'
        final=conditions+stateurl+cityurl
        finalforecast= forecasturl+stateurl+cityurl
	f=urllib2.urlopen(final)
        r = requests.get(finalforecast)

	json_string = f.read()
	data=r.json()
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	temp_f = parsed_json['current_observation']['temp_f']
        icon= parsed_json['current_observation']['icon']


        wx.StaticText(self.panel, -1, "Current temperature in %s is: %s" % (city+', '+state, temp_f), pos=(10, 12))
        if temp_f<20: display="It's freezing! Wear everything you have! "
        elif  20<temp_f<40: display="It's freezing! Wear everything you have!"
        elif 40<temp_f<50: display="Still really cold! Jacket and pants for sure!"
        elif 50<temp_f<60: display="It's a little chilly! Light jacket and pants"
        elif 60<temp_f<70: display="Wow it feels great outside! Light jacket and you're set"
        elif 70<temp_f<80: display="Perfect temperature! You don't even need a jacket"
        elif 80<temp_f<90: display="It's pretty hot outside, wear as little clothes as possible"
        elif 90<temp_f<100: display="I wouldn't reccomend going outside.. wear nothing"
        elif temp_f>100: display="It's hot. I don't need to tell you what to wear"
        elif temp_f>120: display="You are dead. sorry"

    	wx.StaticText(self.panel, -1, display, pos=(10, 40))
        wx.StaticText(self.panel, -1, "Forecast: ", pos=(10, 60))
        
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
        self.picture = wx.StaticBitmap(self.panel, -1, bmp, pos=(10, 90))


    
app = wx.App(False)
frame = Weather(None, "What should I wear?")
app.MainLoop()