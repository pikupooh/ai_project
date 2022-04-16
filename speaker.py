class Speaker:
    def __init__(self, startTimestamp, endTimestamp, speaker) -> None:
        self.startTimestamp = startTimestamp
        self.endTimestamp = endTimestamp
        self.speaker = speaker

    def getSpeaker(self):
        return self.speaker
    
    def getStartTimestamp(self):
        return self.startTimestamp

    def getEndTimestamp(self):
        return  self.endTimestamp