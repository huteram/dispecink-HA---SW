import time
import MujSoubor

xx = MujSoubor.Soubor()
Directory = "c:\\Logger\\"


def init(Directory = "c:\\Logger\\"):
    Directory = Directory

def getTime():
    t = time.localtime()
    d = time.asctime(t)
    Time = str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday)
    return Time

def getTimeMsg():
    t = time.localtime()
    d = time.asctime(t)
    d += " : "
    return d


def writeLog(Name, Data):
    File = Directory + Name + getTime()
    if(xx.FileExists(File)):
        dataOrg = xx.Nahraj(File)
    else:
        dataOrg = ""
    
    dataOrg = '\r\n' + getTimeMsg() + Data + dataOrg 
    xx.Uloz(dataOrg, File)


