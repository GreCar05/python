import io
import boto3
from PIL import Image


rekognition = boto3.client('rekognition')

sourceFile = 'Tzuyu.jpeg'
targetFile = 'twice_group.jpg'

imageSource = open(sourceFile, 'rb')
imageTarget = open(targetFile, 'rb')
response = rekognition.compare_faces(SimilarityThreshold=80,
                                     SourceImage={'Bytes': imageSource.read()},
                                     TargetImage={'Bytes': imageTarget.read()})
response['FaceMatches']