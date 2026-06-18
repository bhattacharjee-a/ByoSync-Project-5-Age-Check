# model.py

import cv2
from deepface import DeepFace

from project_log import logger 

class Model:

    def __init__(self, user_face):
        self.face = user_face


    def face_detect (self):
        
        gray = cv2.cvtColor(self.face, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier( r"ML_models\haarcascade_frontalface_default.xml")
        logger.debug(face_cascade.empty())

        if face_cascade.empty():
            raise ValueError("Could not load haarcascade_frontalface_default.xml")

        face_coord = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(120, 120)
)

              
        if len(face_coord) == 0:
            raise ValueError("No face found")

        if len(face_coord) > 1:
            raise ValueError("Multiple faces found")

        for (x, y, w, h) in face_coord:
            
            if w < 120 or h < 120:
                raise ValueError("Face is too small. Please upload a closer image.")

            cv2.rectangle(self.face, (x, y), (x + w, y + h), (0, 255, 0), 2)

            face_crop = self.face[y:y+h, x:x+w]
            age = Model(face_crop).age_detection()
            label = f"Age: {round(age)}"

            cv2.putText(self.face, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
            
        return self.face

    def age_detection(self):

        result = DeepFace.analyze(self.face, actions=['age'], enforce_detection=True)

        if isinstance(result, list):
            age = result[0]['age']
        else:
            age = result['age']

        logger.debug(f"Predicted Age: {age}")

        return age

    
        '''
        difference = abs(age - threshold)
        confidence = min(difference / 10, 1.0)

        if difference <= 2:
            decision = "INCONCLUSIVE"

        elif age >= threshold:
            decision = "ALLOW"

        else:
            decision = "NOT ALLOW"

        return {
            "age": age,
            "confidence": round(confidence, 2),
            "decision": decision
        }'''