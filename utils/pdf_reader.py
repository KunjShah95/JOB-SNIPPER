from PyPDF2 import PdfReader
import logging
import os


def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file with error handling.

    Args:
        file_path (str): Path to the PDF file

    Returns:
        str: Extracted text from PDF or error message
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found at {file_path}")

        reader = PdfReader(file_path)

        if len(reader.pages) == 0:
            return "The PDF file appears to be empty."

        text = " ".join(
            [page.extract_text() for page in reader.pages if page.extract_text()]
        )

        if not text.strip():
            return "No text could be extracted from the PDF. It may be scanned or contain only images."

        return text
    except FileNotFoundError as e:
        logging.error(f"File not found: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {str(e)}")
        raise Exception(f"Failed to process PDF: {str(e)}")
