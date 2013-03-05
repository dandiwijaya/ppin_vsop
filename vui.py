#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
VUI.py

Created on 2011
Script VUI merupakan pengembangan VSOP User Interface (VUI) untuk aplikasi
VSOP (Very Superior Old Program) Untuk perhitungan desain/analisis
reaktor nuklir berpendingin gas.

@scripter: dandiwijaya
"""

import wx
import sys, os, time
import wx.aui
import inputEditor,inputdat
import birgit1Editor,birgit2Editor,birgit3Editor,birgit4Editor,birgit5Editor
import data1Editor, data2Editor, life1Editor
import vsop1Editor, vsop2Editor, vsop3Editor, vsop4Editor, vsop5Editor, vsop6Editor
import zut1Editor, zut2Editor
import shutil
from wx.lib.wordwrap import wordwrap


ID_NEW          = 100
ID_SAVE         = 101
ID_EXIT         = 102
ID_ABOUT        = 103

ID_READYINPUT   = 106
ID_READYINPUT   = 107
ID_VSOPRUN      = 108
ID_VSOPRUNSTEP  = 109
ID_OUTPUTDIR    = 110

ID_BIRGIT1      = 201
ID_BIRGIT2      = 202
ID_BIRGIT3      = 203
ID_BIRGIT4      = 204
ID_BIRGIT5      = 205
ID_DATA1        = 206
ID_DATA2        = 207
ID_LIFE1        = 208
ID_VSOP1        = 209
ID_VSOP2        = 210
ID_VSOP3        = 211
ID_VSOP4        = 212
ID_VSOP5        = 213
ID_VSOP6        = 214
ID_ZUT1         = 215
ID_ZUT2         = 216
ID_GAM          = 217
ID_THERMA       = 218
ID_TH_RES       = 219
ID_U_RES        = 220


class MainFrame(wx.Frame):

    def __init__(self, parent, id, title='VSOP User Interface',
                 pos=wx.DefaultPosition, size=(800, 600),
                 style=wx.DEFAULT_FRAME_STYLE, duration=2000):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        self.Maximize()
        self.Centre()
        self.CreateStatusBar()
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.SetStatusText("Welcome VUI Project!")

        self.filename=""
        self.dirname=""
        self.dirOut=""

        self.TH232File=""
        self.U232File=""
        self.GAMFile=""
        self.THERMAFile=""

        # pick a splash image file you have in the working folder
        image_file = 'batan.jpg'
        bmp = wx.Bitmap(image_file)
        # covers the parent frame
        wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_PARENT|wx.SPLASH_TIMEOUT,
            duration, parent, wx.ID_ANY)

        iconFile = "batan.ico"
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)

        self._mgr = wx.aui.AuiManager(self)

        filemenu= wx.Menu()
        filemenu.Append(ID_NEW, "&New"," New Calculation")
        filemenu.Append(ID_SAVE, "&Save"," Save Output File")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Exit the program")

        helpmenu = wx.Menu()
        helpmenu.Append(ID_ABOUT, "About This Program"," Information about this program")

        FourthJob = wx.Menu()
        FourthJob.Append(ID_DATA1, 'Create/Edit File DATA1.DAT')
        FourthJob.Append(ID_ZUT2, 'Create/Edit File ZUT2.DAT')

        FifthJob = wx.Menu()
        FifthJob.Append(ID_BIRGIT1, 'Create/Edit File BIRGIT1.DAT')
        FifthJob.Append(ID_VSOP1, 'Create/Edit File VSOP1.DAT')

        SeventhJob = wx.Menu()
        SeventhJob.Append(ID_BIRGIT3, 'Create/Edit Data File for geometric reactor design (BIRGIT3.DAT)')
        SeventhJob.Append(ID_DATA2, 'Create/Edit Data File for fuel element design (DATA2.DAT)')
        SeventhJob.Append(ID_VSOP2, 'Create/Edit Data File for startup core and equilibrium cycle of the 00 MW OTTO - pebble bed reactor (VSOP2.DAT)')

        EighthJob = wx.Menu()
        EighthJob.Append(ID_BIRGIT4, 'Create/Edit Data File BIRGIT4.DAT')
        EighthJob.Append(ID_VSOP3, ' Create/Edit Data File VSOP3.DAT')

        TwelfthJob = wx.Menu()
        TwelfthJob.Append(ID_BIRGIT5, 'Create/Edit Data File to restart: Time dependent thermal hydraulic loss of coolant accident (LOCA) (BIRGIT5.DAT)')
        TwelfthJob.Append(ID_VSOP5, 'Create/Edit Data File to restart: Time dependent thermal hydraulics loss of coolant accident (LOCA) (VSOP4.DAT)')


        LibMenu = wx.Menu()
        LibMenu.Append(ID_GAM, 'GAM-library (68 groups) given in ASCII (GAM.lib)')
        LibMenu.Append(ID_THERMA, 'THERMALIZATION-library (96 groups) given in ASCII (THERMA.lib)')

        ResMenu = wx.Menu()
        ResMenu.Append(ID_TH_RES, "Th-232 Resonance data (formatted)", "TH-232 Resonance Files")
        ResMenu.Append(ID_U_RES, "U-232 Resonance data (formatted)", "U-232 Resonance Files")

        ConfigMenu = wx.Menu()
        ConfigMenu.AppendMenu(wx.ID_ANY, "Select Library Data Files", LibMenu)
        ConfigMenu.AppendMenu(wx.ID_ANY, "Select Resonance Data Files",ResMenu)
        ConfigMenu.Append(ID_OUTPUTDIR, "Select the Directory for Output Files of VSOP Calculations", "Output Directory")

        CreateMenu = wx.Menu()
        CreateMenu.Append(ID_ZUT1, 'Create/Edit Data File to prepare UNIT 30 for the resonance absorption  X-sections (ZUT1.DAT)')
        CreateMenu.AppendMenu(wx.ID_ANY, "Create/Edit Data File toCalculate resonance integrals", FourthJob)
        CreateMenu.AppendMenu(wx.ID_ANY, "Create/Edit Data File toPrepare a 30 group THERMOS-lib", FifthJob)
        CreateMenu.Append(ID_BIRGIT2, 'Create/Edit Data File to create the volume matrix (BIRGIT2.DAT)')
        CreateMenu.AppendMenu(wx.ID_ANY, "Create/Edit Data File to Geometric reactor design", SeventhJob)
        CreateMenu.AppendMenu(wx.ID_ANY, "Create/Edit Data File to Restart OTTO case with 2-D. Thermalhydraulics (steady state)", EighthJob)
        CreateMenu.Append(ID_VSOP4, 'Create/Edit Data File to restart: Calculation of temperature coefficients (VSOP4.DAT)')
        CreateMenu.Append(ID_VSOP5, 'Create/Edit Data File to restart: Lib. for LIFE (life history of the fuel elements) (VSOP4.DAT)')
        CreateMenu.Append(ID_LIFE1, 'Create/Edit Data File to compile fuel life history for decay power evaluation (LIFE1.DAT)')
        CreateMenu.AppendMenu(wx.ID_ANY, "Create/Edit Data File to Restart: Time dependent thermal hydraulic loss of coolant accident (LOCA)", TwelfthJob)

        InputMenu = wx.Menu()
        InputMenu.Append(ID_READYINPUT, "Enter the ready VSOP input file", "Ready VSOP Input File")
        InputMenu.AppendMenu(wx.ID_ANY, "Create/Edit VSOP input file", CreateMenu )

        RunMenu = wx.Menu()
        RunMenu.Append(ID_VSOPRUN,"Run VSOP All at Once","Execute VSOP Calculation")
        RunMenu.Append(ID_VSOPRUNSTEP,"Run VSOP step by step","Execute VSOP Calculation")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(ConfigMenu,"VSOP Configuration")
        menuBar.Append(InputMenu,"VSOP Input File")
        menuBar.Append(RunMenu,"VSOP Run")
        menuBar.Append(helpmenu,"&About")

        self.SetMenuBar(menuBar)


        wx.EVT_MENU(self, ID_NEW, self.OnFileNew)
        wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)

        wx.EVT_MENU(self, ID_OUTPUTDIR, self.OnOpenOutDir)
        wx.EVT_MENU(self, ID_TH_RES, self.OnOpenTH232RES)
        wx.EVT_MENU(self, ID_U_RES, self.OnOpenU232RES)
        wx.EVT_MENU(self, ID_GAM, self.OnOpenGAMLIB)
        wx.EVT_MENU(self, ID_THERMA, self.OnOpenTHERMALIB)

        wx.EVT_MENU(self, ID_READYINPUT, self.OnReadyInput)
        wx.EVT_MENU(self, ID_VSOPRUNSTEP, self.OnVSOPRunStep)
        wx.EVT_MENU(self, ID_VSOPRUN, self.OnVSOPRun)

        # Open text editor for create/edit VSOP input file
        wx.EVT_MENU(self, ID_BIRGIT1, self.OnBIRGIT1Editor)
        wx.EVT_MENU(self, ID_BIRGIT2, self.OnBIRGIT2Editor)
        wx.EVT_MENU(self, ID_BIRGIT3, self.OnBIRGIT3Editor)
        wx.EVT_MENU(self, ID_BIRGIT4, self.OnBIRGIT4Editor)
        wx.EVT_MENU(self, ID_BIRGIT5, self.OnBIRGIT5Editor)
        wx.EVT_MENU(self, ID_DATA1, self.OnDATA1Editor)
        wx.EVT_MENU(self, ID_DATA2, self.OnDATA2Editor)
        wx.EVT_MENU(self, ID_LIFE1, self.OnLIFE1Editor)
        wx.EVT_MENU(self, ID_VSOP1, self.OnVSOP1Editor)
        wx.EVT_MENU(self, ID_VSOP2, self.OnVSOP2Editor)
        wx.EVT_MENU(self, ID_VSOP3, self.OnVSOP3Editor)
        wx.EVT_MENU(self, ID_VSOP4, self.OnVSOP4Editor)
        wx.EVT_MENU(self, ID_VSOP5, self.OnVSOP5Editor)
        wx.EVT_MENU(self, ID_VSOP6, self.OnVSOP6Editor)
        wx.EVT_MENU(self, ID_ZUT1, self.OnZUT1Editor)
        wx.EVT_MENU(self, ID_ZUT2, self.OnZUT2Editor)

        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)


        self.logger = wx.TextCtrl(self, -1, ('create new calculation at %s \n \n' % str(time.ctime())),
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE |  wx.TE_READONLY)

        self.compProcess = wx.TextCtrl(self, -1, 'VSOP (Very Superior Old Program) Running Process \n \n',
                            wx.DefaultPosition, wx.Size(500,150),
                            wx.NO_BORDER | wx.TE_MULTILINE |  wx.TE_READONLY)

        self.compOut = wx.TextCtrl(self, -1, 'View Output Files \n \n',
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE |  wx.TE_READONLY)

        # add the panes to the manager
        self._mgr.AddPane(self.logger, wx.BOTTOM, 'Activity Log')
        self._mgr.AddPane(self.compProcess, wx.RIGHT, 'Computing Process')
        self._mgr.AddPane(self.compOut, wx.CENTER, 'View Output Files')
        self._mgr.Update()

        self.progress = wx.Gauge(self, range=100, size=(300, 30))
        self.progress.SetValue(0)
        self.progress.Centre()
        self.progress.Hide()

####################
###  Bagian Menu ###
####################
    def OnFileNew(self,evt):
        self.compOut.Clear()
        self.compOut.AppendText('View Output Files \n \n')
        self.compProcess.Clear()
        self.compProcess.AppendText('VSOP (Very Superior Old Program) \n')
        self.logger.Clear()
        self.compProcess.SetBackgroundColour("White")
        self.compOut.SetBackgroundColour("White")
        self.logger.SetBackgroundColour("White")
        self.logger.AppendText('>>> create new calculation at %s \n \n' % str(time.ctime()))

        try:
            # remove .exe files
            os.remove(self.dirOut+'\\atlas.exe')
            os.remove(self.dirOut+'\\birgit.exe')
            os.remove(self.dirOut+'\\congam.exe')
            os.remove(self.dirOut+'\\contherma.exe')
            os.remove(self.dirOut+'\\data2.exe')
            os.remove(self.dirOut+'\\life.exe')
            os.remove(self.dirOut+'\\prior.exe')
            os.remove(self.dirOut+'\\trigit.exe')
            os.remove(self.dirOut+'\\vsop.exe')
            os.remove(self.dirOut+'\\zut.exe')

            # remove JOB .jcl files
            os.remove(self.dirOut+'\\1.jcl')
            os.remove(self.dirOut+'\\2.jcl')
            os.remove(self.dirOut+'\\3.jcl')
            os.remove(self.dirOut+'\\41.jcl')
            os.remove(self.dirOut+'\\42.jcl')
            os.remove(self.dirOut+'\\51.jcl')
            os.remove(self.dirOut+'\\52.jcl')
            os.remove(self.dirOut+'\\6.jcl')
            os.remove(self.dirOut+'\\71.jcl')
            os.remove(self.dirOut+'\\72.jcl')
            os.remove(self.dirOut+'\\73.jcl')
            os.remove(self.dirOut+'\\81.jcl')
            os.remove(self.dirOut+'\\82.jcl')
            os.remove(self.dirOut+'\\9.jcl')
            os.remove(self.dirOut+'\\10.jcl')
            os.remove(self.dirOut+'\\11.jcl')
            os.remove(self.dirOut+'\\121.jcl')
            os.remove(self.dirOut+'\\122.jcl')

            # remove DATA .JCL files
            os.remove(self.dirOut+'\\ATLAS.JCL')
            os.remove(self.dirOut+'\\BIRGIT5.JCL')
            os.remove(self.dirOut+'\\BIRGIT6.JCL')
            os.remove(self.dirOut+'\\BIRGIT7.JCL')
            os.remove(self.dirOut+'\\BIRGIT8.JCL')
            os.remove(self.dirOut+'\\BIRGIT12.JCL')
            os.remove(self.dirOut+'\\CONGAM.JCL')
            os.remove(self.dirOut+'\\CONTHERMA.JCL')
            os.remove(self.dirOut+'\\DATA24.JCL')
            os.remove(self.dirOut+'\\DATA27.JCL')
            os.remove(self.dirOut+'\\LIFE11.JCL')
            os.remove(self.dirOut+'\\PRIOR.JCL')
            os.remove(self.dirOut+'\\TRIGIT.JCL')
            os.remove(self.dirOut+'\\VSOP5.JCL')
            os.remove(self.dirOut+'\\VSOP7.JCL')
            os.remove(self.dirOut+'\\VSOP8.JCL')
            os.remove(self.dirOut+'\\VSOP9.JCL')
            os.remove(self.dirOut+'\\VSOP10.JCL')
            os.remove(self.dirOut+'\\VSOP12.JCL')
            os.remove(self.dirOut+'\\ZUT3.JCL')
            os.remove(self.dirOut+'\\ZUT4.JCL')

            os.remove(self.dirOut+'\\fort.1')
            os.remove(self.dirOut+'\\fort.2')
            os.remove(self.dirOut+'\\fort.4')
            os.remove(self.dirOut+'\\fort.8')
            os.remove(self.dirOut+'\\fort.9')
            os.remove(self.dirOut+'\\fort.10')
            os.remove(self.dirOut+'\\fort.11')
            os.remove(self.dirOut+'\\fort.13')
            os.remove(self.dirOut+'\\fort.19')
            os.remove(self.dirOut+'\\fort.21')
            os.remove(self.dirOut+'\\fort.22')
            os.remove(self.dirOut+'\\fort.24')
            os.remove(self.dirOut+'\\fort.25')
            os.remove(self.dirOut+'\\fort.28')
            os.remove(self.dirOut+'\\fort.29')
            os.remove(self.dirOut+'\\fort.30')
            os.remove(self.dirOut+'\\fort.32')
            os.remove(self.dirOut+'\\fort.33')
            os.remove(self.dirOut+'\\fort.34')
            os.remove(self.dirOut+'\\fort.35')
            os.remove(self.dirOut+'\\fort.36')
            os.remove(self.dirOut+'\\fort.37')
            os.remove(self.dirOut+'\\fort.38')
            os.remove(self.dirOut+'\\fort.42')
            os.remove(self.dirOut+'\\fort.43')
            os.remove(self.dirOut+'\\fort.51')
            os.remove(self.dirOut+'\\fort.55')
            os.remove(self.dirOut+'\\fort.56')
            os.remove(self.dirOut+'\\fort.58')
            os.remove(self.dirOut+'\\fort.59')
            os.remove(self.dirOut+'\\fort.60')
            os.remove(self.dirOut+'\\fort.61')
            os.remove(self.dirOut+'\\fort.62')

            # remove bin files
            os.remove(self.dirOut+'\\gam.bin')
            os.remove(self.dirOut+'\\therma.bin')
            os.remove(self.dirOut+'\\thermos.bin')

            # remove .DAT files
            os.remove(self.dirOut+'\\ottou15.DAT')
            os.remove(self.dirOut+'\\ottovm.DAT')

            # remove dummy files
            os.remove(self.dirOut+'\\dummy16')
            os.remove(self.dirOut+'\\dummy17')
            os.remove(self.dirOut+'\\dummy18')
            os.remove(self.dirOut+'\\dummy20')

        except:
            return

    def OnSave(self,event):
        dlg = wx.FileDialog(self, "Save Output file ", self.dirOut, "", "Out File|*.out|All Files|*.*", \
                wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            itcontains = self.compOut.GetValue()
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'w')
            filehandle.write(itcontains)
            filehandle.close()
        dlg.Destroy()

    def onButton(self, evt):
        self.btn.Enable(False)
        self.gauge.SetValue(0)
        self.label.SetLabel("Running")

    def OnExit(self,e):
        """Exit Program"""
        dlg = wx.MessageDialog(self,
            "Do you really want to exit VUI?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
            sys.exit()
        else:
            return

    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
            "Do you really want to close this session?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.compProcess.Clear()
            self.compProcess.SetBackgroundColour("Grey")
            self.SetTitle("VSOP (Very Superior Old Program) User Interface Project")
        else:
            return

    def OnAbout(self,e):
        info = wx.AboutDialogInfo()
        info.Name = "VSOP (Very Superior Old Program) User Interface Project"
        info.Version = "v.0.0.0"
        info.Copyright = "(C) copyfight 2011"
        info.Description = wordwrap(
"""
VSOP User Interface (VUI) Project Version 0.0 for Windows - Release Notes


