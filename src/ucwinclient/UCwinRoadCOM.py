import win32com.client as com

class UCwinRoadComProxy:
    PROG_ID = "UCwinRoad.UCwinRoadCom_1720"
    
    def __init__(self):
        print(self.PROG_ID)
        self.UCwinRoadCOM = com.gencache.EnsureDispatch(self.PROG_ID)
        self.ApplicationServices = self.UCwinRoadCOM.ApplicationServices
        self.Project = self.ApplicationServices.Project
        self.MainForm = self.ApplicationServices.MainForm
        self.SimulationCore = self.ApplicationServices.SimulationCore
        self.GazeTrackingPlugin = self.ApplicationServices.GazeTrackingPlugin
        self.CoordinateConverter = self.ApplicationServices.CoordinateConverter
        self.const = com.constants

    def __del__(self):
        self.UCwinRoadCOM = None
        self.ApplicationServices = None
        self.Project = None
        self.MainForm = None
        self.SimulationCore = None
        self.GazeTrackingPlugin = None
        self.CoordinateConverter = None

    def UserDirectory(self):
        return self.ApplicationServices.UserDirectory

    def PythonPluginDirectory(self):
        return self.ApplicationServices.UserDirectory + '/Plugins/PythonAPIPlugin/' 

