# User Interface

import cv2
import json

import repository
from project_log import logger
from model import Model

class User:

    def __init__(self, face, threshold, user):
        self.face = face
        self.thresh = threshold
        self.user_info = user

    @classmethod
    def menu(cls):

        image_path = input("Choose An Image (Location): ")
        img = cv2.imread(image_path)

        if img is None:
            raise ValueError("Invalid image path")

        threshold = int(input("Threshold:\n[18+] [21+] [60+]\Choose Threshold (Without plus sign): "))

        if threshold not in [18,21,60]:
            raise ValueError("Threshold must be 18, 21 or 60")

        obj = cls(
        face=img,
        threshold=threshold,
        user=repository.load_verification_db()
            )

        result = obj.decision()

        print("\n========================")
        print("Verification Result")
        print("========================")
        logger.info(json.dumps(result, indent=4))


        model = Model(obj.face)

        if logger.debug is True:

            img = model.face_detect()
            cv2.imshow("Face Detection", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return


    def decision(self):

        age = Model(self.face).age_detection()


        difference = abs(age - self.thresh)
        confidence = max(0, 1 - difference/20)
        #confidence = min(difference / 10, 1.0)
        
        if difference <= 2:
            decision = "INCONCLUSIVE"

        elif age >= self.thresh:
            decision = "PASS"

        else:
            decision = "FAIL"

        if DEBUG_MODE:
            self.user_info = {
                "threshold": self.thresh,
                "predicted_age": round(age),
                "is_above_threshold": age >= self.thresh,
                "confidence": round(confidence, 2),
                "decision": decision
                }
            
        else:
            self.user_info = {
            "threshold": self.thresh,
            "is_above_threshold": age >= self.thresh,
            "confidence": round(confidence, 2),
            "decision": decision
            }
        
        repository.save_verification_db(self.user_info)
        
        return self.user_info
    
