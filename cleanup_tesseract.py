import re

# Cleanup function to remove noise and fix common OCR errors
def clean_ocr_text(ocr_text):
    # Remove special characters and extra spaces
    cleaned_text = re.sub(r'\n+', '\n', ocr_text)  # Remove multiple newlines
    cleaned_text = re.sub(r'[^\w\s.,-]', '', cleaned_text)  # Remove unwanted characters
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)  # Remove extra spaces
    return cleaned_text

# Function to extract fields using regex on cleaned text
def extract_fields_from_cleaned_text(cleaned_text):
    fields = {}

    # Look for 'TEST CERTIFICATE' keyword
    fields["Test Certificate"] = re.search(r'TEST CERTIFICATE', cleaned_text) is not None

    # Improved pattern to extract chemical composition - example pattern
    chemical_composition_match = re.search(r'CHEMICAL COMPOSITION\s?%?(.*)', cleaned_text, re.IGNORECASE)
    fields["Chemical Composition"] = chemical_composition_match.group(1).strip() if chemical_composition_match else 'Not Found'

    # Extract a date in the format YYYY (year)
    shipping_date_match = re.search(r'(\d{4})', cleaned_text)
    fields["Shipping Date"] = shipping_date_match.group(1) if shipping_date_match else 'Not Found'

    # Pattern to extract certificate number if mentioned
    certificate_match = re.search(r'Certificate\s?Number\s?:?\s?(\w+)', cleaned_text, re.IGNORECASE)
    fields["Certificate Number"] = certificate_match.group(1).strip() if certificate_match else 'Not Found'

    # Extract customer company name based on likely patterns
    customer_match = re.search(r'Customer\s?([\w\s]+)', cleaned_text, re.IGNORECASE)
    fields["Customer Company Name"] = customer_match.group(1).strip() if customer_match else 'Not Found'

    # Extract sample ID or any specific code format (for example, alphanumeric patterns)
    sample_id_match = re.search(r'SAMPLE\sID\s?:?\s?(\w+)', cleaned_text, re.IGNORECASE)
    fields["Sample ID"] = sample_id_match.group(1).strip() if sample_id_match else 'Not Found'

    # Extract possible numeric values like MPa
    mpa_match = re.search(r'(\d+)\s?MPa', cleaned_text)
    fields["MPa"] = mpa_match.group(1) + ' MPa' if mpa_match else 'Not Found'

    return fields

# Example usage with Tesseract OCR output (replace with your actual OCR result)
tesseract_ocr_output = """
ra

ees
ia

me WH

er TEST CERTIFICATE
oY a fous-o1
5p 245 [RRO RMA aRaH
—_ BER | wesvzs607 x
. O SUE 8M Pore)
wc en Simctt [encase] tee | wn. 03 2010
WF [ese wu narecrion Pa eeigaR|o)
T oar A] TERE ON OUENTTION 7
A) ge {at " | cd
Flawnm oom Ee |ase| senses | ne |e =| | | [e[amfr]s]sifui|cefar ia
ra ‘sme | oor | toni QTY) kg ~{EAT| COLL NO, | SAMPLE ID. LY. S| | dull uk 1 _ hii E es
MILABEL No, om_|_rm_| MPa, Wnm2 | | RB 1x10) i a {ARI
spateao7 a aoa) — eva] So] eran — serene —|tat sos at ye a7 =
8261 | 380) $219) col roieet Eziors | 06) 20a] 4a) 28 a2 ary 3 | | |
soszez |") 1210) Ol so1ee2~Brio1es | too] saa) sal se : 4
cas | S| 5 |! siosent estore | tia] 200| 23 Se 1 1g ory 2
eszes | S| tf | tezsze | Boioxea | 142) 200] ba ui 1 |
caer | t | s | * zsroot | Beaaree~ | tae] 27] 1) 30 add | | fas |
aH aaToeh | BazSTO Ht aa i |
eapeeezss. | + 480] 1219] coi pasetitt | BASStTY Ba) | dubs) | |
13 ea 1 | |
| . | | |
| | | ae |
|| ‘ LAB "|
| = / |
| | aN
| | || ; tT |
| I | |
or ERR THs TEST Ws = Wd
‘op Semimt = JARGIESS TEST \
ae »)
bores si
TrSTRACE ELEMENT WITH ITS CONTENT CONFORMING TO THE SPECIFICATION REQUIREMENTS 804076
Tah TTT ARERR
"""

# Step 1: Clean the OCR text
cleaned_text = clean_ocr_text(tesseract_ocr_output)
print("Cleaned Text:")
print(cleaned_text)

# Step 2: Extract relevant fields
extracted_fields = extract_fields_from_cleaned_text(cleaned_text)
print("\nExtracted Fields:")
for key, value in extracted_fields.items():
    print(f"{key}: {value}")
