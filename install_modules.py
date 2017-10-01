import pip

def installRequests(package):
    pip.main(['install', package])

def installbs4(package):
    pip.main(['install', package])
    
try:
    installRequests('requests')
    installbs4('beautifulsoup')



    
except AttributeError():
    pass
