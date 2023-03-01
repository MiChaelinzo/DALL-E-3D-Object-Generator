import requests
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

# Set the OpenAI API endpoint and your API key
API_ENDPOINT = "https://api.openai.com/v1/images/generations"
API_KEY = "YOUR_API_KEY"


# Set the text prompt and model parameters
prompt = "3D model of a equirectangular panorama a beautiful mountain range with a clear blue sky and fluffy white clouds."
model = "image-alpha-001"
size = "1024x1024"

# Send the API request to generate the image
response = requests.post(
    API_ENDPOINT,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    },
    json={
        "model": model,
        "prompt": prompt,
        "num_images": 1,
        "size": size,
        "response_format": "url",
    },
)

# Check if the request was successful
if response.status_code == 200:
    # Get the URL of the generated image from the response
    image_url = response.json()["data"][0]["url"]

    # Download the image using Pillow and convert to a numpy array
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))
    image_array = np.array(image)

    # Set the parameters for inpainting
    window_size = 15
    search_range = 30

    # Inpaint the left side of the image
    left = image_array[:, :512, :]
    left_gray = cv2.cvtColor(left, cv2.COLOR_RGB2GRAY)
    left_mask = np.zeros(left_gray.shape, dtype=np.uint8)
    left_mask[left_gray == 0] = 255
    left_inpaint = cv2.inpaint(left, left_mask, window_size, cv2.INPAINT_TELEA)

    # Inpaint the right side of the image
    right = image_array[:, 512:, :]
    right_gray = cv2.cvtColor(right, cv2.COLOR_RGB2GRAY)
    right_mask = np.zeros(right_gray.shape, dtype=np.uint8)
    right_mask[right_gray == 0] = 255
    right_inpaint = cv2.inpaint(right, right_mask, window_size, cv2.INPAINT_TELEA)

    # Combine the left and right sides of the image
    combined_inpaint = np.concatenate((left_inpaint, right_inpaint), axis=1)

    # Display the combined image using Pillow
    combined_image = Image.fromarray(combined_inpaint)
    combined_image.show()

    # Save the combined image to a file using Pillow
    combined_image.save("combined_image.png")
    combined_image.show()
else:
    # Display the error message if the request failed
    print(f"Error: {response.text}")
