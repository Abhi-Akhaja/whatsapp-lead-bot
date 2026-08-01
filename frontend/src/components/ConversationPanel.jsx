import { useState } from "react";

export default function ConversationPanel({ lead, messages, onSend }) {
    const [draft, setDraft] = useState("");

    if (!lead) {
        return (
            <div className="conversation-panel">
                <div className="empty-state">Select a lead to view the conversation.</div>
            </div>
        );
    }

    const handleSend = () => {
        if (!draft.trim()) return;
        onSend(draft.trim());
        setDraft("");
    };

    return (
        <div className="conversation-panel">
            <div className="conversation-header">
                <h2>{lead.phone_number.replace("whatsapp:", "")}</h2>
                {lead.assigned_agent ? (
                    <p className="agent-line">
                        Assigned to <strong>{lead.assigned_agent.name}</strong> · {lead.assigned_agent.team}
                    </p>
                ) : (
                    <p className="agent-line agent-line-unassigned">Not yet assigned</p>
                )}
            </div>
            <div className="message-scroll">
                {messages.map((m) => (
                    <div key={m.id} className={`bubble-row ${m.sender === "lead" ? "lead" : "outbound"}`}>
                        <div className="bubble">{m.body}</div>
                    </div>
                ))}
            </div>
            <div className="composer">
                <input
                    value={draft}
                    onChange={(e) => setDraft(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    placeholder="Reply as agent…"
                />
                <button onClick={handleSend}>Send</button>
            </div>
        </div>
    );
}