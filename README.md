# POS System (CSV-based) — Python CLI Project

A simple **Point-of-Sale (POS) & Delivery Tracking System** built in Python.  
This project uses **CSV files as a lightweight database** to store users, inventory items, and transactions.

---

## Features

### User Features
- Register & login (stored in `users.csv`)
- Browse items by category/subcategory (from `items.csv`)
- Search items by keyword
- Add/remove items in cart
- Checkout & generate receipt
- Apply promotion codes (DIS10, DIS15)
- View transaction history
- Check delivery status using tracking ID
- Update personal details

### Admin Features
- Admin login (key: `admin123`)
- Inventory alerts (low stock < 5)
- Update delivery status for tracking ID
- Generate total sales report
- Generate top sales report

---

## Project Structure

```text
POS-System/
│
├── main.py
├── users.csv
├── items.csv
├── transactions.csv
