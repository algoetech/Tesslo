import datetime
import cv2
from deepface import DeepFace
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="tairo",
  password="A19m59n19",
  database="tesslo"
)

# This code will open the camera and display the captured images in a window. Press 'q' to stop the camera. 
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# the engine
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    detected_face = frame[int(y):int(y+h), int(x):int(x+w)]
    cv2.imshow('detected_face', detected_face)
    cv2.imwrite('detected_face.jpg', detected_face)
    result = DeepFace.verify("detected_face.jpg", "known_face.jpg")
    if result["verified"]:
        print("Face recognized!")
        # Store the captured image and time in the MySQL database
        cursor = mydb.cursor()
        sql = "INSERT INTO faces (image, time) VALUES (%s, %s)"
        with open("detected_face.jpg", "rb") as f:
            image = f.read()
        time = datetime.now()
        val = (image, time)
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()
    else:
        print("Face not recognized.")