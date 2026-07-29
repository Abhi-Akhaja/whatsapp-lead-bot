import { useState, useEffect } from "react";


function App() {

    const [leads, setLeads] = useState([]);
    const [selectedLead, setSelectedLead] = useState(null);
    const [messages, setMessages] = useState([]);
    const [draft, setDraft] = useState("");

    useEffect(() => {
        const fetchLeads = () => {
            fetch(`${import.meta.env.VITE_API_URL}/api/leads`)
                .then((res) => res.json())
                .then((data) => setLeads(data));
        };

        fetchLeads();                                        // Fetch immediately once, without this - user will see leads after 3 seconds
        const intervalId = setInterval(fetchLeads, 3000);    // Poll every 3 seconds

        return () => clearInterval(intervalId);              // Stop polling when component unmounts (navigates page). without clearInterval => when user leaves page and revisit - 2nd interval starts with 1st & then 3rd. 
    }, []);


    const handleSelectLead = (leadId) => {
        setSelectedLead(leadId);
    };

    useEffect(() => {                                        // runs when selectedLead changes
        if (!selectedLead) return;

        const fetchMessages = () => {
            fetch(`${import.meta.env.VITE_API_URL}/api/leads/${selectedLead}/messages`)
                .then((res) => res.json())
                .then((data) => setMessages(data));
        };

        fetchMessages();
        const intervalId = setInterval(fetchMessages, 3000);

        return () => clearInterval(intervalId);
    }, [selectedLead]);                                       // if [selectedLead] present (button click) then start interval for that lead & clear old intervals


    const handleSend = () => {
        if (!draft.trim()) return;
        fetch(`${import.meta.env.VITE_API_URL}/api/leads/${selectedLead}/message`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ body: draft }),
        }).then(() => setDraft(""));
    };


    return (
        <div>
            <h1>Leads</h1>
            <table border="1" cellPadding="8">
                <thead>
                    <tr>
                        <th>Phone</th>
                        <th>Interest</th>
                        <th>Budget</th>
                        <th>Urgency</th>
                        <th>Status</th>
                        <th>Agent</th>
                    </tr>
                </thead>
                <tbody>
                    {leads.map((l) => (
                        <tr
                            key={l.id}
                            onClick={() => handleSelectLead(l.id)}
                            style={{ cursor: "pointer", background: selectedLead === l.id ? "#eef" : "white" }}
                        >
                            <td>{l.phone_number}</td>
                            <td>{l.interest || "—"}</td>
                            <td>{l.budget || "—"}</td>
                            <td>{l.urgency || "—"}</td>
                            <td>{l.current_step}</td>
                            <td>{l.assigned_agent || "—"}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {selectedLead && (
                <div style={{ marginTop: 20 }}>
                    <h2>Conversation</h2>
                    <ul>
                        <div>
                            {messages.map((m) => (
                                <li key={m.id}>
                                    <strong>{m.sender}:</strong> {m.body}
                                </li>
                            ))}
                        </div>
                        <input
                            value={draft}
                            onChange={(e) => setDraft(e.target.value)}
                            onKeyDown={(e) => e.key === "Enter" && handleSend()}
                        />
                        <button onClick={handleSend}>Send</button>
                    </ul>
                </div>
            )}
        </div>
    );
}

export default App;