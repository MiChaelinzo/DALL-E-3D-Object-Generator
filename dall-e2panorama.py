import requests
from PIL import Image
from io import BytesIO

# Set the OpenAI API endpoint and your API key
API_ENDPOINT = "https://api.openai.com/v1/images/generations"
API_KEY = "YOU_API_KEY"

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

    # Download and save the image using Pillow
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))
    image.save("generated_image.png")
    image.show()
else:
    # Display the error message if the request failed
    print(f"Error: {response.text}")
