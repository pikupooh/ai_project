class SpeechText:
    def __init__(self, timestamp, text) -> None:
        self.timestamp = timestamp
        self.text = text

    def getText(self):
        return self.text
    
    def getTimestamp(self):
        return self.timestamp