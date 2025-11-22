from simulation.ticketing import MockTicketing

class AuditorAgent:
    """
    Logs all activities and manages the incident ticket.
    """
    def __init__(self, ticketing_client: MockTicketing):
        self.ticketing = ticketing_client

    def log_incident(self, service_name: str, issues: list) -> str:
        """Creates a ticket for the incident."""
        title = f"Incident: {service_name} - {', '.join(issues)}"
        description = f"Detected issues in {service_name}. Initiating automated resolution."
        ticket_id = self.ticketing.create_ticket(title, description, priority="High")
        return ticket_id

    def log_diagnosis(self, ticket_id: str, diagnosis: dict):
        """Updates ticket with diagnosis."""
        comment = (
            f"Diagnosis Complete.\n"
            f"Root Cause: {diagnosis['root_cause']}\n"
            f"Reasoning: {diagnosis['reasoning']}\n"
            f"Recommended Action: {diagnosis['recommended_action']}"
        )
        self.ticketing.update_ticket(ticket_id, comment=comment)

    def log_action(self, ticket_id: str, action: str, success: bool):
        """Updates ticket with action result."""
        status = "Resolved" if success and action != "escalate" else "Escalated"
        if not success:
            status = "Failed"
            
        comment = f"Action Execution: {action}\nResult: {'Success' if success else 'Failed'}"
        self.ticketing.update_ticket(ticket_id, status=status, comment=comment)
