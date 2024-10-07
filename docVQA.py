import torch
from transformers import LayoutLMv2Processor, LayoutLMv2ForQuestionAnswering
from PIL import Image
import pytesseract
from datasets import Dataset


# Task 1: Document Understanding

def preprocess_image(image_path):
    # Load image using PIL
    image = Image.open(image_path).convert("RGB")
    return image


def perform_ocr(image):
    # Perform OCR to get words and bounding boxes
    ocr_results = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    words = ocr_results['text']
    boxes = []
    for i in range(len(words)):
        (x, y, w, h) = (ocr_results['left'][i], ocr_results['top'][i],
                        ocr_results['width'][i], ocr_results['height'][i])
        boxes.append([x, y, x + w, y + h])
    return words, boxes


# Task 2: Information Retrieval using DocVQA

def load_docvqa_model():
    processor = LayoutLMv2Processor.from_pretrained("microsoft/layoutlmv2-base-uncased")
    model = LayoutLMv2ForQuestionAnswering.from_pretrained("microsoft/layoutlmv2-base-uncased")
    return processor, model


def prepare_docvqa_input(image, question, words, boxes, processor):
    # Prepare input for the model
    encoding = processor(image, question, words, boxes=boxes, return_tensors="pt")
    return encoding


def extract_field(image, question, words, boxes, processor, model):
    encoding = prepare_docvqa_input(image, question, words, boxes, processor)
    outputs = model(**encoding)

    # Get the most likely beginning and end of the answer
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1

    # Decode the answer
    answer = processor.tokenizer.decode(encoding.input_ids[0][answer_start:answer_end])
    return answer


def extract_fields(image, words, boxes, processor, model):
    fields = {
        "Customer company name": "What is the customer company name?",
        "Model type": "What is the model type?",
        "Product type": "What is the product type?",
        "Certificate number": "What is the certificate number?",
        "Shipping date": "What is the shipping date?",
        "Total quantity": "What is the total quantity?",
        "Total weight": "What is the total weight?"
    }

    extracted_fields = {}
    for field, question in fields.items():
        extracted_fields[field] = extract_field(image, question, words, boxes, processor, model)

    return extracted_fields


# Main pipeline

def process_document(image_path):
    # Task 1
    image = preprocess_image(image_path)
    words, boxes = perform_ocr(image)

    # Task 2
    processor, model = load_docvqa_model()
    extracted_fields = extract_fields(image, words, boxes, processor, model)

    return extracted_fields


# Example usage
image_path = "page_1.png"
results = process_document(image_path)
print(results)

