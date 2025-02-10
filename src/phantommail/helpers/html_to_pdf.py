import base64
import io

from xhtml2pdf import pisa


def create_pdf(html_content: str) -> str:
    """Convert HTML content to PDF bytes and encode as base64 string.

    Args:
        html_content (str): The HTML content to convert

    Returns:
        str: Base64 encoded PDF string

    """
    # Add CSS for A4 page format and table scaling
    a4_styled_html = f"""
        <html>
        <head>
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    width: 100%;
                    font-family: Arial, sans-serif;
                }}
                table {{
                    width: 100%;
                    margin-bottom: 1em;
                    border-collapse: collapse;
                    font-size: 12px;
                }}
                td, th {{
                    padding: 4px;
                    word-wrap: break-word;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
    """

    # Create an in-memory buffer to store the PDF
    pdf_buffer = io.BytesIO()

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(src=a4_styled_html, dest=pdf_buffer)

    # Check if conversion was successful
    if pisa_status.err:
        raise Exception("HTML to PDF conversion failed")

    # Get the PDF content as bytes and encode to base64
    pdf_buffer.seek(0)
    return base64.b64encode(pdf_buffer.getvalue()).decode("utf-8")
