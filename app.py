import os
from dotenv import load_dotenv, find_dotenv
from twilio.twiml.voice_response import VoiceResponse

load_dotenv(find_dotenv())

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from get_claim import get_claim_details
from get_warranty import get_warranty_details
from session_history import view_session_history, save_session_to_json, get_last_message
from google_gemini import generate_llm_response

# Initialize Flask app
app = Flask(__name__)

# Twilio credentials (from your Twilio Console)
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

menu_options = {
    "1": "Warranty Information",
    "2": "Check Claim Status",
    "3": "File a claim",
    "4": "Ask a question",
    "5": "Request a Callback",
    "6": "Talk to live agent",
}


def is_question(message):
    question_keywords = [
        "how",
        "what",
        "why",
        "where",
        "when",
        "can",
        "please",
        "tell",
        "help",
    ]
    message = message.strip().lower()
    return any(keyword in message for keyword in question_keywords) or message.endswith(
        "?"
    )


# Respond to incoming WhatsApp messages
@app.route("/webhook", methods=["POST"])
def webhook():
    # Get the incoming message from the request
    incoming_msg = (
        request.values.get("Body", "").lower() or request.json.get("Body", "").lower()
    )
    sender = request.values.get("From", "") or request.json.get("From", "").lower()
    sender = sender.removeprefix("whatsapp:")

    # Create a response object
    response = MessagingResponse()
    # print("last message :", get_last_message(sender))
    # print("sender", sender)

    menu_message = (
        f"Hello! Welcome to SQTD support chatbot. To help us assist you better, please reply with "
        f"the number corresponding to your request:\n\n"
        f"1️⃣ Warranty Information\n"
        f"2️⃣ Check Claim Status\n"
        f"3️⃣ File a Claim\n"
        f"4️⃣ Ask a Question\n"
        f"5️⃣ Request a Callback\n"
        f"6️⃣ Talk to a Live Agent\n\n"
        f"Reply with the number of your choice to get started!"
    )

    if is_question(incoming_msg):
        user_question = incoming_msg.strip("ask").strip()

        if user_question:
            answer = generate_llm_response(user_question)
            response.message(answer)
        else:
            response.message("Sorry, I couldn't answer your question")

    elif "1" in incoming_msg:
        response_list = get_warranty_details(sender)
        for res in response_list:
            response.message(res)
        response.message(menu_message)

    elif "2" in incoming_msg:
        response_list = get_claim_details(sender)
        for res in response_list:
            response.message(res)
        response.message(menu_message)

    elif "3" in incoming_msg:
        claim_url = "https://squaretrade.com/file-a-claim"
        message = (
            f"You can file a claim using the following link: {claim_url}\n\n"
            f"Click the link to get started."
        )
        response.message(message)
        response.message(menu_message)

    elif "4" in incoming_msg:
        response.message("Please ask your question, and I will help you with it.")

    elif "5" in incoming_msg:
        message = "We have notified your request. Our dedicated support team will reach out to you at earliest"
        response.message(message)

    elif "6" in incoming_msg:
        message1 = "We have notified your request. Our dedicated support team will connect with you shortly."
        message2 = "Hello, welcome to SQTD chat support. I am Harry and I will be assisting you today."
        response.message(message1)
        response.message(message2)

    elif "bye" in incoming_msg:
        response.message("Goodbye! Have a great day!")

    else:
        response.message("Sorry, I didn't understand that. Can you try again?")
        response.message(menu_message)

    save_session_to_json(sender, incoming_msg, response)

    return str(response)


def send_sms(to_phone_number, message):
    """Sends an SMS using Twilio"""
    message = client.messages.create(
        body=message, from_=TWILIO_PHONE_NUMBER, to=to_phone_number
    )
    print(f"Sent message to {to_phone_number}: {message.body}")


@app.route("/missed-call", methods=["POST"])
def missed_call():
    """Handle missed call webhook from Twilio"""
    phone_number = request.form.get("From")  # Extract the phone number of the caller

    message_list = get_claim_details(phone_number)

    # Send SMS with the response
    for response_message in message_list:
        send_sms(phone_number, response_message)

    response = VoiceResponse()
    response.hangup()
    return str(response)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
