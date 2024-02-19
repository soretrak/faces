import cv2
import face_recognition
import pickle
import os
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


#importing student image to a list
folderPath = 'images'
imagesPathList = os.listdir(folderPath)
imgList = []
agentIds = []
for path in imagesPathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
#    print(os.path.splitext(path)[0])
    agentIds.append(os.path.splitext(path)[0])

    # firebase storage
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


#for agent in agentIds:
#    print(agent)

def createEncodings(imageList):
    encodeList = []
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        print("encode")
        face_pickled_data = pickle.dumps(encode)
        print(encode)
        print(face_pickled_data)
        encodeList.append(encode)
    return encodeList

print("encoding started ...")
encodeListKnown = createEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, agentIds]
#print(encodeListKnownWithIds)
print("encoding Completed")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("file saved")




