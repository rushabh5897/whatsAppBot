from data import data


def get_warranty_details(sender):
    user_data = data.get(sender, "")
    product_data = user_data.get("products", "")
    if not user_data or not product_data:
        return ["There is no product purchased for this user"]

    warranty_message = []
    for product in product_data:
        warranty_message.append((f"The product {product['product_name']} with code {product['product_id']}"
                                 f" has a warranty period of {product['warranty_period']}"
                                 f" from the date of purchase {product['purchase_date']}"))
    return warranty_message