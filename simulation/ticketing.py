import uuid
from datetime import datetime
from typing import Dict, List

class MockTicketing:
    """
    Simulates a ticketing system like Jira or ServiceNow.
    """
    def __init__(self):
        self.tickets = {}

    def create_ticket(self, title: str, description: str, priority: str = "Medium") -> str:
        ticket_id = f"TICKET-{len(self.tickets) + 1001}"
        self.tickets[ticket_id] = {
            "id": ticket_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "Open",
            "created_at": datetime.now().isoformat(),
            "comments": []
        }
        print(f"[Ticketing] Created ticket {ticket_id}: {title}")
        return ticket_id

    def update_ticket(self, ticket_id: str, status: str = None, comment: str = None):
        if ticket_id not in self.tickets:
            raise ValueError(f"Ticket {ticket_id} not found")
        
        if status:
            self.tickets[ticket_id]["status"] = status
            print(f"[Ticketing] Updated {ticket_id} status to {status}")
        
        if comment:
            self.tickets[ticket_id]["comments"].append({
                "timestamp": datetime.now().isoformat(),
                "text": comment
            })
            print(f"[Ticketing] Added comment to {ticket_id}: {comment}")

    def get_ticket(self, ticket_id: str) -> Dict:
        return self.tickets.get(ticket_id)
