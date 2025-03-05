import json
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_textract.type_defs import DetectDocumentTextResponseTypeDef

def detect_file_text() -> None:
    client = boto3.client("textract")

    file_path = Path(__file__).parent / "Imagens" / "lista-material-escolar.jpeg"
    with open(file_path, "rb") as f:
        document_bytes = f.read()

    try:
        response = client.detect_document_text(Document={"Bytes": document_bytes})
        with open("response.json", "w", encoding="utf-8") as response_file:
            json.dump(response, response_file, ensure_ascii=False, indent=4)
    except ClientError as e:
        print(f"Erro processando documento: {e}")

def get_lines() -> list[str]:
    try:
        with open("response.json", "r", encoding="utf-8") as f:
            data: DetectDocumentTextResponseTypeDef = json.load(f)
            blocks = data.get("Blocks", [])  # Corrigido "blocks" para "Blocks"
        
        return [block["Text"] for block in blocks if block.get("BlockType") == "LINE"]
    
    except (IOError, KeyError) as e:
        print(f"Erro ao ler o arquivo response.json: {e}")
        detect_file_text()
        return []

if __name__ == "__main__":
    for line in get_lines():
        print(line)