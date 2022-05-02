from datetime import datetime

def LOG(message):  
    print(datetime.now().strftime("%H:%M:%S") + ": -> " + message)