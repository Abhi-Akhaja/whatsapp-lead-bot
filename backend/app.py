from flask import Flask, request, jsonify
from config import Config
from db import db
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from models import Agent, Lead, Message
from routing import assign_agent
from twilio.rest import Client
from config import Config
from ai import classify_reply

app = Flask(__name__)
twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
app.config.from_object(Config)

db.init_app(app)
CORS(app, origins=["http://localhost:5173"])

with app.app_context():
    db.create_all()

@app.route("/api/leads/<int:lead_id>/message", methods=["POST"])                          # for Browser messages
def send_agent_message(lead_id):
    lead = Lead.query.get_or_404(lead_id)         
    data = request.get_json()
    body = data["body"]

    lead.bot_active = False
    db.session.commit()

    twilio_client.messages.create(
        from_=Config.TWILIO_WHATSAPP_NUMBER,
        to=lead.phone_number,
        body=body,
    )

    msg = Message(body=body, lead_id=lead.id, sender="agent")
    db.session.add(msg)
    db.session.commit()

    return jsonify({"id": msg.id, "body": msg.body, "sender": msg.sender}), 201

@app.route("/webhook/whatsapp", methods=["POST"])                  # for twilio - bot messages 
def whatsapp_webhook():
    incoming_body = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")

    lead = Lead.query.filter_by(phone_number=from_number).first()           # creates python object. If this phone number already exists: use the existing lead with his stages. without this - every message creates new row.
    if lead is None:                                                        # If no row exists, then:
        lead = Lead(phone_number=from_number)
        db.session.add(lead)
        db.session.commit()

    msg = Message(body=incoming_body, lead_id=lead.id)
    db.session.add(msg)
    db.session.commit()

    resp = MessagingResponse()

    if not lead.bot_active:
        return str(resp)                                        # send empty response, bot stays silent

    if lead.current_step == "start":
        reply_text = "Hi! What are you interested in?\n1. Buying a product\n2. Getting support"
        lead.current_step = "awaiting_interest"

    elif lead.current_step == "awaiting_interest":
        if incoming_body == "1":
            lead.interest = "product"
            reply_text = "What's your budget?\n1. Under $1,000\n2. $1,000-$5,000\n3. $5,000+"
            lead.current_step = "awaiting_budget"
        elif incoming_body == "2":
            lead.interest = "support"
            reply_text = "Got it, connecting you with support. Someone will reach out shortly."
            lead.current_step = "done"
            assign_agent(lead)
        else:
            classified = classify_reply("awaiting_interest", incoming_body)
            if classified == "product":
                lead.interest = "product"
                reply_text = "What's your budget?\n1. Under $1,000\n2. $1,000-$5,000\n3. $5,000+"
                lead.current_step = "awaiting_budget"
            elif classified == "support":
                lead.interest = "support"
                reply_text = "Got it, connecting you with support. Someone will reach out shortly."
                lead.current_step = "done"
                assign_agent(lead)
            else:
                reply_text = "Please reply with 1 or 2.\n1. Buying a product\n2. Getting support"
                bot_msg = Message(body=reply_text, lead_id=lead.id, sender="bot")
                db.session.add(bot_msg)
                db.session.commit()
                resp.message(reply_text)
                return str(resp)

    elif lead.current_step == "awaiting_budget":
        if incoming_body == "1":
            lead.budget = "under_1k"
        elif incoming_body == "2":
            lead.budget = "1k_5k"
        elif incoming_body == "3":
            lead.budget = "5k_plus"
        else:
            classified = classify_reply("awaiting_budget", incoming_body)
            if classified == "under_1k":
                lead.budget = "under_1k"
            elif classified == "1k_5k":
                lead.budget = "1k_5k"
            elif classified == "5k_plus":
                lead.budget = "5k_plus"
            else:
                reply_text = "Please reply with 1, 2, or 3.\n1. Under $1,000\n2. $1,000-$5,000\n3. $5,000+"
                bot_msg = Message(body=reply_text, lead_id=lead.id, sender="bot")
                db.session.add(bot_msg)
                db.session.commit()
                resp.message(reply_text)
                return str(resp)
        
        reply_text = "How soon are you looking to move forward?\n1. ASAP\n2. This month\n3. Just exploring"
        lead.current_step = "awaiting_urgency"

    elif lead.current_step == "awaiting_urgency":
        if incoming_body == "1":
            lead.urgency = "asap"
        elif incoming_body == "2":
            lead.urgency = "this_month"
        elif incoming_body == "3":
            lead.urgency = "exploring"
        else:
            classified = classify_reply("awaiting_urgency", incoming_body)
            if classified == "asap":
                lead.urgency = "asap"
            elif classified == "this_month":
                lead.urgency = "this_month"
            elif classified == "exploring":
                lead.urgency = "exploring"
            else:
                reply_text = "Please reply with 1, 2, or 3.\n1. ASAP\n2. This month\n3. Just exploring"
                bot_msg = Message(body=reply_text, lead_id=lead.id, sender="bot")
                db.session.add(bot_msg)
                db.session.commit()
                resp.message(reply_text)
                return str(resp)

        reply_text = "Thanks! You're all set — someone from our team will reach out shortly."
        lead.current_step = "done"
        assign_agent(lead)

    else:
        reply_text = "Thanks again — we'll be in touch!"

    bot_msg = Message(body=reply_text, lead_id=lead.id, sender="bot")
    db.session.add(bot_msg)
    db.session.commit()
    resp.message(reply_text)
    return str(resp)

@app.route("/api/leads", methods=["GET"])
def get_leads():
    leads = Lead.query.all()
    return jsonify([
        {
            "id": l.id,
            "phone_number": l.phone_number,
            "name": l.name,
            "interest": l.interest,
            "budget": l.budget,
            "urgency": l.urgency,
            "current_step": l.current_step,
            "assigned_agent": l.assigned_agent.name if l.assigned_agent else None,
        }
        for l in leads
    ])

@app.route("/api/leads/<int:lead_id>/messages", methods=["GET"])
def get_lead_messages(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    return jsonify([
        {"id": m.id, "body": m.body, "sender": m.sender}
        for m in lead.messages
    ])


if __name__ == "__main__":
    app.run(debug=True, port=5000)  
