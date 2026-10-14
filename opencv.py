"""camera capture library and colour detection window"""

import cv2  # type: ignore
from detection import DetectionPipeline
from typing import Any
import numpy as np


class CameraDetector:
    def __init__(self, camera_index: int = 0) -> None:
        self.cap = cv2.VideoCapture(camera_index)
        self.lower_blue = np.array([100, 150, 50])
        self.upper_blue = np.array([140, 255, 255])
        self.pipeline = DetectionPipeline(min_area=2000)

    def get_frame_detections(self) -> tuple[bool,
                                            Any,
                                            dict[str,
                                                 list[tuple[int,
                                                            int,
                                                            int,
                                                            int
                                                            ]]]]:
        ret, frame = self.cap.read()
        if not ret:
            return (False, None, {})
        height, width, _ = frame.shape
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        contours, _ = cv2.findContours(mask,
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        boxes = [cv2.boundingRect(c) for c in contours]
        categorised = self.pipeline.categorise_boxes(boxes, width)
        return True, frame, categorised

    def close(self) -> None:
        self.cap.release()
        cv2.destroyAllWindows()
