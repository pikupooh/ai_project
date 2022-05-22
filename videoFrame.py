class VideoFrame:
    def __init__(self, timestamp, frame, name) -> None:
        self.timestamp = timestamp
        self.frame = frame
        self.name = name

    def getFrame(self):
        return self.frame
    
    def getTimestamp(self):
        return self.timestamp

    def getName(self):
        return self.name