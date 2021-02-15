import boto3

#session = boto3.Session(profile_name='default')
#client = boto3.client('rekognition')

# grab the image from online
# imgurl = 'https://media1.popsugar-assets.com/files/thumbor/xptPz9chB_kMwxzqI9qMCZrK_YA/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2015/07/13/766/n/1922398/3d3a7ee5_11698501_923697884352975_2728822964439153485_n.jpg'
# imgurl = 'http://media.comicbook.com/uploads1/2015/07/fox-comic-con-panel-144933.jpg'

#img = Image.open("img/modelo1.jpg")

#imgbytes = image_helpers.get_image_from_file(img)

#rekresp = client.detect_faces(Image={'Bytes': imgbytes}, Attributes=['ALL'])

#print(rekresp)

# pprint(rekresp['CelebrityFaces'])
#for face in rekresp['CelebrityFaces']:
#    print(face['Name'],'confidence:', face['Mat chConfidence'], 'url:',face['Urls'])


if __name__ == "__main__":
    sourceFile = 'img/mo.jpg'
    targetFile = 'img/md.jpg'
    client = boto3.client('rekognition')
    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')
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