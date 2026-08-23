import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# --- 1. Generate B2B Clients ---
client_ids = [f"CLI-{str(i).zfill(4)}" for i in range(1, 101)]
tiers = np.random.choice(['Seed', 'Growth', 'Enterprise'], 100, p=[0.5, 0.3, 0.2])
clients = pd.DataFrame({
    'client_id': client_ids,
    'company_name': [f"Company {i}" for i in range(1, 101)],
    'contract_tier': tiers
})
# Force our VIP client for the Loom narrative
clients.loc[0, 'company_name'] = "Global Retail Partners"
clients.loc[0, 'contract_tier'] = "Enterprise"

# --- 2. Generate Inventory Master (Hero vs Zero) ---
skus = [f"SKU-{str(i).zfill(3)}" for i in range(1, 21)]
inventory = pd.DataFrame({
    'sku': skus,
    'product_name': [f"Product {i}" for i in range(1, 21)],
    'unit_cost': np.random.uniform(10, 200, 20).round(2),
    'lead_time_days': np.random.randint(5, 30, 20)
})
# Inject Hero and Zero
inventory.loc[0, 'sku'] = 'SKU-H01' # Hero
inventory.loc[0, 'product_name'] = 'Eco-Packaging Bulk'
inventory.loc[19, 'sku'] = 'SKU-Z99' # Zero
inventory.loc[19, 'product_name'] = 'Premium Display Cases'
inventory.loc[19, 'unit_cost'] = 500.00

# --- 3. Generate 12-Month Sales Orders ---
start_date = datetime(2025, 4, 1)
end_date = datetime(2026, 4, 8)
date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days)]

orders = []
order_id_counter = 1

for current_date in date_range:
    # 10 to 30 orders a day
    num_orders = random.randint(10, 30) 
    for _ in range(num_orders):
        client = random.choice(client_ids)
        
        # Loom Narrative: Stop orders for VIP client in the last 55 days
        if client == "CLI-0001" and (end_date - current_date).days < 55:
            continue 

        # Skew probabilities: Hero product ordered 40% of the time, Zero ordered 1%
        sku = np.random.choice(inventory['sku'], p=[0.4] + [0.59/18]*18 + [0.01])
        
        # Zero product hasn't been ordered in 120 days
        if sku == 'SKU-Z99' and (end_date - current_date).days < 120:
            continue

        orders.append({
            'order_id': f"ORD-{str(order_id_counter).zfill(5)}",
            'client_id': client,
            'order_date': current_date.strftime('%Y-%m-%d'),
            'sku_ordered': sku,
            'quantity': random.randint(50, 500),
            'order_status': 'Completed'
        })
        order_id_counter += 1

orders_df = pd.DataFrame(orders)
orders_df = orders_df.merge(inventory[['sku', 'unit_cost']], left_on='sku_ordered', right_on='sku')
orders_df['total_amount'] = orders_df['quantity'] * orders_df['unit_cost']

# --- 4. Generate Logistics / Shipments ---
shipments = []
for index, row in orders_df.iterrows():
    carrier = np.random.choice(['FedEx', 'DHL', 'Carrier B'], p=[0.4, 0.4, 0.2])
    delay_days = random.randint(0, 2)
    
    # Loom Narrative: Carrier B ruins the VIP client order 60 days ago
    order_date_obj = datetime.strptime(row['order_date'], '%Y-%m-%d')
    if row['client_id'] == 'CLI-0001' and 55 <= (end_date - order_date_obj).days <= 65:
        carrier = 'Carrier B'
        delay_days = 12 # Massive delay

    dispatch_date = order_date_obj + timedelta(days=1)
    promised_date = dispatch_date + timedelta(days=5)
    actual_date = promised_date + timedelta(days=delay_days)

    shipments.append({
        'shipment_id': f"SHP-{row['order_id']}",
        'order_id': row['order_id'],
        'carrier_name': carrier,
        'dispatch_date': dispatch_date.strftime('%Y-%m-%d'),
        'promised_delivery_date': promised_date.strftime('%Y-%m-%d'),
        'actual_delivery_date': actual_date.strftime('%Y-%m-%d'),
    })

shipments_df = pd.DataFrame(shipments)

# --- 5. Export to CSV ---
clients.to_csv('b2b_clients.csv', index=False)
inventory.to_csv('inventory_master.csv', index=False)
orders_df.drop(columns=['sku', 'unit_cost']).to_csv('sales_orders.csv', index=False)
shipments_df.to_csv('logistics_shipments.csv', index=False)

print("12-Month Relational Dataset Generated Successfully.")