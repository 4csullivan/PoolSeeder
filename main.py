import challonge
import asyncio
import wx
import seeder as seed
import configparser
import os
import pathlib
import time

# Class for initializing drop down window
class ConfigWindow(wx.Frame):

    # Set up on initialized.
    def __init__(self, parent, title):
        super(ConfigWindow,self).__init__(parent,title=title)
        self.InitUI()
        self.Centre()
        self.Show()

    # Creates a config file if config file has not been found.
    # If found, update the values in the config file.
    def ScanDoc(self):
        self.config = configparser.ConfigParser()
        if not os.path.isfile(pathlib.Path('config.ini')):
            file = open(pathlib.Path('config.ini'),'w')
            self.config.add_section('SETTINGS')
            file.close()
        self.config.read(pathlib.Path('config.ini'))
        if self.myU == '':
            self.myU = self.config.get('SETTINGS','username')
        else:
            self.config.set('SETTINGS','username', self.myU)
        if self.myKey == '':
            self.myKey = self.config.get('SETTINGS','username')
        else:
            self.config.set('SETTINGS','key', self.myKey)
        if self.isSub:
            if self.mySub == '':
                self.mySub = self.config.get('SETTINGS','subdomain')
            else:
               self.config.set('SETTINGS','subdomain', self.mySub)
        else:
            self.config.set('SETTINGS','subdomain', 'none')
        with open(pathlib.Path('config.ini'), 'w+') as cfile:
            self.config.write(cfile)

    # If the button has been pressed, update values and enter them
    # into the config file.
    def onButton(self, e):
        self.usrRes.SetLabel(self.usrT.GetValue())
        self.keyRes.SetLabel(self.keyT.GetValue())
        self.subRes.SetLabel(self.subT.GetValue())
        self.myU = str(self.usrRes.GetLabel())
        self.myKey = str(self.keyRes.GetLabel())
        self.mySub = str(self.subRes.GetLabel())
        self.ScanDoc()
        self.Close()

    # Checks if subdomain is checked, and update
    # necessary values for the config file.
    def checkSub(self, e):
        obj = e.GetEventObject()
        if obj.GetValue():
            self.subDom.Show()
            self.subT.Show()
            self.Layout()
            self.isSub = True
        else:
            self.subDom.Hide()
            self.subT.Hide()
            self.Layout()
            self.isSub = False

    # Set up UI for initializing window.
    # See main window for info on most of
    # this.
    def InitUI(self):
        self.SetMaxSize(wx.Size(1920,200))
        self.SetMinSize(wx.Size(300,200))
        self.SetInitialSize(wx.Size(300,200))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#cae8dd')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        fgs = wx.FlexGridSizer(3, 2, 9, 25)

        # Username input.
        usr = wx.StaticText(panel, label="Username")
        self.usrRes = wx.StaticText(panel, label="")

        # API key input.
        key = wx.StaticText(panel, label="API Key")
        self.keyRes = wx.StaticText(panel, label="")

        # Subdomain input.
        # Note: subomain is only needed if using
        # a community.
        self.subDom = wx.StaticText(panel, label="Subdomain")
        self.subRes = wx.StaticText(panel, label="")
        self.subT = wx.TextCtrl(panel)

        self.usrT = wx.TextCtrl(panel)
        self.keyT = wx.TextCtrl(panel)


        fgs.AddMany([(usr), (self.usrT, 1, wx.EXPAND), (key), (self.keyT, 1, wx.EXPAND), (self.subDom), (self.subT, 1, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)])

        # Initially hide the subomain.
        self.subDom.Hide()
        self.subT.Hide()
        self.Layout()

        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)
        hbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)

        vbox.Add(hbox, flag=wx.ALL | wx.EXPAND)

        # Save button.
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        goBtn = wx.Button(panel, label='Save', size=(70, 30))
        goBtn.Bind(wx.EVT_BUTTON, self.onButton)

        # Checkmark button to show or hide the subdomain.
        checkBtn = wx.CheckBox(panel,label='Subdomain?')
        checkBtn.SetValue(False)
        self.isSub = False
        checkBtn.Bind(wx.EVT_CHECKBOX,self.checkSub)

        hbox1.Add(goBtn, flag=wx.ALIGN_CENTER, border=5)
        hbox1.Add(checkBtn, flag=wx.ALIGN_CENTER, border=5)
        vbox.Add(hbox1, flag=wx.ALIGN_CENTER, border=10)

        panel.SetSizer(vbox)

