import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import louis

# Register a Braille font with the specified path
braille_font_path = "C:/Users/91620/OneDrive/Desktop/ML/Pandas ai/braille-cc0-font/BrailleCc0-DOeDd.ttf"
pdfmetrics.registerFont(TTFont("Braille", braille_font_path))

def text_to_braille(text):
    # Convert text to Braille using liblouis
    braille = louis.translate(['en-us-g2.ctb'], text)
    return braille[0]

def create_braille_page(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Braille", 12)
    
    # Set initial position
    x, y = 50, 750
    
    for line in text.split('\n'):
        braille_line = text_to_braille(line)
        c.drawString(x, y, braille_line)
        y -= 20  # Move to next line
        
        if y < 50:  # Start a new page if we're near the bottom
            c.showPage()
            y = 750
    
    c.save()

def convert_pdf_to_braille(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()

        if text.strip():  # If there's text on the page
            temp_braille_page = f"temp_braille_page_{page_num}.pdf"
            create_braille_page(text, temp_braille_page)
            
            # Add the Braille page to the output PDF
            braille_reader = PdfReader(temp_braille_page)
            writer.add_page(braille_reader.pages[0])
            
            # Clean up temporary file
            os.remove(temp_braille_page)
        else:
            # If no text (assumed to be an image), add a blank page
            writer.add_blank_page(width=letter[0], height=letter[1])

    # Save the final Braille PDF
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

# Usage
input_pdf = "FeesChallan_bhawanipur.pdf"
output_pdf = "output_braille.pdf"
convert_pdf_to_braille(input_pdf, output_pdf)
