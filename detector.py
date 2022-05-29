import cv2
from PIL import Image 

# This Create a LBPH recognizer.
def main_app():

    flat_list = []
    filtered_list = []
    with open('nameslist.txt', 'r') as f:
        flat_list=[word for line in f for word in line.split()]
        filtered_list=list(filter(lambda word: word != "NO", flat_list))

    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt.xml')

    print(filtered_list)

    recognizers = []

    for name in filtered_list:
        print(f"./data/classifiers/{name}_classifier.xml")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(f"./data/classifiers/{name}_classifier.xml")
        recognizers.append(recognizer)
    
    print(recognizers)

    cap = cv2.VideoCapture(0)
    pred = 0
    while True:
        ret, frame = cap.read()
        #default_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h,x:x+w]
            closing = cv2.morphologyEx(roi_gray, cv2.MORPH_CLOSE, (3, 3))
            cv2.imshow('Closed', closing)

            recognized = False

            for index, recognizer in enumerate(recognizers):
                id, confidence = recognizer.predict(closing)
                confidence = 100 - int(confidence)
                pred = 0
                if confidence > 50:
                    confidence = 100 - int(confidence)
                    pred += +1
                    text = filtered_list[index].upper() + " " + str(confidence) + "%"
                    font = cv2.FONT_HERSHEY_PLAIN
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    recognized = True
                    break
                else:   
                    recognized = False

            if recognized: break
            else:
                pred += -1
                text = "There's a dude behind you"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)


        cv2.imshow("image", frame)


        if cv2.waitKey(20) & 0xFF == ord('q'):
            print(pred)
            break


    cap.release()
    cv2.destroyAllWindows()
    
