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

initial_meals = {
    1: {
        "name": "Spaghetti Bolognese",
        "price": 12
    },
    2: {
        "name": "Chicken Alfredo",
        "price": 15
    },
    3: {
        "name": "Margherita Pizza",
        "price": 10
    },
    4: {
        "name": "Caesar Salad",
        "price": 8
    },
    5: {
        "name": "Beef Stir-Fry",
        "price": 14
    },
    6: {
        "name": "Adana Kebab",
        "price": 20
    },
    7: {
        "name": "Grilled Salmon",
        "price": 18
    },
    8: {
        "name": "Mushroom Risotto",
        "price": 13
    },
    9: {
        "name": "Classic Burger",
        "price": 9
    },
    10: {
        "name": "Chocolate Lava Cake",
        "price": 7
    },
}

DATA = [["Meal Name", "Quantity", "Unit Cost", "Price ($)"]]
meal_dict = {
    meal_id: meal_info["name"]
    for meal_id, meal_info in initial_meals.items()
}
meal_id_counter = max(initial_meals.keys()) + 1
subtotal = 0
discount_visable = 0
discount = 0
tip = 0

discount_codes = ["free", "FREE"]

while True:
  print("Menu:\n")
  for meal_id, meal_info in initial_meals.items():
    print(f"{meal_id}: {meal_info['name']} - ${meal_info['price']}")
  print()

  meal_id_input = input(
      "Please enter the ID of the meal (You can type 'exit' to exit): ")
  print()

  if meal_id_input.lower() == 'exit':
    while True:
      discount_code_input = input(
          "Please enter a discount code or type 'exit' to proceed: ")
      if discount_code_input.lower() == 'exit':
        break
      elif discount_code_input.lower() in discount_codes:
        print(f"Discount applied for {discount_code_input}!")
        discount_visable = 1
        discount_percentage = 0.05
        discount = subtotal * discount_percentage
        print(f"Discount amount: ${int(discount)}")
        break
      else:
        print(
            "Invalid discount code. Please enter a valid code or type 'exit'."
        )

    tip_input = input(
        "Would you like to leave a tip? (Enter the tip amount or '0' for no tip): "
    )
    try:
      tip = int(tip_input)
      if tip < 0:
        print("Invalid tip amount. Please enter a non-negative value.")
      elif tip == 0:
       pass
      else:
        print(f"Tip added: ${tip}")
    except ValueError:
      print(
          "Invalid input. Please enter a valid tip amount or '0' for no tip.")

    tax = (subtotal * 3) / 100
    blank_row = [""]
    subtotal_row = ["Subtotal", "", "", f"${subtotal}"]
    tax_row = ["Tax (%3)", "", "", f"${tax}"]
    total_row = ["Total", "", "", f"${(subtotal - discount) + tax + tip}"]
    DATA.append(blank_row)
    DATA.append(subtotal_row)
    DATA.append(tax_row)
    if discount_visable == 1:
      discount_row = ["Discount (%5)", "", "", f"${discount}"]
      DATA.append(discount_row)
    else:
      pass
    if tip > 0:
      tip_row = ["Tip", "", "", f"${tip}"]
      DATA.append(tip_row)
    else:
      pass
    DATA.append(total_row)
    break

  try:
    meal_id_input = int(meal_id_input)
  except ValueError:
    print("Invalid input. Please enter a valid meal ID.")
    continue

  if meal_id_input not in meal_dict:
    print("Invalid meal ID. Please enter a valid ID from the menu.")
    continue

  meal_name = meal_dict[meal_id_input]
  quantity = input("How Many: ")
  print()

  price = initial_meals[meal_id_input]["price"]

  total_price = int(quantity) * price
  subtotal += total_price

  new_row = [
      f"(#{meal_id_input}) {meal_name}", quantity, f"${price}",
      f"${total_price}"
  ]
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
text = Paragraph("Thanks for visiting Phun Restaurant", text_style)

text_style2 = styles["Normal"]
text_style2.alignment = 0
time = Paragraph(f"Date: {today}", text_style2)

table = Table(DATA, style=style)

spacer = Spacer(1, 20)

pdf.build([time, title, spacer, table, spacer, text])
