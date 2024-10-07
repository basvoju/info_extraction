from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from pdf2image import convert_from_path
from PIL import Image


def load_docvqa_model():
    model_name = "impira/layoutlm-document-qa"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    return tokenizer, model


def extract_field(pdf_path, question, tokenizer, model):
    # Convert PDF to image
    images = convert_from_path(pdf_path)
    image = images[0]  # Assume single-page PDF for simplicity

    # Prepare inputs
    encoding = tokenizer(question, image, return_tensors="pt", padding="max_length", truncation=True)

    # Get model output
    with torch.no_grad():
        outputs = model(**encoding)

    # Process output
    predictions = outputs.logits.argmax(-1).squeeze().tolist()
    tokens = tokenizer.convert_ids_to_tokens(encoding.input_ids.squeeze().tolist())

    # Extract answer
    answer_tokens = [token for token, pred in zip(tokens, predictions) if pred == 1]
    answer = tokenizer.convert_tokens_to_string(answer_tokens)

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
pdf_path = "path_to_inspection_certificate.pdf"
extracted_info = information_retrieval(pdf_path)
print(extracted_info)