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
                    margin: 0;
                }}
                body {{
                    width: 100%;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 1cm;
                    box-sizing: border-box;
                }}
                table {{
                    width: 100%;
                    margin-bottom: 1em;
                    border-collapse: collapse;
                    font-size: 12px;
                    table-layout: fixed;
                }}
                td, th {{
                    padding: 4px;
                    word-wrap: break-word;
                    word-break: break-word;
                    overflow-wrap: break-word;
                    hyphens: auto;
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

            # Generate PDF with A4 format and no margins (handled by CSS)
            pdf_bytes = await page.pdf(
                format="A4",
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                print_background=True,  # Include CSS backgrounds
                scale=1.0,
            )

            # Encode PDF bytes to base64
            return base64.b64encode(pdf_bytes).decode("utf-8")

        finally:
            # Ensure browser is closed
            await browser.close()
