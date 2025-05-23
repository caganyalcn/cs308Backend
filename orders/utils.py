from reportlab.pdfgen import canvas
import os

def generate_invoice_pdf(order_id, user_email, user_address, items, total_price):
    filename = f"invoice_{order_id}.pdf"
    filepath = os.path.join("invoices", filename)

    os.makedirs("invoices", exist_ok=True)

    c = canvas.Canvas(filepath)
    c.setFont("Helvetica", 14)
    c.drawString(100, 800, "ÇiftlikBank Invoice")
    c.drawString(100, 780, f"User: {user_email}")
    c.drawString(100, 760, f"Order number: {order_id}")
    c.drawString(100, 740, f"Address: {user_address}")

    y = 700
    for item in items:
        c.drawString(100, y, f"{item['name']} x {item['quantity']} - {item['price']} TL")
        y -= 20

    c.drawString(100, y - 20, f"Total: {total_price} TL")
    c.showPage()
    c.save()

    return filepath