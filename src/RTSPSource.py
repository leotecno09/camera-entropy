import cv2
import hashlib
import time
import threading
import logging

logger = logging.getLogger("capture")

class RTSPSource:
    def __init__(self, name, url, interval_seconds=300):
        self.name = name
        self.url = url
        self.interval_seconds = interval_seconds
        self.last_hash = None
        self.last_capture_time = None
        self._lock = threading.Lock()

    def _capture_once(self):
        cap = cv2.VideoCapture(self.url)
        try:
            if not cap.isOpened():
                logger.warning(f"[{self.name}] unable to get stream")
                return None

            # serve a scartare vecchi frame nel buffer video
            for _ in range(5):
                cap.grab()

            ret, frame = cap.retrieve()
            if not ret:
                logger.warning(f"[{self.name}] frame not readable")
                return None

            success, buffer = cv2.imencode(".jpg", frame)
            if not success:
                return None

            return buffer.tobytes()
        finally:
            cap.release()

    def capture_and_hash(self):
        frame_bytes = self._capture_once()
        if frame_bytes is None:
            return

        digest = hashlib.sha256(frame_bytes).hexdigest()

        with self._lock:
            self.last_hash = digest
            self.last_capture_time = time.time()

        logger.info(f"[{self.name}] new hash: {digest[:12]}...")

    def get_hash(self):
        with self._lock:
            return self.last_hash


    def run_forever(self):
        while True:
            self.capture_and_hash()
            time.sleep(self.interval_seconds)