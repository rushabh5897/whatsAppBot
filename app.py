from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from data import data
from get_claim import get_claim_details
from get_warranty import get_warranty_details
from session_history import view_session_history, save_session_to_json, get_last_message

# Initialize Flask app
app = Flask(__name__)

# Twilio credentials (from your Twilio Console)
TWILIO_ACCOUNT_SID = 'ACe6d90ad86a7qqqc7f4e5b1f60b10e4969c2'
TWILIO_AUTH_TOKEN = 'f9f0114945c1f6qwefeqwffdb6a98c00ef3f7125'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+1415qwere5238886'  # Your Twilio Sandbox WhatsApp number
TWILIO_PHONE_NUMBER = '+14155ewr238886'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

menu_options = {
    "1": "Warranty Information",
    "2": "Check Claim Status",
    "3": "File a claim",
    "4": "Ask a question",
    "5": "Request a Callback",
    "6": "Talk to live agent"
}


# Respond to incoming WhatsApp messages
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the incoming message from the request
    incoming_msg = request.values.get('Body', '').lower() or request.json.get('Body', '').lower()
    sender = request.values.get('From', '') or request.json.get('From', '').lower()
    sender = sender.removeprefix("whatsapp:")

    # Create a response object
    response = MessagingResponse()
    print("last message :",get_last_message(sender))

    # Create the logic for your chatbot
    if '1' or 'warranty details' in incoming_msg:
        response_list = get_warranty_details(sender)
        for res in response_list:
            response.message(res)

    elif '2' or 'claim status' in incoming_msg:
        response_list = get_claim_details(sender)
        for res in response_list:
            response.message(res)

    elif 'bye' in incoming_msg:
        response.message('Goodbye! Have a great day!')

    #else:
    #    response.message("Sorry, I didn't understand that. Can you try again?")

    response.message(f"Hello! Welcome to our claims support chatbot. To help us assist you better, please reply with "
                     f"the number corresponding to your request:! Please choose an option:\n{menu_options}")

    save_session_to_json(sender, incoming_msg, response)

    return str(response)



def send_sms(to_phone_number, message):
    """Sends an SMS using Twilio"""
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to_phone_number
    )
    print(f"Sent message to {to_phone_number}: {message.body}")


@app.route('/missed-call', methods=['POST'])
def missed_call():
    """Handle missed call webhook from Twilio"""
    phone_number = request.form.get('From')  # Extract the phone number of the caller

    message_list = get_claim_details(phone_number)

    # Send SMS with the response
    for response_message in message_list:
        send_sms(phone_number, response_message)

    return '', 200  # Return HTTP 200 OK



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
