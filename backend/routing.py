from models import Agent, Lead


def assign_agent(lead):
    if lead.interest == "support":
        team = "support"
    elif lead.budget == "5k_plus":
        team = "enterprise"
    else:
        team = "sales"

    agents = Agent.query.filter_by(team=team).all()
    if not agents:
        return

    agent_loads = []
    for agent in agents:
        lead_count = Lead.query.filter_by(assigned_agent_id=agent.id).count()       # counts existing leads of every agent
        agent_loads.append((lead_count, agent))

    agent_loads.sort(key=lambda pair: pair[0])             # tuple => ([0], [1]) -> sort by lead_count
    chosen_agent = agent_loads[0][1]                       # [0] => first position, [1] => first position's agent

    lead.assigned_agent_id = chosen_agent.id