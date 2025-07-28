import base64

from playwright.async_api import async_playwright


async def create_pdf(html_content: str) -> str:
    """Convert HTML content to PDF bytes and encode as base64 string using Playwright.

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

    # Use async Playwright API
    async with async_playwright() as p:
        # Launch headless Chromium browser
        browser = await p.chromium.launch(headless=True)

        try:
            # Create a new page
            page = await browser.new_page()

            # Set the HTML content
            await page.set_content(a4_styled_html)

            # Generate PDF with A4 format and 2cm margins
            pdf_bytes = await page.pdf(
                format="A4",
                margin={"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"},
                print_background=True,  # Include CSS backgrounds
                scale=1.0,
            )

            # Encode PDF bytes to base64
            return base64.b64encode(pdf_bytes).decode("utf-8")

        finally:
            # Ensure browser is closed
            await browser.close()
