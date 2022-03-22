class VideoFrame:
    def __init__(self, timestamp, frame) -> None:
        self.timestamp = timestamp
        self.frame = frame

    def getFrame(self):
        return self.frame
    
    def getTimestamp(self):
        return self.timestamp