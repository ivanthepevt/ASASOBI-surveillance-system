import win32com.client as com
import math

def SetCallbackHandlers(evlist, instance, handler):
    if instance is not None:
        if handler is not None:
            Event = com.WithEvents(instance, handler)
            Event.SetCOMEventClass(Event)
            instance.RegisterEventHandlers()
            if evlist is not None:
                evlist.append([instance, Event])

def CloseCallbackEvent(eventlist):
    if eventlist is not None:
        for i, Event in enumerate(eventlist):
            for k, ev in enumerate(Event):
                if k == 0 :
                    ev.UnRegisterEventHandlers()
                if k == 1 :
                    ev.close()

def AsF8COMdVec3(x, y, z):
    dV3 = com.Dispatch('UCwinRoad.F8COMdVec3')
    dV3.X = x
    dV3.Y = y
    dV3.Z = z
    return dV3

def AsF8COMdVec4(x, y, z, w):
    dV4 = com.Dispatch('UCwinRoad.F8COMdVec4')
    dV4.X = x
    dV4.Y = y
    dV4.Z = z
    dV4.W = w
    return dV4

def AsF8COMdMat4(x, y, z, w):
    dM4 = com.Dispatch('UCwinRoad.F8COMdMat4')
    dM4.X = x
    dM4.Y = y
    dM4.Z = z
    dM4.W = w
    return dM4

def ToStrF8COMdVec3(a):
    return "{}".format(a.X)+",{}".format(a.Y)+",{}".format(a.Z)

def SetF8COMdVec3(target, x, y, z):
    if target is not None:
        target.X = x
        target.Y = y
        target.Z = z
    return target

def Distance(p1, p2) :
    return math.sqrt(pow(p1.X - p2.X, 2) + pow(p1.Y - p2.Y, 2) + pow(p1.Z - p2.Z, 2))