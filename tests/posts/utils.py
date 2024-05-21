from PIL import Image
from faker import Faker
from django.core.files.uploadedfile import SimpleUploadedFile
import io

def generate_image_file():
    # Generate a simple image using Pillow
    image = Image.new('RGB', (100, 100), color='red')

    # Save the image to an in-memory buffer
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')

    # Get the binary data from the buffer
    image_data = buffer.getvalue()

    file = SimpleUploadedFile("testfile.jpg", image_data, content_type="image/jpeg")

    return file


def generate_invalid_file():

    fake = Faker()
    mp3_data = fake.binary(length=10000)  # Generate 10KB of random binary data

    # Create a SimpleUploadedFile with the MP3 data
    file = SimpleUploadedFile("testfile.mp3", mp3_data, content_type="audio/mpeg")
    
    return file