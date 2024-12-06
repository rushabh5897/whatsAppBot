from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from get_claim import get_claim_details

# Initialize Flask app
app = Flask(__name__)

# Twilio credentials (from your Twilio Console)
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Your Twilio Sandbox WhatsApp number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Respond to incoming WhatsApp messages
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the incoming message from the request
    incoming_msg = request.values.get('Body', '').lower() or request.json.get('Body', '').lower()
    sender = request.values.get('From', '') or request.json.get('From', '').lower()
    sender = sender.removeprefix("whatsapp:")
    # Create a response object
    response = MessagingResponse()

    # Create the logic for your chatbot
    if 'hello' in incoming_msg:
        response.message('Hello! How can I assist you today?')
    if '2' or 'claim status' in incoming_msg:
        response_list = get_claim_details(sender)
        for res in response_list:
            response.message(res)
    elif 'bye' in incoming_msg:
        response.message('Goodbye! Have a great day!')
    else:
        response.message("Sorry, I didn't understand that. Can you try again?")

    return str(response)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
