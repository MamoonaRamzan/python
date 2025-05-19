import csv
import json
import re
from collections import defaultdict, deque

EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
ORDER_ID_REGEX = re.compile(r'^O-\d+$')
PRODUCT_ID_REGEX = re.compile(r'^P\d+$')

def validate_row(row):
    return (EMAIL_REGEX.match(row["customer_email"]) and
            ORDER_ID_REGEX.match(row["order_id"]) and
            PRODUCT_ID_REGEX.match(row["product_id"]))

def process_csv(file_path):
    customers = {}
    total_products_sold = 0
    total_revenue = 0
    product_count = defaultdict(int)
    category_count = defaultdict(int)

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not validate_row(row):
                continue

            cust_id = row["customer_id"]
            order_id = row["order_id"]
            prod_id = row["product_id"]
            quantity = int(row["quantity"])
            unit_price = float(row["unit_price"])
            subtotal = round(quantity * unit_price, 2)

            total_products_sold += quantity
            total_revenue += subtotal
            product_count[row["product_name"]] += quantity
            category_count[row["category"]] += quantity

            if cust_id not in customers:
                customers[cust_id] = {
                    "id": cust_id,
                    "name": row["customer_name"],
                    "email": row["customer_email"],
                    "address": row["shipping_address"],
                    "orders": {},
                }

            if order_id not in customers[cust_id]["orders"]:
                customers[cust_id]["orders"][order_id] = {
                    "id": order_id,
                    "date": row["order_date"],
                    "items": [],
                    "total": 0.0
                }

            order = customers[cust_id]["orders"][order_id]
            order["items"].append({
                "product_id": prod_id,
                "name": row["product_name"],
                "category": row["category"],
                "quantity": quantity,
                "unit_price": unit_price,
                "subtotal": subtotal
            })
            order["total"] = round(order["total"] + subtotal, 2)

    result = {"customers": []}
    total_orders = 0

    for customer in customers.values():
        customer["orders"] = list(customer["orders"].values())
        customer["total_orders"] = len(customer["orders"])
        customer["total_spent"] = round(sum(o["total"] for o in customer["orders"]), 2)
        total_orders += customer["total_orders"]
        result["customers"].append(customer)

    most_popular_product = max(product_count, key=product_count.get, default=None)
    most_popular_category = max(category_count, key=category_count.get, default=None)

    result["metadata"] = {
        "total_customers": len(customers),
        "total_orders": total_orders,
        "total_products_sold": total_products_sold,
        "total_revenue": round(total_revenue, 2),
        "most_popular_product": most_popular_product,
        "most_popular_category": most_popular_category
    }

    return result

def main():
    json_output = process_csv("customer_orders.csv")
    with open("customer_orders.json", "w", encoding='utf-8') as f:
        json.dump(json_output, f, indent=2)
    print("CSV successfully transformed into JSON!")

if __name__ == "__main__":
    main()
