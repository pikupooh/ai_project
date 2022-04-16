class SpeechText:
    def __init__(self, startTimestamp, endTimestamp, text) -> None:
        self.startTimestamp = startTimestamp
        self.endTimestamp = endTimestamp
        self.text = text

    def getText(self):
        return self.text
    
    def getStartTimestamp(self):
        return self.startTimestamp
    
    def getEndTimestamp(self):
        return self.endTimestamp