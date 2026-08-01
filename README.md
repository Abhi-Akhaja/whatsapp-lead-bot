# Lead Relay — WhatsApp Lead Qualification Bot

A WhatsApp bot that automatically qualifies inbound leads through a short
question flow, routes them to the right team, and gives agents a live CRM
dashboard to manage conversations - built end-to-end from scratch (Flask,
MySQL, React, Twilio, Gemini AI) as a full-stack learning project.

**Live dashboard:** https://wa-chatbot-crm.vercel.app
**Backend API:** https://whatsapp-lead-bot-t07e.onrender.com/


## What it does

1. A lead messages a WhatsApp number and gets walked through 3 qualifying
   questions (interest, budget, urgency) — answered either by tapping a
   numbered option or just typing naturally (free text is classified by
   Gemini AI when it doesn't match a number).
2. Once qualified, the lead is automatically routed to the right team
   (sales / support / enterprise) and assigned to whichever agent on that
   team currently has the fewest active leads.
3. Agents manage everything from a live-updating dashboard - viewing
   conversations, seeing qualification data, and replying manually 
   (which pauses the bot for that conversation).


## Stack

- **Backend:** Flask + SQLAlchemy, deployed on Render
- **Database:** MySQL, hosted on Aiven (SSL-secured)
- **Frontend:** React (Vite), deployed on Vercel
- **Messaging:** Twilio WhatsApp Sandbox
- **AI:** Google Gemini (`gemini-3.6-flash`) for free-text intent classification


## Try it via WhatsApp

The bot is connected to a live Twilio sandbox number. If you'd like to test
it directly rather than just viewing the dashboard:

1. Send `Join organized-guess` to **+1 415 523 8886** from WhatsApp
2. Message it anything to start the qualification flow
3. Watch it appear live on the dashboard above within a few seconds

Note: this is a Twilio *sandbox* number, not a production WhatsApp Business
line - sessions expire after 3 days (you'd need to rejoin).


## Architecture

WhatsApp → Twilio → Flask webhook → MySQL (leads/messages/agents)
↓
Gemini AI (free-text fallback classification)
↓
Rule-based routing + load-balanced agent assignment
↓
React dashboard (polls API, live conversation view)


## Local setup

```bash
# Backend
cd backend
python -m venv venv
Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in your own DB/Twilio/Gemini credentials
python app.py

# Frontend
cd frontend
npm install
cp .env.example .env            # set VITE_API_URL to your backend URL
npm run dev
```