# image inhance and preprocess   - opencv   

import os
import sys
import requests
# If you are using a Jupyter Notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO

# Add your Computer Vision key and endpoint to your environment variables.
if 'COMPUTER_VISION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_KEY']
else:
    print("\nSet the COMPUTER_VISION_KEY environment variable.\n*Restart your shell or IDE for changes to take effect.*")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n*Restart your shell or IDE for changes to take effect.*")
    sys.exit()

analyze_url = endpoint + "vision/v3.1/ocr"



def extract_text_image(image_path):
    # with open(image_path,"rb") as image_file:
    image_data = open(image_path, "rb").read()

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }
    params = {'language': 'unk', 'detectOrientation': 'true'}
    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()

    # Extract the word bounding boxes and text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)
                # print(word_infos)

    # print("extracted text",image_path)
    extracted_text=""
    for word in word_infos:
        extracted_text+=word["text"]+""
    return extracted_text.strip()
        # print("\n")
def extract_text_textfile(text_file):
    with open(text_file, 'r') as file:
        text_content=file.read()
    return text_content.strip()

image_dir="C:/Users/navgurukul/Downloads/imageExtract/PS1-TR-Data/images"
textFile_dir="C:/Users/navgurukul/Downloads/imageExtract/PS1-TR-Data/groundtruth" 

image_files = []
for f in os.listdir(image_dir):
    if os.path.isfile(os.path.join(image_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_files.append(os.path.join(image_dir, f))

text_files = []
for f in os.listdir(textFile_dir):
    full_path = os.path.join(textFile_dir, f)
    if os.path.isfile(full_path) and f.lower().endswith('.txt'):
        text_files.append(full_path)

text_files.sort()

if len(image_files)!=len(text_files):
    print("do not match")
    sys.exit()

for image_path, text_file in zip(image_files, text_files):
    extracted_text_image = extract_text_image(image_path)

    extracted_text_textfile = extract_text_textfile(text_file)

    match_status="correct" if extracted_text_image == extracted_text_textfile else "incorrect"

    print(f"img file:{extracted_text_image}")
    print(f"text file:{extracted_text_textfile}")
    print(f"{os.path.basename(image_path)}, {extracted_text_image}, {extracted_text_textfile}, {match_status}")
    





   

   
