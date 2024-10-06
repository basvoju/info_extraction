from transformers import LayoutLMForQuestionAnswering, LayoutLMTokenizer
import torch
import fitz
from PIL import Image
import io


def load_docvqa_model():
    model_name = "microsoft/layoutlm-base-uncased"
    tokenizer = LayoutLMTokenizer.from_pretrained(model_name)
    model = LayoutLMForQuestionAnswering.from_pretrained(model_name)
    return tokenizer, model


def extract_field(pdf_path, question, tokenizer, model):
    doc = fitz.open(pdf_path)
    page = doc[0]  # Assume the information is on the first page
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    encoding = tokenizer(question, img, return_tensors="pt", padding="max_length", truncation=True)

    with torch.no_grad():
        outputs = model(**encoding)

    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1
    answer = tokenizer.decode(encoding.input_ids[0][answer_start:answer_end])

    return answer


def information_retrieval(pdf_path):
    tokenizer, model = load_docvqa_model()

    fields = {
        "Customer company name": "What is the customer company name?",
        "Model type": "What is the model type?",
        "Product type": "What is the product type?",
        "Certificate number": "What is the certificate number?",
        "Shipping date": "What is the shipping date?",
        "Total quantity": "What is the total quantity?",
        "Total weight": "What is the total weight?"
    }

    results = {}
    for field, question in fields.items():
        results[field] = extract_field(pdf_path, question, tokenizer, model)

    return results


# Usage
pdf_path = r'C:\Users\BASVOJU\Desktop\Conxai\Inspection_Certificate.pdf'
extracted_info = information_retrieval(pdf_path)
print(extracted_info)