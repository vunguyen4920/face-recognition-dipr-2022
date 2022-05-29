import cv2
import os

def capture(personName):
        path = "./data/" + personName
        imageNums = 0
        detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_alt.xml")
        try:
            os.makedirs(path)
        except:
            print('Directory Already Created')
        vid = cv2.VideoCapture(0)
        while True:

            ret, img = vid.read()
            new_img = None
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            closing = cv2.morphologyEx(gray_img, cv2.MORPH_CLOSE, (3, 3))

            face = detector.detectMultiScale(image=closing, scaleFactor=1.1, minNeighbors=5)
            for x, y, w, h in face:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
                cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255))
                cv2.putText(img, str(str(imageNums)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255))
                new_img = img[y:y+h, x:x+w]
            cv2.imshow("Face Detection", img)
            key = cv2.waitKey(1) & 0xFF


            try :
                cv2.imwrite(str(path+"/"+str(imageNums)+personName+".jpg"), new_img)
                imageNums += 1
            except :

                pass
            if key == ord("q") or key == 27 or imageNums > 310:
                break
        cv2.destroyAllWindows()
        return imageNums

