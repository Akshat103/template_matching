import cv2
import numpy as np

class TemplateMatcher:
    def __init__(self, video_device=0):
        self.cap = cv2.VideoCapture(video_device)
        self.template = None
        self.bbox = None
        self.threshold = 0.8
        self.live_fps = 10
        self.running = False

    def select_roi(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return

        self.bbox = cv2.selectROI("Select ROI", frame, False)
        x, y, w, h = self.bbox
        self.template = frame[y:y+h, x:x+w]
        cv2.destroyWindow("Select ROI")

    def set_threshold(self, threshold):
        self.threshold = threshold / 100.0

    def set_live_fps(self, fps):
        self.live_fps = fps

    def start(self):
        if self.template is None:
            print("Error: Template not selected.")
            return

        self.running = True
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            if self.bbox:
                x, y, w, h = self.bbox
                square_region = frame[y:y+h, x:x+w]
            else:
                square_region = frame

            norm_frame = cv2.normalize(square_region, None, 0, 255, cv2.NORM_MINMAX)

            mask = np.zeros_like(square_region)
            for scale in np.linspace(0.5, 1.0, 5)[::-1]:
                resized_template = cv2.resize(self.template, None, fx=scale, fy=scale)
                result = cv2.matchTemplate(norm_frame, resized_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                if max_val > self.threshold:
                    loc = np.where(result >= self.threshold)
                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(mask, pt, (pt[0] + resized_template.shape[1], pt[1] + resized_template.shape[0]), (0, 255, 0), -1)

            square_region = cv2.addWeighted(square_region, 1, mask, 0.5, 0)

            if self.bbox:
                frame[y:y+h, x:x+w] = square_region
            else:
                frame = square_region

            accuracy = max_val if max_val > 0 else 0.0
            cv2.putText(frame, f"Accuracy: {accuracy:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.putText(frame, f"Threshold: {self.threshold}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Live FPS: {self.live_fps}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow("Real-Time Template Matching", frame)

            key = cv2.waitKey(1000 // self.live_fps) & 0xFF
            if key == ord('q'):
                self.running = False

        self.cap.release()
        cv2.destroyAllWindows()
