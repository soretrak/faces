# This is a sample Python script.

import cv2
import dlib
import face_recognition
import csv

# Load a pre-trained face recognition model
known_face_encodings = []
known_face_names = []

# Replace these with the paths to your known faces
image_of_person1 = face_recognition.load_image_file("images/1015.png")
person1_face_encoding = face_recognition.face_encodings(image_of_person1)[0]
known_face_encodings.append(person1_face_encoding)
known_face_names.append("Fakhri")

image_of_person2 = face_recognition.load_image_file("images/1000.jpg")
person2_face_encoding = face_recognition.face_encodings(image_of_person2)[0]
known_face_encodings.append(person2_face_encoding)
known_face_names.append("Yassine")

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
i = 0



video_capture = cv2.VideoCapture(0)
while True:
    # Capture each frame from the video feed
    ret, frame = video_capture.read()

    # Resize the frame for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the frame from BGR to RGB
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if process_this_frame:
        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Check if the face matches any known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the name of the first known face with a match
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top-5), (right, bottom), (0, 0, 255), 2)

        # Draw the name below the face
        cv2.putText(frame, name, (left + 6, bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        i = i+1
        print(name + " " + str(i))


    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
video_capture.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
