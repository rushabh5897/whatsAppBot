from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

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
    incoming_msg = request.form.get('Body', '').lower()
    sender = request.form.get('From')

    # Create a response object
    response = MessagingResponse()

    # Create the logic for your chatbot
    if 'hello' in incoming_msg:
        response.message('Hello! How can I assist you today?')
    elif 'bye' in incoming_msg:
        response.message('Goodbye! Have a great day!')
    else:
        response.message("Sorry, I didn't understand that. Can you try again?")

    return str(response)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
