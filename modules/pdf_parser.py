import PyPDF2
import re
import json
from typing import Dict


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        raise RuntimeError(f"Error reading PDF: {e}")


def parse_sections_from_text(text: str, sections: Dict[str, str]) -> Dict[str, str]:
    """
    Extracts specific sections from text using regex patterns.

    Args:
        text (str): The full text extracted from a PDF.
        sections (Dict[str, str]): Dictionary of section names and their regex patterns.

    Returns:
        Dict[str, str]: Extracted sections with section names as keys and content as values.
    """
    extracted_sections = {}
    for section, pattern in sections.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            extracted_sections[section] = match.group(1).strip()

    return extracted_sections


def parse_pdf_sections(pdf_path: str, sections: Dict[str, str], output_json_path: str) -> None:
    """
    Extracts text from a PDF, parses it into structured sections, and saves it to a JSON file.

    Args:
        pdf_path (str): Path to the PDF file.
        sections (Dict[str, str]): Dictionary of section names and regex patterns.
        output_json_path (str): Path to save the parsed JSON file.

    Returns:
        None
    """
    text = extract_text_from_pdf(pdf_path)
    parsed_sections = parse_sections_from_text(text, sections)

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(parsed_sections, f, indent=4)

    print(f"✅ Parsed data saved to {output_json_path}")
