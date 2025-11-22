import time
from simulation.grafana import MockGrafana
from simulation.infrastructure import MockInfrastructure
from simulation.ticketing import MockTicketing
from agents.monitor import MonitorAgent
from agents.diagnoser import DiagnoserAgent
from agents.remediator import RemediationAgent
from agents.auditor import AuditorAgent
from agents.safety import SafetyLayer

def run_demo():
    print("=== Starting Autonomous Ops Agent Demo ===\n")

    # 1. Initialize Simulation & Agents
    print("--- Initializing System ---")
    grafana = MockGrafana()
    infra = MockInfrastructure()
    ticketing = MockTicketing()

    monitor = MonitorAgent(grafana)
    diagnoser = DiagnoserAgent(infra)
    safety = SafetyLayer()
    remediator = RemediationAgent(infra, safety)
    auditor = AuditorAgent(ticketing)
    
    service_name = "payment-service"
    
    # 2. Normal State Check
    print(f"\n--- Checking {service_name} (Normal State) ---")
    issues = monitor.check_health(service_name)
    if not issues:
        print("Status: Healthy")
    else:
        print(f"Status: Unhealthy ({issues})")

    # 3. Inject Anomaly (Memory Leak)
    print(f"\n--- Injecting Anomaly: High Memory & OOM Logs ---")
    grafana.inject_anomaly(service_name, "memory", 95.0)
    infra.inject_log_error(service_name, "java.lang.OutOfMemoryError: Java heap space")
    
    # 4. Detection
    print(f"\n--- Monitor Agent Scan ---")
    issues = monitor.check_health(service_name)
    if issues:
        print(f"ALERT: Detected {issues}")
        
        # 5. Incident Creation
        print(f"\n--- Auditor Agent: Creating Ticket ---")
        ticket_id = auditor.log_incident(service_name, issues)
        
        # 6. Diagnosis
        print(f"\n--- Diagnoser Agent: Analyzing ---")
        diagnosis = diagnoser.diagnose(service_name, issues)
        auditor.log_diagnosis(ticket_id, diagnosis)
        
        # 7. Remediation
        print(f"\n--- Remediation Agent: Executing Action ---")
        action = diagnosis["recommended_action"]
        success = remediator.remediate(service_name, action)
        auditor.log_action(ticket_id, action, success)
        
        # 8. Final Status
        print(f"\n--- Final Ticket Status ---")
        ticket = ticketing.get_ticket(ticket_id)
        print(f"Ticket ID: {ticket['id']}")
        print(f"Status: {ticket['status']}")
        print("Comments:")
        for c in ticket['comments']:
            print(f" - {c['text']}")

    else:
        print("No issues detected (Unexpected!)")

if __name__ == "__main__":
    run_demo()
