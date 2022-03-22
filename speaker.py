class Speaker:
    def __init__(self, timestamp, speaker) -> None:
        self.timestamp = timestamp
        self.speaker = speaker

    def getSpeaker(self):
        return self.speaker
    
    def getTimestamp(self):
        return self.timestamp