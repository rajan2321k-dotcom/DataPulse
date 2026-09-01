import pandas as pd


data = {
    "product_id": [101, 102, 103, 104, 105],
    "product": [
        "Laptop",
        "Keyboard",
        "Mouse",
        "Monitor",
        "Headset"
    ],
    "price": [
        55000,
        1200,
        700,
        15000,
        2500
    ],
    "quantity": [
        5,
        20,
        35,
        8,
        15
    ]
}


df = pd.DataFrame(data)

df.to_excel(
    "data/sales.xlsx",
    index=False
)

print("Excel file created successfully.")