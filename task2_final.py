import os
import openai
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.0)


# Define a Pydantic model for the extracted information
class ExtractionResult(BaseModel):
    customer_company_name: str
    spec: str
    product: str
    certificate_no: str
    shipping_date: str
    total_quantity: int
    total_weight: str


# Define a prompt template to extract the required information
template = """
The following text is a document containing various details. Extract the following key information from the extracted text: 
1. CUSTOMER COMPANY NAME(NOTE THAT THIS FIELD IS NOT IN ENGLISH)
2. SPEC
3. PRODUCT
4. CERTIFICATE NO
5. SHIPPING DATE
6. TOTAL QUANTITY
7. TOTAL WEIGHT
Give only this data, in this format and no other data should be printed.
Text:
{document}

Extracted Information:
1. CUSTOMER COMPANY NAME(NOTE THAT THIS FIELD IS NOT IN ENGLISH):
2. SPEC:
3. PRODUCT:
4. CERTIFICATE NO: 
5. SHIPPING DATE: 
6. TOTAL QUANTITY: 
7. TOTAL WEIGHT: 
"""

# Create a prompt with the text from the document
prompt = PromptTemplate(
    input_variables=["document"],
    template=template,
)

# Text extracted from OCR (already processed and available in 'ocr_text')
ocr_text = """
Extracted Text:
 品算镫明 善 TST CRRTIFICA  F0148-01 客卢名掰 |眷源鲷皴工类股份有限公司 窿品名掰 CR SHET-COIL 恕[}邬 燹票虢礁 M23121567 趱明普编虢 080403F014B INIC
世 @C 皿 规格名掰 JIS 63141 SPCC-SD。 OILED。 (C03, UE) 客卢编虢 11529802 中钢订军缟虢 DC169IE OIST@VBR 加 @ @业 SPBC 交逸日期 镫明善日期 R35 SIIPP
IAG HT APR 03,2019 T/C ISSUB DV APR 03,2019 桧险 CSC AlLL INSPECTION TC 01 客卢酊巢犏虢 @时 (昵_血 项 尺 拉伸武l * *05 仅墨戍佥 ~W(@% 目 麈品序虢 D
NSI0I 量 贫量 墟虢 钢揣虢礁 武片编虢 GI 50 血 硬 箧 厚度 笕度 &度 N5S 降厌|抚短[u  P 1S ISiCuNi | Cr IAI I T[CK IIDJ IBGI IQ 1 皿A COIL N0。 SAWPUB
 I。 Y 卫8   2 尕酬 LABELNO 血 天 q J@J泗2 % R Qu1a 6 襁 凶" |豳 0011T15367 0。800 1219 COIL 10168/+F504/56194042 619404 1691 3051 481 4 35 00031H9
68261 180 1219 COIL 11.420651*94152191541 6219154 166 303| 481 3 #]] 趴T ' 1968262 1。38511X94552191542 6219164 166| 303| 48 3 1968263 10,870FF5021
5192821 519282 1421 2901 591 33 倒 别 Tf 3 1968264 10,846FF60266192822 5519282 1421 290 69 331 r 1968287 11,3005822362297981 5229796 146 297 51 36 
3 4 3 1968268 11,2351723652297962 6229796 146| 297 51 36 例 10041H968254 1480 1219 COILI 10,526k39652331111 5233111 158 3001 51 381 2 佝 3 331 TOTA
L: 8 87,746 蓖J劐 加/, $01疝I箴顾 TENSILE TEST Ia - INmm2 $06  硬度武酸 HARDNESS TEST 荭释 NOTRS Tr: TRACE ELEHENT WITH ITS CONTENT CONFORHIMG TO T
HE SPECIFICATION RFQUIREMENTS。 804078 兹醯明本衷所列盛品 均侬秆料规格颞笾虿甙啄 ,乖符合 榕乏耍衷 胙 HEREBY CERTIFY THAT MATERLALDESCRIBED HEREIN HAs BEN MAMFACTURED AND SURVRYE By TESTED MITH SATISFACTORY RESULTS IN ACCORDANCE WITH THE REQUIKEMEMT QF THE ABOVE MATERIAL SPECIFICATION
"""

# Format the prompt with the extracted OCR text
formatted_prompt = prompt.format(document=ocr_text)

# Call the LLM to process the prompt and extract the information
response = llm.invoke(formatted_prompt)
response_content = response.content
print("Extracted Information:\n", response_content)


# Function to parse the response and create an instance of ExtractionResult
def parse_response(response_text: str) -> ExtractionResult:
    # Initialize a dictionary to hold the extracted values
    extracted_data = {
        "customer_company_name": "",
        "spec": "",
        "product": "",
        "certificate_no": "",
        "shipping_date": "",
        "total_quantity": 0,
        "total_weight": ""
    }

    # Split response text into lines and iterate over them
    for line in response_text.strip().split('\n'):
        # Strip whitespace and check for the expected fields
        line = line.strip()
        if "CUSTOMER COMPANY NAME" in line:
            extracted_data["customer_company_name"] = line.split(":")[1].strip()
        elif "SPEC" in line:
            extracted_data["spec"] = line.split(":")[1].strip()
        elif "PRODUCT" in line:
            extracted_data["product"] = line.split(":")[1].strip()
        elif "CERTIFICATE NO" in line:
            extracted_data["certificate_no"] = line.split(":")[1].strip()
        elif "SHIPPING DATE" in line:
            extracted_data["shipping_date"] = line.split(":")[1].strip()
        elif "TOTAL QUANTITY" in line:
            extracted_data["total_quantity"] = int(line.split(":")[1].strip())
        elif "TOTAL WEIGHT" in line:
            extracted_data["total_weight"] = line.split(":")[1].strip()

    # Create and return a Pydantic model instance
    return ExtractionResult(**extracted_data)


# Convert the extracted data to JSON format
extraction_result = parse_response(response_content)

output_file_path = 'extracted_information.json'
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(extraction_result.dict(), json_file, ensure_ascii=False, indent=4)

print(f"JSON output saved to {output_file_path}")
