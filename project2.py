import tkinter as tk
from tkinter import messagebox, ttk
from fpdf import FPDF  # For generating PDFs

# Function to calculate the total cost with discount and tax
def calculate_total():
    subtotal = 0
    for item in items:
        subtotal += item['price'] * item['quantity']
    discount = float(entry_discount.get() or 0)
    tax = float(entry_tax.get() or 0)
    total = subtotal - (subtotal * discount / 100)
    total += total * tax / 100
    return subtotal, total

# Function to generate the bill and save it as a .txt or .pdf file
def generate_bill():
    subtotal, total = calculate_total()
    customer_name = entry_customer_name.get()
    customer_phone = entry_customer_phone.get()
    customer_email = entry_customer_email.get()

    bill_content = f"""
--- Bill Receipt ---
Customer Name: {customer_name}
Customer Phone: {customer_phone}
Customer Email: {customer_email}
-------------------
Products:
"""
    for item in items:
        bill_content += f"{item['name']} (x{item['quantity']}): ${item['price'] * item['quantity']:.2f}\n"
    bill_content += f"""
-------------------
Subtotal: ${subtotal:.2f}
Discount: {entry_discount.get()}%
Tax: {entry_tax.get()}%
-------------------
Total: ${total:.2f}
-------------------
"""

    # Save the bill to a .txt file
    with open("bill_receipt.txt", "w") as file:
        file.write(bill_content)

    # Save the bill to a .pdf file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in bill_content.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output("bill_receipt.pdf")

    # Show a confirmation message
    messagebox.showinfo("Bill Saved", "Bill saved as 'bill_receipt.txt' and 'bill_receipt.pdf'")

# Function to add a product to the list
def add_product():
    name = entry_name.get()
    quantity = int(entry_quantity.get())
    price = float(entry_price.get())
    items.append({'name': name, 'quantity': quantity, 'price': price})
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    update_product_list()

# Function to update the product list display
def update_product_list():
    product_list.delete(0, tk.END)
    for item in items:
        product_list.insert(tk.END, f"{item['name']} (x{item['quantity']}) - ${item['price']:.2f} each")

# Function to clear all fields
def clear_fields():
    entry_customer_name.delete(0, tk.END)
    entry_customer_phone.delete(0, tk.END)
    entry_customer_email.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_discount.delete(0, tk.END)
    entry_tax.delete(0, tk.END)
    items.clear()
    update_product_list()

# Initialize the main window
root = tk.Tk()
root.title("Advanced Billing System")
root.geometry("500x600")

# List to store products
items = []

# Customer Details
tk.Label(root, text="Customer Name:").grid(row=0, column=0, padx=10, pady=5)
entry_customer_name = tk.Entry(root)
entry_customer_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Customer Phone:").grid(row=1, column=0, padx=10, pady=5)
entry_customer_phone = tk.Entry(root)
entry_customer_phone.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Customer Email:").grid(row=2, column=0, padx=10, pady=5)
entry_customer_email = tk.Entry(root)
entry_customer_email.grid(row=2, column=1, padx=10, pady=5)

# Product Details
tk.Label(root, text="Product Name:").grid(row=3, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Quantity:").grid(row=4, column=0, padx=10, pady=5)
entry_quantity = tk.Entry(root)
entry_quantity.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Price per Unit:").grid(row=5, column=0, padx=10, pady=5)
entry_price = tk.Entry(root)
entry_price.grid(row=5, column=1, padx=10, pady=5)

# Discount and Tax
tk.Label(root, text="Discount (%):").grid(row=6, column=0, padx=10, pady=5)
entry_discount = tk.Entry(root)
entry_discount.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Tax (%):").grid(row=7, column=0, padx=10, pady=5)
entry_tax = tk.Entry(root)
entry_tax.grid(row=7, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Product", command=add_product).grid(row=8, column=0, columnspan=2, pady=10)
tk.Button(root, text="Generate Bill", command=generate_bill).grid(row=9, column=0, columnspan=2, pady=10)
tk.Button(root, text="Clear All", command=clear_fields).grid(row=10, column=0, columnspan=2, pady=10)

# Product List Display
product_list = tk.Listbox(root, width=50)
product_list.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()