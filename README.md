# info_extraction

# PDF Information Extraction

This repository contains a Python script that extracts key information from PDF documents using Optical Character Recognition (OCR) and Natural Language Processing (NLP). The script processes images within PDFs to extract text and identify key-value pairs for structured data retrieval.

## Features

- Extract images from PDF files.
- Perform OCR on extracted images using EasyOCR.
- Identify key-value pairs in the extracted text using regex and NLP.
- Format extracted data using OpenAI's GPT model.
- Save extracted information in JSON format.

## Requirements

To run this script, need to have the following Python packages installed:

- `fitz` (PyMuPDF)
- `easyocr`
- `re`
- `spacy`
- `Pillow` (PIL)
- `openai`
- `langchain_openai`
- `python-dotenv`
- `pydantic`

Install these packages using pip:
```bash
pip install PyMuPDF easyocr spacy openai langchain_openai python-dotenv pydantic Pillow


Additionally, you need to download the SpaCy language model:

python -m spacy download en_core_web_sm
```


## Usage
1. Place the PDF file from which you want to extract information in the designated path in the script.
2. Ensure your OpenAI API key is stored in an environment variable named OPENAI_API_KEY in .env file.
3. Run the script using: python task1_final.py and python task2_final.py.
4. The extracted information will be saved in a file named extracted_information.json.




## Example:
An example of the extracted JSON format:
```
{
    "customer_company_name": "Company Name",
    "spec": "Specification",
    "product": "Product Name",
    "certificate_no": "Certificate Number",
    "shipping_date": "Shipping Date",
    "total_quantity": 8,
    "total_weight": "Weight in units"
}
```
