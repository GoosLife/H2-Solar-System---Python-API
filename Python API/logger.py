from datetime import datetime

def logToConsole(body: str, header="ERROR", ):
    print("\n\n~~~" + header + "~~~\n\n" + str(datetime.now()) + "\n\n" + body + "\n\n~~~" + header + " END~~~\n\n")