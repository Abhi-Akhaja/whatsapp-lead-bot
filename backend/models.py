from db import db

class Agent(db.Model):
    __tablename__ = "agents"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    team = db.Column(db.String(32), nullable=False)

class Lead(db.Model):
    __tablename__ = "leads"
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(120))
    current_step = db.Column(db.String(32), default="start")
    interest = db.Column(db.String(32))
    budget = db.Column(db.String(32))
    urgency = db.Column(db.String(32))
    bot_active = db.Column(db.Boolean, default=True)
    assigned_agent_id = db.Column(db.Integer, db.ForeignKey("agents.id"))
    assigned_agent = db.relationship("Agent")

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    sender = db.Column(db.String(20), default="lead")             # holds lead, bot, agent
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"))
    lead = db.relationship("Lead", backref = "messages")          # lead = db.relationship("Lead", primaryjoin = "Message.lead_id == Lead.id")
