import cv2

class VideoReader:
    def __init__(self, path: str):
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise IOError(f"Could not open video: {path}")

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.aspect_ratio = self.width / self.height

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame  # BGR, numpy array (H, W, 3)

    def release(self):
        self.cap.release()