function StatusPill({ status }) {
    const isDone = status === "done";
    return (
        <span className={`status-pill ${isDone ? "status-done" : "status-progress"}`}>
            {isDone ? "qualified" : status.replace("awaiting_", "")}
        </span>
    );
}

export default function LeadList({ leads, selectedId, onSelect }) {
    return (
        <div className="queue-column">
            <div className="queue-header">
                <h1>Leads</h1>
                <p>{leads.length} conversation{leads.length === 1 ? "" : "s"}</p>
            </div>
            <div className="queue-list">
                {leads.map((l) => (
                    <div
                        key={l.id}
                        className={`lead-card ${selectedId === l.id ? "selected" : ""}`}
                        onClick={() => onSelect(l.id)}
                    >
                        <div className="lead-top-row">
                            <span className="lead-phone">{l.phone_number.replace("whatsapp:", "")}</span>
                            <StatusPill status={l.current_step} />
                        </div>
                        <div className="lead-meta-row">
                            {l.interest && <span className="tag">{l.interest}</span>}
                            {l.budget && <span className="tag">{l.budget}</span>}
                            {l.assigned_agent && <span className="agent-tag">{l.assigned_agent.name}</span>}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}