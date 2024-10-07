import fitz
import easyocr
import re
import spacy
from PIL import Image
import io


nlp = spacy.load("en_core_web_sm")

# Initialize EasyOCR reader
reader = easyocr.Reader(['ch_sim','en'])

# Extract images from the PDF using PyMuPDF (fitz)
def extract_images_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)

    return images

# Apply OCR to extract text from the image using EasyOCR
def extract_text_from_image(image):
    image.save("temp_image.png")  # Save the image temporarily
    result = reader.readtext("temp_image.png", detail=0)  # detail=0 returns only the text
    return " ".join(result)  # Join all detected text into a single string

# Identify key-value pairs in the extracted text using regex or NER
def extract_key_value_pairs(text):
    key_value_pairs = {}

    # Basic regex for key-value pairs (like "Field: Value")
    matches = re.findall(r'(\w[\w\s]+):\s*(\w[\w\s]+)', text)
    for match in matches:
        key, value = match
        key_value_pairs[key.strip()] = value.strip()

    # Further improvements can be done using NLP (like spaCy) if text is complex
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'GPE', 'DATE', 'MONEY']:  # Sample named entities for key-value
            key_value_pairs[ent.label_] = ent.text

    return key_value_pairs

# Process the PDF for key-value extraction
def process_pdf_for_key_value_pairs(pdf_path):
    images = extract_images_from_pdf(pdf_path)

    all_key_value_pairs = {}

    for i, image in enumerate(images):
        print(f"Processing image from page {i + 1}")

        # Extract text from the image using EasyOCR
        text = extract_text_from_image(image)
        print("Extracted Text:\n", text)

        # Extract key-value pairs from the text
        key_value_pairs = extract_key_value_pairs(text)
        print("Extracted Key-Value Pairs:\n", key_value_pairs)

        all_key_value_pairs[f"Page_{i + 1}"] = key_value_pairs

    return all_key_value_pairs



def format_text_with_gpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that formats text and returns the text in "},
            {"role": "user", "content": raw_text}
        ]
    )
    return response['choices'][0]['message']['content']


pdf_path = r'C:\Users\BASVOJU\Desktop\Conxai\Inspection_Certificate.pdf'
extracted_key_values = process_pdf_for_key_value_pairs(pdf_path)
print("All Extracted Key-Value Pairs:\n", extracted_key_values)
