# ============================================================
# SKILLSYNC - PDF PROCESSOR
# ============================================================
import io

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


# ============================================================
# EXTRACT TEXT FROM PDF
# ============================================================

def extract_text_from_pdf(uploaded_file):
    """
    Extract readable text from a Streamlit uploaded PDF file.

    Parameters
    ----------
    uploaded_file : Streamlit UploadedFile
        PDF uploaded using st.file_uploader()

    Returns
    -------
    str
        Extracted text from all readable PDF pages.
    """

    if uploaded_file is None:
        return ""

    if PdfReader is None:
        raise ImportError(
            "pypdf is not installed. "
            "Please install it using: pip install pypdf"
        )

    try:
        # Read uploaded file into memory
        pdf_bytes = uploaded_file.getvalue()

        if not pdf_bytes:
            return ""

        pdf_stream = io.BytesIO(pdf_bytes)

        # Create PDF reader
        reader = PdfReader(pdf_stream)

        extracted_text = []

        # Extract text page by page
        for page in reader.pages:
            try:
                page_text = page.extract_text()

                if page_text:
                    extracted_text.append(page_text)

            except Exception:
                # Skip pages that cannot be read
                continue

        # Combine all pages
        final_text = "\n\n".join(extracted_text)

        return final_text.strip()

    except Exception as e:
        raise RuntimeError(
            f"Unable to read PDF file: {str(e)}"
        )


# ============================================================
# GET PDF PAGE COUNT
# ============================================================

def get_pdf_page_count(uploaded_file):
    """
    Return number of pages in uploaded PDF.
    """

    if uploaded_file is None:
        return 0

    if PdfReader is None:
        return 0

    try:
        pdf_bytes = uploaded_file.getvalue()

        if not pdf_bytes:
            return 0

        reader = PdfReader(io.BytesIO(pdf_bytes))

        return len(reader.pages)

    except Exception:
        return 0


# ============================================================
# CLEAN EXTRACTED TEXT
# ============================================================

def clean_pdf_text(text):
    """
    Clean unnecessary spaces and blank lines
    from extracted PDF text.
    """

    if not text:
        return ""

    # Normalize line breaks
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            lines.append(line)

    # Rebuild clean text
    cleaned_text = "\n".join(lines)

    return cleaned_text.strip()


# ============================================================
# GET PDF SUMMARY INFORMATION
# ============================================================

def get_pdf_info(uploaded_file):
    """
    Return basic information about uploaded PDF.
    """

    if uploaded_file is None:
        return {
            "file_name": "",
            "file_size_kb": 0,
            "page_count": 0
        }

    file_name = uploaded_file.name

    try:
        file_size_kb = round(
            uploaded_file.size / 1024,
            2
        )
    except Exception:
        file_size_kb = 0

    page_count = get_pdf_page_count(uploaded_file)

    return {
        "file_name": file_name,
        "file_size_kb": file_size_kb,
        "page_count": page_count
    }


# ============================================================
# MAIN PROCESSOR
# ============================================================

def process_pdf(uploaded_file):
    """
    Complete PDF processing pipeline.

    Returns:
        {
            "text": extracted text,
            "page_count": number of pages,
            "file_name": PDF name,
            "file_size_kb": file size
        }
    """

    if uploaded_file is None:
        return {
            "text": "",
            "page_count": 0,
            "file_name": "",
            "file_size_kb": 0
        }

    # Extract
    raw_text = extract_text_from_pdf(uploaded_file)

    # Clean
    cleaned_text = clean_pdf_text(raw_text)

    # File information
    info = get_pdf_info(uploaded_file)

    return {
        "text": cleaned_text,
        "page_count": info["page_count"],
        "file_name": info["file_name"],
        "file_size_kb": info["file_size_kb"]
    }