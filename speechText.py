class SpeechText:
    def __init__(self, timestamp, speechText, speaker) -> None:
        self.timestamp = timestamp
        self.speechText = speechText
        self.speaker = speaker

    def getSpeaker(self):
        return self.speaker
    
    def getTimestamp(self):
        return self.timestamp

    def getSpeechText(self):
        return self.speechText