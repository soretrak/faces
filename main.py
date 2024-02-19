import os
import pickle

import cv2
import face_recognition
import numpy as np
import cvzone
from datetime import datetime

import requests

# importing firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ecommerce-c6a64-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "ecommerce-c6a64.appspot.com"
})

cap = cv2.VideoCapture(0)
# for ip cam
# adress = "http://192.168.43.1:8080/video"
# cap.open(adress)


api_url = "http://localhost:8080/presence"

cap.set(3, 640)
cap.set(4, 480)

bucket = storage.bucket()

imgBackgroud = cv2.imread("Resources/background2.png")

# importing mode image to a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(imgModeList)

# Load the encoding file
print("Loadind encoding file")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()

encodeListKnown, agentIds = encodeListKnownWithIds
# print(agentIds)
print("Encoding file loaded")

modeType = 0
counter = 0
id = -1
idlast = -1
imgAgent = []

while True:
    # Capture each frame from the video feed
    success, img = cap.read()
    # resizing images
    imgS = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # imgBackgroud[100:100+480,55:55+640] = img
    imgBackgroud[162:162 + 480, 55:55 + 640] = img
    imgBackgroud[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    # imgBackgroud[90:90+120, 800:800+220] =

    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)


            matcheIndex = np.argmin(faceDis)
            print("matcheIndex ", matcheIndex)
            print("faceDis[matcheIndex]", faceDis[matcheIndex])
            #print("faceDis", faceDis)

            if faceDis[matcheIndex] <= 0.5:
                if matches[matcheIndex]:
                    # print("Known Face Detected ", agentIds[matcheIndex])
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackgroud = cvzone.cornerRect(imgBackgroud, bbox, rt=0)

                    id = agentIds[matcheIndex]

                    if counter == 0:
                        # cvzone.putTextRect(imgBackgroud,"Loading", (275,400))
                        # cv2.imshow("Face Attendence", imgBackgroud)
                        # cv2.waitKey(1)
                        counter = 1
                        modeType = 1

        if counter != 0:
            if counter == 1:
                # Get Data
                agentInfo = db.reference(f'Agent/{id}').get()

                # Get Image from firebase
                blob = bucket.get_blob(f'images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgAgent = cv2.imdecode(array, cv2.COLOR_BGR2RGB)

                # update data of attendance
                #datetimeObject = datetime.strptime(agentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                #secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                # inserting data  using api
                if idlast != id:
                    data = {"matric": int(id) , "faceDist": float(faceDis[matcheIndex])}
                    response = requests.post(api_url, json=data)
                    print(counter)
                    print(modeType)
                    print(response.status_code)

                    idlast = id

                    #print(secondsElapsed)
                    #if secondsElapsed > 60:
                    #    ref = db.reference(f'Agent/{id}')
                    #    agentInfo['total_attendance'] += 1
                    #    ref.child('total_attendance').set(agentInfo['total_attendance'])
                    #    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    #else:
                    #    modeType = 3
                    #    counter = 0
                    #    imgBackgroud[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                else:
                    modeType = 3
                    counter = 0
                    imgBackgroud[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                #print(agentInfo)
            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackgroud[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    # cv2.putText(imgBackgroud, str(agentInfo['total_attendance']), (1220, 125), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
                    # cv2.putText(imgBackgroud, str(id), (1220, 485), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0),1)
                    # cv2.putText(imgBackgroud, str(agentInfo['name']), (1220, 530), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0),1)

                    cv2.putText(imgBackgroud, str(agentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackgroud, str(agentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackgroud, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackgroud, str(agentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackgroud, str(agentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackgroud, str(agentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    (w, h), _ = cv2.getTextSize(agentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackgroud, str(agentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50, 1))

                    # set image to backgroud
                    imgBackgroud[175:175 + 216, 909:909 + 216] = imgAgent

                counter += 1

                if counter > 20:
                    counter = 0
                    modeType = 0
                    agentInfo = []
                    imgAgent = []
                    imgBackgroud[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0

    #   cv2.imshow("WebCam", img)
    cv2.imshow("Face Attendence", imgBackgroud)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
