from data import data


def get_claim_details(sender):
    user_data = data.get(sender, "")
    if not user_data:
        return ["There is no claim registered against your phone number"]
    claims_data = user_data.get("claims", "")
    if not claims_data:
        return ["There is no claim registered against your phone number"]

    claim_message = []
    for claim in claims_data:
        claim_message.append((f"Your claim for {claim['product_name']} is raised on {claim['claim_date']} under claim ID: {claim['id']}. "
                   f"Status of claim is {claim['state'].value}."))
    return claim_message
