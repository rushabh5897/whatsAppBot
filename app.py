import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from get_claim import get_claim_details
from get_warranty import get_warranty_details
from session_history import view_session_history, save_session_to_json, get_last_message

# Initialize Flask app
app = Flask(__name__)

# Twilio credentials (from your Twilio Console)
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
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
    # print("last message :", get_last_message(sender))
    # print("sender", sender)

    menu_message = f"Hello! Welcome to SQTD claims support chatbot. To help us assist you better, please reply with " \
                   f"the number corresponding to your request:!\n* Please choose an option:" \
                   f"\n*1: Warranty Information" \
                   f"\n*2: Check Claim Status" \
                   f"\n*3: File a claim" \
                   f"\n*4: Ask a question" \
                   f"\n*5: Request a Callback" \
                   f"\n*6: Talk to live agent"

    # Create the logic for your chatbot
    if '1' in incoming_msg:
        response_list = get_warranty_details(sender)
        for res in response_list:
            response.message(res)
        response.message(menu_message)

    elif '2' in incoming_msg:
        response_list = get_claim_details(sender)
        for res in response_list:
            response.message(res)
        response.message(menu_message)

    elif '5' in incoming_msg:
        message = "We have notified your request. Our dedicated support team will reach out to you at earliest"
        response.message(message)

    elif '6' in incoming_msg:
        message1 = "We have notified your request. Our dedicated support team will connect with you shortly."
        message2 = "Hello, welcome to SQTD chat support. I am Harry and I will be assisting you today."
        response.message(message1)
        response.message(message2)

    elif 'bye' in incoming_msg:
        response.message('Goodbye! Have a great day!')

    else:
        response.message("Sorry, I didn't understand that. Can you try again?")
        response.message(menu_message)

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