1. VSOP Project User Interface is a software-based development program VSOP (Very Superior Old Program)-94 is modified by Ilham Putranto Yazid.

2. VUI was developed to facilitate the use of GUI(Graphicalical User Interface)-based applications of VSOP-94 

3. VUI applications,  is still needed further development to meet the needs of users, therefore for any suggestions, ideas, criticisms,
   or report any problems in using this applications, please contact me at dinan@batan.go.id


We wish you enjoy this software.

D. Andiwijayakusuma""",
        500, wx.ClientDC(self))
        info.WebSite = ("http://komputasi.batan.go.id/","VUI project homepage")
        info.Developers = [
"""Computational Division
Centre of Nuclear Informatic Development
National Nuclear Energy Agency (BATAN)"""]
        info.License = "General Public Lisence"
        wx.AboutBox(info)


############################
###     Bagian Config    ###
############################

    def OnOpenTH232RES(self,e):
        dlg=wx.FileDialog(self,"Open TH-232.RES File",self.dirname,self.filename,"Resources Files|*.RES",wx.OPEN)
        if(dlg.ShowModal()==wx.ID_OK):
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            self.TH232File=dirname+'\\'+filename
            self.logger.AppendText('>>> %s  | TH-232.RES has been selected \n \n' % str(time.ctime()))
        else :
            dlg.Destroy()

    def OnOpenU232RES(self,e):
        dlg=wx.FileDialog(self,"Open U-238.RES File",self.dirname,self.filename,"Resources Files|*.RES",wx.OPEN)
        if(dlg.ShowModal()==wx.ID_OK):
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            self.U232File=dirname+'\\'+filename
            self.logger.AppendText('>>> %s  | The U-238.RES has been selected \n \n' % (str(time.ctime())))
        else:
            dlg.Destroy()

    def OnOpenGAMLIB(self,e):
        dlg=wx.FileDialog(self,"Open GAM.LIB File",self.dirname,self.filename,"Library Files|*.LIB",wx.OPEN)
        if(dlg.ShowModal()==wx.ID_OK):
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            self.GAMFile=dirname+'\\'+filename
            self.logger.AppendText('>>> %s  | The GAM.LIB File has been selected \n \n' % (str(time.ctime())))
        else:
            dlg.Destroy()

    def OnOpenTHERMALIB(self,e):
        dlg=wx.FileDialog(self,"Open THERMA.LIB File",self.dirname,self.filename,"Library Files|*.LIB",wx.OPEN)
        if(dlg.ShowModal()==wx.ID_OK):
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            self.THERMAFile=dirname+'\\'+filename
            self.logger.AppendText('>>> %s  | The THERMA.LIB File has been selected \n \n' % (str(time.ctime())))
        else:
            dlg.Destroy()

    def OnOpenOutDir(self,e,buffer_size=1024*1024):
        if self.TH232File=="" or self.U232File == "" or self.GAMFile=="" or self.THERMAFile=="" :
            dlgWarning=wx.MessageDialog(self,"Please Select the Resource(.RES) and Library(.LIB) file first","Warning ",wx.OK|wx.ICON_INFORMATION)
            dlgWarning.ShowModal()
            dlgWarning.Destroy()
        else:
            dlg = wx.DirDialog(self, "Please Select the Directory for Output file", self.dirOut, wx.OPEN)
            if dlg.ShowModal()==wx.ID_OK:
                self.dirOut=dlg.GetPath()
                self.logger.AppendText('>>> %s  |  Select the Directory for Output file \n \n' % str(time.ctime()))
                # Copying .RES and .LIB Files #
                try:
                    shutil.copy2(self.TH232File,(self.dirOut+'\\TH-232.RES'))
                    shutil.copy2(self.U232File,(self.dirOut+'\\U-238.RES'))
                    shutil.copy2(self.GAMFile,(self.dirOut+'\\GAM.LIB'))
                    shutil.copy2(self.THERMAFile,(self.dirOut+'\\THERMA.LIB'))
                    self.logger.AppendText('>>> %s  | The Resource(.RES) and Library(.LIB) files has been copied to the output directory \n \n' % (str(time.ctime())))

                    # copy exe files
                    shutil.copy2((os.getcwd()+'\\VSOP94\\atlas.exe'),(self.dirOut+'\\atlas.exe'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\birgit.exe'),(self.dirOut+'\\birgit.exe'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\congam.exe'),(self.dirOut+'\\congam.exe'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\contherma.exe'),(self.dirOut+'\\contherma.exe'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\data2.exe'),(self.dirOut+'\\data2.exe'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\life.exe'),(self.dirOut+'\\life.exe'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\prior.exe'),(self.dirOut+'\\prior.exe'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\trigit.exe'),(self.dirOut+'\\trigit.exe'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\vsop.exe'),(self.dirOut+'\\vsop.exe'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\zut.exe'),(self.dirOut+'\\zut.exe'))

                    # copy jcl files
                    shutil.copy2((os.getcwd()+'\\VSOP94\\1.jcl'),(self.dirOut+'\\1.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\2.jcl'),(self.dirOut+'\\2.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\3.jcl'),(self.dirOut+'\\3.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\41.jcl'),(self.dirOut+'\\41.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\42.jcl'),(self.dirOut+'\\42.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\51.jcl'),(self.dirOut+'\\51.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\52.jcl'),(self.dirOut+'\\52.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\6.jcl'),(self.dirOut+'\\6.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\71.jcl'),(self.dirOut+'\\71.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\72.jcl'),(self.dirOut+'\\72.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\73.jcl'),(self.dirOut+'\\73.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\81.jcl'),(self.dirOut+'\\81.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\82.jcl'),(self.dirOut+'\\82.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\9.jcl'),(self.dirOut+'\\9.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\10.jcl'),(self.dirOut+'\\10.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\11.jcl'),(self.dirOut+'\\11.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\121.jcl'),(self.dirOut+'\\121.jcl'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\122.jcl'),(self.dirOut+'\\122.jcl'))

                    # copy JCL files
                    shutil.copy2((os.getcwd()+'\\VSOP94\\ATLAS.JCL'),(self.dirOut+'\\ATLAS.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\BIRGIT5.JCL'),(self.dirOut+'\\BIRGIT5.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\BIRGIT6.JCL'),(self.dirOut+'\\BIRGIT6.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\BIRGIT7.JCL'),(self.dirOut+'\\BIRGIT7.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\BIRGIT8.JCL'),(self.dirOut+'\\BIRGIT8.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\BIRGIT12.JCL'),(self.dirOut+'\\BIRGIT12.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\CONGAM.JCL'),(self.dirOut+'\\CONGAM.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\CONTHERMA.JCL'),(self.dirOut+'\\CONTHERMA.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\DATA24.JCL'),(self.dirOut+'\\DATA24.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\DATA27.JCL'),(self.dirOut+'\\DATA27.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\LIFE11.JCL'),(self.dirOut+'\\LIFE11.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\PRIOR.JCL'),(self.dirOut+'\\PRIOR.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\TRIGIT.JCL'),(self.dirOut+'\\TRIGIT.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\VSOP5.JCL'),(self.dirOut+'\\VSOP5.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\VSOP7.JCL'),(self.dirOut+'\\VSOP7.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\VSOP8.JCL'),(self.dirOut+'\\VSOP8.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\VSOP9.JCL'),(self.dirOut+'\\VSOP9.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\VSOP10.JCL'),(self.dirOut+'\\VSOP10.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\VSOP12.JCL'),(self.dirOut+'\\VSOP12.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\ZUT3.JCL'),(self.dirOut+'\\ZUT3.JCL'))
                    shutil.copy2((os.getcwd()+'\\VSOP94\\ZUT4.JCL'),(self.dirOut+'\\ZUT4.JCL'))

                except:
                    dlgWarning=wx.MessageDialog(self,"Please Select the Resource(.RES) and Library(.LIB) file first","Warning ",wx.OK|wx.ICON_INFORMATION)
                    dlgWarning.ShowModal()


############################
###  Bagian Input File   ###
############################
    def OnReadyInput(self,e):
        if self.dirOut=="" :
            dlgWarning=wx.MessageDialog(self,"Please Select the Directory for Output File First on VSOP Configuration","Warning ",wx.OK|wx.ICON_INFORMATION)
            dlgWarning.ShowModal()
            dlgWarning.Destroy()
        else:
            frame=inputdat.MainWindow(None,-1, "Enter ready VSOP Input File", self.dirOut)
            self.logger.AppendText('>>> %s  |  Enter ready VSOP Input file \n \n' % str(time.ctime()))
            frame.CenterOnScreen()
            frame.Show(True)
            #self.logger.AppendText('>>> %s  | The .DAT input files has been selected and copied to the output directory \n \n' % (str(time.ctime())))

    def OnTextInput(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit VSOP Preprocessor input file by text editor \n \n' % str(time.ctime()))
        frame=inputEditor.MainWindow(None,-1, "VSOP Preprocessor Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnBIRGIT1Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit BIRGIT1.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=birgit1Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnBIRGIT2Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit BIRGIT2.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=birgit2Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnBIRGIT3Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit BIRGIT3.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=birgit3Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnBIRGIT4Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit BIRGIT4.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=birgit4Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnBIRGIT5Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit BIRGIT5.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=birgit5Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnDATA1Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit DATA1.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=data1Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnDATA2Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit DATA2.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=data2Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnLIFE1Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit LIFE1.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=life1Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnVSOP1Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit VSOP1.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=vsop1Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnVSOP2Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit VSOP2.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=vsop2Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnVSOP3Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit VSOP3.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=vsop3Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnVSOP4Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit VSOP4.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=vsop4Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnVSOP5Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit VSOP5.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=vsop5Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnVSOP6Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit VSOP6.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=vsop6Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnZUT1Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit ZUT1.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=zut1Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)

    def OnZUT2Editor(self,e):
        self.logger.AppendText('>>> %s  |  Create / Edit ZUT2.DAT for VSOP input file by text editor \n \n' % str(time.ctime()))
        frame=zut2Editor.MainWindow(None,-1, "VSOP Input Editor", self.dirOut)
        frame.CenterOnScreen()
        frame.Show(True)


############################
###     Bagian Running   ###
############################
    def OnVSOPRunStep(self,e):
        if self.dirOut=="" :
            dlgWarning=wx.MessageDialog(self,"Please Select the Directory for Output File First on VSOP Configuration","Warning ",wx.OK|wx.ICON_INFORMATION)
            dlgWarning.ShowModal()
            dlgWarning.Destroy()
        else:
            os.chdir(self.dirOut)
            if (os.path.exists('BIRGIT1.DAT')== False or os.path.exists('BIRGIT2.DAT')== False or os.path.exists('BIRGIT3.DAT')== False or
                os.path.exists('BIRGIT4.DAT')== False or os.path.exists('BIRGIT5.DAT')== False or os.path.exists('Data1.DAT')== False or
                os.path.exists('Data2.DAT')== False or os.path.exists('Life1.DAT')== False or os.path.exists('Vsop1.DAT')== False or
                os.path.exists('Vsop2.DAT')== False or os.path.exists('Vsop3.DAT')== False or os.path.exists('Vsop4.DAT')== False or
                os.path.exists('Vsop5.DAT')== False or os.path.exists('Vsop6.DAT')== False or os.path.exists('zut1.DAT')== False or
                os.path.exists('zut2.DAT')== False) :

                dlgWarning=wx.MessageDialog(self,"Indicated input file. DAT are not met, please complete it first \n"
                                        "Do you to continue this process?","Warning ",wx.YES|wx.NO|wx.ICON_QUESTION)
                result = dlgWarning.ShowModal()
                dlgWarning.Destroy()

                if result == wx.ID_YES:
                    self.logger.AppendText('>>> %s  | <<< VSOP Running >>> \n \n' % str(time.ctime()))
                    arJob=['FIRST JOB','SECOND JOB','THIRD JOB', 'FOURTH JOB (first step)',
                           'FOURTH JOB (second step)', 'FIFTH JOB (first step)',
                           'FIFTH JOB (second step)', 'SIXTH JOB', 'SEVENTH JOB (first step)',
                           'SEVENTH JOB (second step)', 'SEVENTH JOB (third step)',
                           'EIGHTH JOB (first step)', 'EIGHTH JOB (second step)',
                           'NINTH JOB', 'TENTH JOB', 'ELEVENTH JOB', 'TWELFTH JOB (first step)',
                           'TWELFTH JOB (second step)']

                    arCommand=['congam.exe<1.jcl', 'contherma.exe<2.jcl', 'zut.exe<3.jcl',
                               'data2.exe<41.jcl' ,'zut.exe<42.jcl','birgit.exe<51.jcl',
                               'vsop.exe<52.jcl', 'birgit.exe<6.jcl','birgit.exe<71.jcl',
                               'data2.exe<72.jcl','vsop.exe<73.jcl','birgit.exe<81.jcl',
                               'vsop.exe<82.jcl','vsop.exe<9.jcl','vsop.exe<10.jcl',
                               'life.exe<11.jcl','birgit.exe<121.jcl','vsop.exe<122.jcl']
                    for i in range (0,18):
                        dlg = wx.MessageDialog(self,
                        "Click OK to continue job or Cancel to terminate","Confirm Job Execution", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
                        result = dlg.ShowModal()
                        dlg.Destroy()
                        if result == wx.ID_OK:
                            self.logger.AppendText('>>> %s  |  VSOP Running, Execute %s \n \n' % (str(time.ctime()), arJob[i]))
                            processView(self,arJob[i],arCommand[i])
                        else :
                            return

                    dlgResult=wx.MessageDialog(self,"Calculation Done","Information",wx.OK|wx.ICON_INFORMATION)
                    dlgResult.ShowModal()
                    dlgResult.Destroy()
                    self.SetStatusText("Calculation Done")
                    return

                else:
                    return

            else:
                self.logger.AppendText('>>> %s  | <<< VSOP Running >>> \n \n' % str(time.ctime()))
                arJob=['FIRST JOB','SECOND JOB','THIRD JOB', 'FOURTH JOB (first step)',
                       'FOURTH JOB (second step)', 'FIFTH JOB (first step)',
                       'FIFTH JOB (second step)', 'SIXTH JOB', 'SEVENTH JOB (first step)',
                       'SEVENTH JOB (second step)', 'SEVENTH JOB (third step)',
                       'EIGHTH JOB (first step)', 'EIGHTH JOB (second step)',
                       'NINTH JOB', 'TENTH JOB', 'ELEVENTH JOB', 'TWELFTH JOB (first step)',
                       'TWELFTH JOB (second step)']

                arCommand=['congam.exe<1.jcl', 'contherma.exe<2.jcl', 'zut.exe<3.jcl',
                           'data2.exe<41.jcl' ,'zut.exe<42.jcl','birgit.exe<51.jcl',
                           'vsop.exe<52.jcl', 'birgit.exe<6.jcl','birgit.exe<71.jcl',
                           'data2.exe<72.jcl','vsop.exe<73.jcl','birgit.exe<81.jcl',
                           'vsop.exe<82.jcl','vsop.exe<9.jcl','vsop.exe<10.jcl',
                           'life.exe<11.jcl','birgit.exe<121.jcl','vsop.exe<122.jcl']
                for i in range (0,18):
                    dlg = wx.MessageDialog(self,
                    "Click OK to continue job or Cancel to terminate","Confirm Job Execution", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
                    result = dlg.ShowModal()
                    dlg.Destroy()
                    if result == wx.ID_OK:
                        self.logger.AppendText('>>> %s  |  VSOP Running, Execute %s \n \n' % (str(time.ctime()), arJob[i]))
                        processView(self,arJob[i],arCommand[i])
                    else :
                        return

                dlgResult=wx.MessageDialog(self,"Calculation Done","Information",wx.OK|wx.ICON_INFORMATION)
                dlgResult.ShowModal()
                dlgResult.Destroy()
                self.SetStatusText("Calculation Done")
                return

    def OnVSOPRun(self,e):
        arJob=['FIRST JOB','SECOND JOB','THIRD JOB', 'FOURTH JOB (first step)',
               'FOURTH JOB (second step)', 'FIFTH JOB (first step)',
               'FIFTH JOB (second step)', 'SIXTH JOB', 'SEVENTH JOB (first step)',
               'SEVENTH JOB (second step)', 'SEVENTH JOB (third step)',
               'EIGHTH JOB (first step)', 'EIGHTH JOB (second step)',
               'NINTH JOB', 'TENTH JOB', 'ELEVENTH JOB', 'TWELFTH JOB (first step)',
               'TWELFTH JOB (second step)']

        arCommand=['congam.exe<1.jcl', 'contherma.exe<2.jcl', 'zut.exe<3.jcl',
                   'data2.exe<41.jcl' ,'zut.exe<42.jcl','birgit.exe<51.jcl',
                   'vsop.exe<52.jcl', 'birgit.exe<6.jcl','birgit.exe<71.jcl',
                   'data2.exe<72.jcl','vsop.exe<73.jcl','birgit.exe<81.jcl',
                   'vsop.exe<82.jcl','vsop.exe<9.jcl','vsop.exe<10.jcl',
                   'life.exe<11.jcl','birgit.exe<121.jcl','vsop.exe<122.jcl']
        if self.dirOut=="" :
            dlgWarning=wx.MessageDialog(self,"Please Select the Directory for Output File First on VSOP Configuration","Warning ",wx.OK|wx.ICON_INFORMATION)
            dlgWarning.ShowModal()
            dlgWarning.Destroy()
        else:
            os.chdir(self.dirOut)
            if (os.path.exists('BIRGIT1.DAT')== False or os.path.exists('BIRGIT2.DAT')== False or os.path.exists('BIRGIT3.DAT')== False or
                os.path.exists('BIRGIT4.DAT')== False or os.path.exists('BIRGIT5.DAT')== False or os.path.exists('Data1.DAT')== False or
                os.path.exists('Data2.DAT')== False or os.path.exists('Life1.DAT')== False or os.path.exists('Vsop1.DAT')== False or
                os.path.exists('Vsop2.DAT')== False or os.path.exists('Vsop3.DAT')== False or os.path.exists('Vsop4.DAT')== False or
                os.path.exists('Vsop5.DAT')== False or os.path.exists('Vsop6.DAT')== False or os.path.exists('zut1.DAT')== False or
                os.path.exists('zut2.DAT')== False) :
                dlgWarning=wx.MessageDialog(self,"Indicated input file. DAT are not met, please complete it first \n"
                                        "Do you to continue this process?","Warning ",wx.YES|wx.NO|wx.ICON_QUESTION)
                result = dlgWarning.ShowModal()
                dlgWarning.Destroy()

                if result == wx.ID_YES:
                    self.logger.AppendText('>>> %s  | <<< VSOP Running >>> \n \n' % str(time.ctime()))


                    for i in range (0,18):
                        self.logger.AppendText('>>> %s  |  VSOP Running, Execute %s \n \n' % (str(time.ctime()), arJob[i]))
                        processView(self,arJob[i],arCommand[i])

                    dlgResult=wx.MessageDialog(self,"Calculation Done","Information",wx.OK|wx.ICON_INFORMATION)
                    dlgResult.ShowModal()
                    dlgResult.Destroy()
                    self.SetStatusText("Calculation Done")
                    return

                else:
                    return
            else:
                self.logger.AppendText('>>> %s  | <<< VSOP Running >>> \n \n' % str(time.ctime()))
                for i in range (0,18):
                    self.logger.AppendText('>>> %s  |  VSOP Running, Execute %s \n \n' % (str(time.ctime()), arJob[i]))
                    processView(self,arJob[i],arCommand[i])

                dlgResult=wx.MessageDialog(self,"Calculation Done","Information",wx.OK|wx.ICON_INFORMATION)
                dlgResult.ShowModal()
                dlgResult.Destroy()
                self.SetStatusText("Calculation Done")
                return

def processView(self,job,command):
    os.chdir(self.dirOut)
    border = '='*47
    self.compProcess.AppendText(border +'\n')
    self.compProcess.AppendText('Executing '+job+' ...\n')
    self.compProcess.AppendText(border +'\n')

    t0 = time.time()
    process = os.popen(command)
    self.compOut.AppendText('\n'+border+'\n')
    self.compOut.AppendText('                                                           <<< %s >>>\n' % job)
    self.compOut.AppendText(border+'\n \n')
    for line in process.readlines():
        self.compOut.Refresh()
        self.compOut.AppendText('                           ')
        self.compOut.AppendText(line)
        self.compOut.Refresh()
    delta = (time.time() - t0)
    if delta < 60.000:
        self.compProcess.AppendText('The '+job +' is COMPLETED in %.3f' % delta +' second \n')
    else:
        exec_time = time.strftime('%M Minutes %S Second', time.gmtime(delta))
        self.compProcess.AppendText('The '+job +' is COMPLETED in '+ exec_time+'\n')
    self.compProcess.AppendText(border +'\n \n')

app = wx.App()
frame = MainFrame(None, -1, "VSOP94 User Interface")
frame.Show()
app.MainLoop()