# Class for the main window.
class MainWindow(wx.Frame):

    # Setup for initializing main window.
    def __init__(self, parent, title):
        super(MainWindow,self).__init__(parent,title=title)
        self.InitUI()
        self.Centre()
        self.Show()

    # If main window button is pressed, run the seeder.
    def onButton(self,e):
        self.Run(False)
        diagR = wx.MessageDialog(self, 'Seeding complete!', 'Result', wx.OK)
        if diagR.ShowModal() == wx.OK:
            diagR.Close(True)

    # Run the seeder by calling 'seeder.py' with either
    # True (undo seeder) or False(run seeder).
    # Note: the 'achallonge' package runs asynchronous-ly.
    # As a result, asyncio is needed to run the seeder.
    def Run(self, ifUndo):
        s = seed
        tID = str(self.tT.GetValue())
        if self.poolT.GetValue() == '':
            p = 0
        else:
            p = int(self.poolT.GetValue())
        if ifUndo:
            asyncio.run(s.undo(tID,p))
        else:
            asyncio.run(s.run(tID, p))

    #If config dropdown is opened, make a new ConfigWindow.
    def menuOpen(self, e):
        configW = ConfigWindow(None, "Config")
        configW.Show()

    # If undo buttton is pressed, run with True.
    def onUndo(self, e):
        self.Run(True)
        diagU = wx.MessageDialog(self, 'Undo complete!', 'Result', wx.OK)
        if diagU.ShowModal() == wx.OK:
            diagU.Close(True)

    # Create main window for the user to see.
    def InitUI(self):
        self.SetMaxSize(wx.Size(300,225))
        self.SetMinSize(wx.Size(300,225))
        self.SetInitialSize(wx.Size(300,225))
        menu = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_ANY, 'Setup', 'Set username and API key')
        menu.Append(fileMenu, '&Edit')
        self.Bind(wx.EVT_MENU, self.menuOpen, fileItem)
        self.SetMenuBar(menu)

        # Set up panel and containers.
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#cae8dd')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(3,2,9,25)

        # Input for tournament ID panel
        tourneyID = wx.StaticText(panel, label="Tournament ID")
        self.tT = wx.TextCtrl(panel)

        # Input for the # of pools.
        numPools = wx.StaticText(panel, label="# of Pools")
        self.poolT = wx.TextCtrl(panel)

        # Add those panels to the flex grid.
        fgs.AddMany([(tourneyID),(self.tT, 1, wx.EXPAND), (numPools),(self.poolT, 1,wx.EXPAND)])

        # Empty container.
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        vbox.Add(hbox0, flag=wx.ALIGN_CENTER, border=10)

        # Set up container for buttons and make
        # running button.
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        goBtn = wx.Button(panel, label='Run', size=(70,30))
        goBtn.Bind(wx.EVT_BUTTON, self.onButton)

        # Make undo button.
        undoBtn = wx.Button(panel,label='Undo', size=(70,30))
        undoBtn.Bind(wx.EVT_BUTTON, self.onUndo)

        # Add panels to bottom container and add to the
        # main container.
        hbox1.Add(goBtn, flag=wx.ALIGN_CENTER, border=5)
        hbox1.Add(undoBtn, flag=wx.ALIGN_CENTER, border=5)
        vbox.Add(hbox1, flag=wx.ALIGN_CENTER, border=10)

        panel.SetSizer(vbox)

        # Bar at the bottom.
        # I wanted to add error messages here,
        # but could not access the error messages
        # from achallonge correctly.
        self.statusBr = self.CreateStatusBar()
        self.statusBr.SetStatusText('')
        self.Centre()

# Run everything.
def main():
    app = wx.App()
    main = MainWindow(None,title="Auto Seeder")
    main.Show()
    app.MainLoop()