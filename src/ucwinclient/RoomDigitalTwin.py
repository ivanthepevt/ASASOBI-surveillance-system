import threading
from UCwinRoadCOM import *
from LoggerProxy import LoggerProxy
import win32com.client as com
import time
import json
import websocket

from UCwinRoadUtils import *

def PlaceObj(data):
    global winRoadProxy
    prj = winRoadProxy.Project
    const = winRoadProxy.const
    modelcount = prj.ThreeDModelsCount
    found = False
    for i in range(modelcount):
        model = prj.ThreeDModel(i)
        if data['type'] == "person":
            if model.ModelType == const._CharacterModel:
                found = True
                break
        elif data['type'] == "car":
            if model.ModelType == const._VehicleModel and model.Name == "SmallCarBlue":
                found = True
                break

    if (not found) and (model is None) :
        logProxy.logger.info('Model is not found.')
        return

    traffic = winRoadProxy.SimulationCore.TrafficSimulation
    obj = traffic.AddNewTransient(model)
    logProxy.logger.info(f"Added new obj ID: {data['id']}")

    return obj

ID_TO_OBJMAP = {}
OFFSET_X = 5000
OFFSET_Y = 5000
OFFSET_Z = 550

def PerformAction(ws, jsonData):
    jsonData = json.loads(jsonData)

    for item in jsonData['data']:
        id = item['id']

        if id not in ID_TO_OBJMAP.keys():
            # create new obj in UC-win/Road here
            # save its IF8TransientMovingInstanceProxy to the dictionary
            ID_TO_OBJMAP[id] = PlaceObj(item)

        obj = ID_TO_OBJMAP[id]

        if obj is not None:
            logProxy.logger.info(f"Obj #{id} ({obj.Name}) last pos = {ToStrF8COMdVec3(obj.Position)}")
            nx, nz = OFFSET_X + item['position']['x'], OFFSET_Y + item['position']['y']

            obj.Position = AsF8COMdVec3(nx, OFFSET_Z, nz)

            logProxy.logger.info(f"Obj #{id} moved to ({ToStrF8COMdVec3(obj.Position)})")
        else:
            logProxy.logger.info(f"Obj #{id} not found")

class RibbonButtonHandler:
    def SetCOMEventClass(self, events):
        self.events = events
    def OnIsExistEventHandler(self, funcname):
        try:
            func = getattr(self.events, funcname)
        except AttributeError:
            return False
        return True
    def OnClick(self):
        print("OnClick")

# thread flag
WebSocketConnected = threading.Event()
WS_URI = "ws://localhost:8765"

def WsLogError(ws, error):
    global logProxy
    logProxy.logger.error(f"Error occured: {error}")

def RunWsThread():
    websocket.enableTrace(True)
    global wsApp
    wsApp = websocket.WebSocketApp(WS_URI,
                                on_message=PerformAction,
                                on_error=WsLogError)
    
    wsApp.run_forever()

class BtnConnectHandler(RibbonButtonHandler):
    def OnClick(self):
        if WebSocketConnected.is_set():
            return
        
        WebSocketConnected.set()

        global wsThread
        wsThread = threading.Thread(target=RunWsThread)
        wsThread.start()

class BtnDisconnectHandler(RibbonButtonHandler):
    def OnClick(self):
        WebSocketConnected.clear()
        wsApp.close()
        wsThread.join()
        logProxy.logger.info(f'Disconnected websocket {WS_URI}')
            
