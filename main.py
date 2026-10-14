from opencv import CameraDetector
import cv2


def main() -> None:
    print(getattr(cv2, "__version__", "no version"))
    detector = CameraDetector()
    while True:
        success, frame, categorised = detector.get_frame_detections()
        if not success:
            break
        for l in categorised.values():
            for b in l:
                x, y, w, h = b
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("webcam feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    detector.close()


if __name__ == "__main__":
    main()
