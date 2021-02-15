import boto3
import cv2

#Funcional

def ExtractFace(ImgFile):
    image = cv2.imread(ImgFile)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier("xml/haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("[INFO] Found {0} Faces!".format(len(faces)))
    i = 2;
    for (x, y, w, h) in faces:

        #  cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if len(faces) == 2:
            if i==1:
                roi_color = image[y-45:y + h+50, x-30:x + w+20]
                print("[INFO] Object found. Saving locally.")
                cv2.imwrite("tmp/" + str(w) + str(h) + '_faces.jpg', roi_color)
            else: i = i-1
        else:
            roi_color = image[y - 45:y + h + 40, x - 30:x + w + 20]
            print("[INFO] Object found. Saving locally.")
            cv2.imwrite("tmp/" + str(w) + str(h) + '_faces.jpg', roi_color)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    status = cv2.imwrite('tmp/faces_detected.jpg', image)
    print("[INFO] Image faces_detected.jpg written to filesystem: ", status)


def CompareFace(ImgSource , ImgTarget):

    client = boto3.client('rekognition')
    imageSource = open(ImgSource, 'rb')
    imageTarget = open(ImgTarget, 'rb')
    response = client.compare_faces(SimilarityThreshold=70,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        confidence = str(faceMatch['Face']['Confidence'])
        print('The face at ' +
              str(position['Left']) + ' ' + str(position['Top']) +
              ' matches with ' + confidence + '% confidence')
    imageSource.close()
    imageTarget.close()


ExtractFace('img/licencia.jpg')
#CompareFace('img/mo.jpg','img/md.jpg')
