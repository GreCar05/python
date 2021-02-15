import io
import boto3
from PIL import Image


rekognition = boto3.client('rekognition')
image = Image.open("img/mo.jpeg")
stream = io.BytesIO()
image.save(stream,format="JPEG")
image_binary = stream.getvalue()
rekognition.detect_faces(
Image={'Bytes':image_binary},
    Attributes=['ALL']
)