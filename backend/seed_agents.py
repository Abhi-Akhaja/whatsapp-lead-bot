from app import app
from db import db
from models import Agent

with app.app_context():
    if Agent.query.count() > 0:
        print("Agents already exist — skipping seed.")
    else:
        db.session.add_all([
            Agent(name="Nandini Sanepara", team="sales"),
            Agent(name="Sarju Ramani", team="sales"),
            Agent(name="Meet Bhalani", team="support"),
            Agent(name="Vikas Nair", team="support"),
            Agent(name="Milan Lathiya", team="enterprise"),
        ])
        db.session.commit()
        print("Agents seeded.")