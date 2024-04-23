from flask import Flask, request, jsonify
import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

# Twilio credentials
account_sid = 'AC3966004769cab3bcb7ecfe147cdd28d5'
auth_token = '9b8dec70f9c1b0aa525f52adc9de3a02'
twilio_number = 'whatsapp:+14155238886'

# ChatGPT model and tokenizer
model = GPT2LMHeadModel.from_pretrained("microsoft/DialoGPT-large")
tokenizer = GPT2Tokenizer.from_pretrained("microsoft/DialoGPT-large")

# Twilio client
client = Client(account_sid, auth_token)

# Generate response using ChatGPT
def generate_response(message):
    input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors="pt")
    response_ids = model.generate(input_ids, max_length=1000, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_message = request.values.get('Body', '')
    sender_number = request.values.get('From', '')

    # Generate response using ChatGPT
    response_message = generate_response(incoming_message)

    # Sending a reply message
    client.messages.create(
        from_=twilio_number,
        body=response_message,
        to=sender_number
    )

    return ('', 200)

if __name__ == '__main__':
    app.run(debug=True)
