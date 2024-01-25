from datetime import datetime

import pytz
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
  Paragraph,
  SimpleDocTemplate,
  Spacer,
  Table,
  TableStyle,
)

turkey_timezone = pytz.timezone('Europe/Istanbul')
turkey_now = datetime.now(tz=turkey_timezone)
today = turkey_now.strftime("%Y/%m/%d - %H:%M:%S")

DATA = [["List of Items", "Quantity ", "Unit Cost", "Price ($)"]]

subtotal = 0


while True:
  item_name = input("Please enter the name of the meal (You can type 'exit' to exit) : ")
  if item_name.lower() == 'exit':
    blank_row =[""]
    subtotal_row = ["Subtotal", "", "", f"{subtotal}$"]
    tax_row = ["Tax", "", "", f"{(subtotal * 3) / 100}$"]
    total_row = ["Total", "", "", f"{subtotal - ((subtotal * 3) / 100)}$"]
    DATA.append(blank_row)
    DATA.append(subtotal_row)
    DATA.append(tax_row)
    DATA.append(total_row)
    break

  quantity = input("How Many: ")
  price = input("Price: ")
  sum = int(quantity) * int(price)
  subtotal += sum
  

  new_row = [item_name, quantity, price, f"{sum}$"]
  DATA.append(new_row)

pdf = SimpleDocTemplate("receipt.pdf", pagesize=A4)
styles = getSampleStyleSheet()
title_style = styles["Heading1"]
title_style.alignment = 1
title = Paragraph("Phun Restaurant", title_style)
style = TableStyle([
    ("BOX", (0, 0), (-1, -1), 1, colors.black),
    ("GRID", (0, 0), (4, len(DATA)), 1, colors.black),
    ("BACKGROUND", (0, 0), (3, 0), colors.gray),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
])

text_style = styles["Heading3"]
text_style.alignment = 1
text = Paragraph("Thanks for visiting Phun Restaurant ", text_style)

text_style2 = styles["Normal"]
text_style2.alignment = 0
time = Paragraph(f"Date : {today}", text_style2)

table = Table(DATA, style=style)

spacer = Spacer(1, 20)

pdf.build([time, title, table, spacer, text])
