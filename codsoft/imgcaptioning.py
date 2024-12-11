
# Install necessary libraries
pip install transformers torch torchvision

import torch
import torchvision.transforms as transforms
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

# Load pre-trained image captioning model
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Image preprocessing
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Function to generate captions for images
def generate_caption(image_path):
    i_image = Image.open(image_path)
    if i_image.mode != "RGB":
        i_image = i_image.convert(mode="RGB")

    pixel_values = feature_extractor(images=i_image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_caption

# Example usage:
image_path = "/content/image.jpg" # Replace with your image path
caption = generate_caption(image_path)
print(f"Generated Caption: {caption}")