class RibbonUI:
    def __init__(self) -> None:
        self.EventList = []

    def MakeRibbonTab(self, Parent, partsName, caption):
        if Parent is not None:
            tab = Parent.GetTabByName(partsName)
            if tab is None:
                tab = Parent.CreateTab(partsName, 10000)
                tab.Caption = caption
            return tab

    def MakeRibbonGroup(self, Parent, partsName, caption):
        if Parent is not None:
            group = Parent.GetGroupByName(partsName)
            if group is None:
                group = Parent.CreateGroup(partsName, 100)
                group.Caption = caption
            return group
    
    def MakeRibbonPanel(self, Parent, partsName, caption):
        if Parent is not None:
            panel = Parent.GetControlByName(partsName)
            if panel is None:
                panel = Parent.CreatePanel(partsName)    
            return panel
    
    def SetCallbackEvent(self, button, handler):
        if button is not None:
            isValue = button.IsSetCallbackOnClick()
        if isValue == False :
            Event = com.WithEvents(button, handler)
            Event.SetCOMEventClass(Event)
            button.RegisterEventHandlers()
            self.EventList.append(Event)
            return Event

    def MakeRibbonButton(self, Parent, partsName, caption, handler):
        if Parent is not None:
            button = Parent.GetControlByName(partsName)
            if button is None:
                button = Parent.CreateButton(partsName)
                button.Caption = caption
                self.SetCallbackEvent(button, handler)
            return button

    def DeleteControlFromParent(self, child, Parent):
        if child is not None:
            child.UnRegisterEventHandlers()
            if Parent is not None:
                Parent.DeleteControl(child)
            child = None

    def CloseCallbackEvent(self):
        if self.EventList is not None:
            for Event in self.EventList:
                Event.close()

    def MakeRibbonUI(self):
        mainForm = winRoadProxy.MainForm
        # Menu
        self.ribbonMenu = mainForm.MainRibbonMenu
        # Tab
        self.ribbonTab = self.MakeRibbonTab(self.ribbonMenu, 'AsasobiPlugins', 'ASASOBI!!')
        # Group
        self.ribbonGroup = self.MakeRibbonGroup(self.ribbonTab, 'GroupCmdServer', 'Connect to Command Server')
        # Button
        self.ribbonButton1 = self.MakeRibbonButton(self.ribbonGroup, 'ButtonConnectCmd', 'Connect', BtnConnectHandler)
        self.ribbonButton2 = self.MakeRibbonButton(self.ribbonGroup, 'ButtonDisconnectCmd', 'Disconnect', BtnDisconnectHandler)

    def KillRibbonUI(self):
        self.CloseCallbackEvent()
        self.DeleteControlFromParent(self.ribbonButton1, self.ribbonGroup)
        self.DeleteControlFromParent(self.ribbonButton2, self.ribbonGroup)
        self.ribbonTab.DeleteGroup(self.ribbonGroup)
        self.ribbonGroup = None
        if self.ribbonTab.RibbonGroupsCount == 0:
            self.ribbonMenu.DeleteTab(self.ribbonTab)
        self.ribbonTab = None
        self.ribbonMenu = None

def main():
    try:
        start = time.perf_counter_ns()
        global winRoadProxy
        winRoadProxy = UCwinRoadComProxy()
        global const
        const = winRoadProxy.const

        scriptName = 'RoomDigitalTwin'
        global logProxy
        logfilepath = winRoadProxy.PythonPluginDirectory() + scriptName + '.log'
        logProxy = LoggerProxy(scriptName, logfilepath)
        logProxy.logger.info('Start '+ scriptName)

        ribbon = RibbonUI()
        ribbon.MakeRibbonUI()

        # Event Loop
        loopFlg = True
        winRoadProxy.ApplicationServices.IsPythonScriptRun = loopFlg
        while loopFlg:
            time.sleep(0.005)
            #loopFlg = winRoadProxy.ApplicationServices.PythonScriptUserFlg(0)
            loopFlg = winRoadProxy.ApplicationServices.IsPythonScriptRun
            if loopFlg == False:
                logProxy.logger.info("loopFlg={}".format(loopFlg))
                logProxy.logger.info("Script close")
        winRoadProxy.ApplicationServices.IsPythonScriptRun = loopFlg
    except Exception as ex:
        logProxy.logger.error(f'Error occured: {ex}')
    finally:
        elapsed_time = time.perf_counter_ns() - start
        logProxy.logger.info("Total:{}ms".format(elapsed_time/1000000))
        logProxy.logger.info('End '+ scriptName)
        ribbon.KillRibbonUI()
        logProxy.killLogger()
        del winRoadProxy

if __name__ == '__main__':
    main()