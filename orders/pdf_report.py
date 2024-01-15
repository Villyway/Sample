from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import *
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import datetime

def draw_text_with_line_breaks(c, text, x, y, font, font_size, line_height):
    c.setFont(font, font_size)
    lines = text.split('\n')
    for line in lines:
        c.drawString(x, y, line)
        y -= line_height

def generate_order_confirmation_pdf(file_path, report_details):
    # Create a canvas
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFillColor(colors.HexColor("#FFA500"))  # Set the fill color
    # c.setStrokeColor(colors.HexColor("#FFA500"))  # Set the border color if needed
    c.rect(0, 740, 700, 60, stroke=0, fill=1)  
    # c.rect(0, 740, 700, 60, stroke=0, fill=1, fillColor=colors.HexColor("#FFA500"))
    # c.rect(50, 50, 300, 100, fill=1)
    # c.
    c.setFillColor(colors.HexColor("#000000"))
    # Set company name
    company_name =  report_details['header_title'] #"BasuriAutomotive"
    c.setFont("Helvetica", 16)
    c.drawCentredString(letter[0] / 2, letter[1] - 30, company_name, )

    title_name = report_details['report_subject'] #"Order Details"
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(letter[0] / 2, letter[1] - 70, title_name, )

    # c.drawInlineImage("logo.png", x=100, y=700, width=100, height=60)
    c.drawImage("logo.png", x=220, y=755, width=25, height=25, preserveAspectRatio=True, anchor='sw', mask='auto')

    # Draw horizontal line below title
    c.line(50, letter[1] - 55, letter[0] - 50, letter[1] - 55)
    draw_text_with_line_breaks(c, "Date:- " + report_details['date'] , 50, letter[1] - 85, "Helvetica", 8, 12) #str(datetime.date.today().strftime("%d/%m/%Y")
    draw_text_with_line_breaks(c, "Order No.:- " + report_details['order_no'] , 400, letter[1] - 85, "Helvetica", 8, 12) # KISO000128

    # Billing and Shipping address
    
    billing_address = report_details['billing_address'] #"123 Billing Street\nCity, Country\nZIP Code"
    shipping_address = report_details['shipping_address']  #"456 Shipping Street\nCity, Country\nZIP Code"

    draw_text_with_line_breaks(c, "Billing Address:-", 50, letter[1] - 100, "Helvetica-Bold", 8, 11)
    draw_text_with_line_breaks(c, "Shipping Address:-", letter[0] / 1.5, letter[1] - 100, "Helvetica-Bold", 8, 11)

    # For Shipping Address
    draw_text_with_line_breaks(c, billing_address, 50, letter[1] - 120, "Helvetica", 8, 10)
    draw_text_with_line_breaks(c, shipping_address, letter[0] / 1.5, letter[1] - 120, "Helvetica", 8, 10)

    # Create a table for product list
    product_data = [
        ["Product Name", "Quantity", "Price"],
        ["Product 1", "2", "$50"],
        ["Product 2", "1", "$30"],
        # Add more product rows as needed
    ]

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    product_table = Table(product_data)
    product_table.setStyle(table_style)

    # Get the width and height of the table
    width, height = product_table.wrap(0, 0)

    # Position the table on the page
    product_table.drawOn(c, 200, letter[1] - 180 - height)

    c.line(50, letter[1] - 750, letter[0] - 50, letter[1] - 750)

    basuri_address = "Address:- 23/24/25/26 SHREEJI INDUSTRIES, B/H UDHYOG NAGER, KAMREJ CHAR RASTA, \nSURAT - 394185 India, Mail:- sales@basuriautomotive.com, Phone:- +91 7259163815"
    draw_text_with_line_breaks(c, basuri_address, 50, letter[1] - 765, "Helvetica", 12, 14)

    # Save the PDF file
    c.save()

# Generate the PDF
generate_order_confirmation_pdf("order_confirmation.pdf")