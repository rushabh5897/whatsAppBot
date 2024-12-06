from enum import Enum

class ClaimStatus(Enum):
    FILED = "Filed/Reported"
    UNDER_REVIEW = "Under Review"
    PENDING = "Pending"
    APPROVED = "Approved"
    DENIED = "Denied/Rejected"
    SETTLED = "Settled"
    PAID = "Paid"
    CLOSED = "Closed"
    REOPENED = "Reopened"
    AWAITING_INFORMATION = "Awaiting Information"
    IN_LITIGATION = "In Litigation"
    CANCELED = "Canceled"
    PAID_TO_THIRD_PARTY = "Paid to Third Party"
    ESCALATED = "Escalated"


data = {
    "+919421342134": {
        "name": "Rushabh Sancheti",
        "products": [
            {
             "product_id": "ABCD1234",
             "product_name": "iPHONE 15 PRO",
             "purchase_date": "2023-12-01",
             "warranty_period": "2 years"
            },
            {
                "product_id": "ABRY1A34C",
                "product_name": "Macbook Pro",
                "purchase_date": "2024-01-01",
                "warranty_period": "1 years"
            }
        ],
        "claims":
        [
            {
             "id": "cl111",
             "product_id": "ABCD1234",
             "product_name": "iPHONE 15 PRO",
             "claim_date": "2023-12-01",
             "state": ClaimStatus.UNDER_REVIEW
            },
{
             "id": "cl113",
            "product_id": "ABRY1A34C",
            "product_name": "Macbook Pro",
             "claim_date": "2024-10-01",
             "state": ClaimStatus.APPROVED
            }
        ]
    }

}
