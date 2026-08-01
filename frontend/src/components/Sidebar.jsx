export default function Sidebar({ totalLeads, doneCount }) {
    return (
        <aside className="sidebar">
            <div className="brand">
                <span className="brand-dot" />
                Lead Relay
            </div>
            <div className="stat-grid">
                <div className="stat-card">
                    <div className="stat-value">{totalLeads}</div>
                    <div className="stat-label">Total leads</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value">{doneCount}</div>
                    <div className="stat-label">Qualified</div>
                </div>
            </div>
        </aside>
    );
}