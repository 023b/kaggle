from simulation.infrastructure import MockInfrastructure
from agents.safety import SafetyLayer

class RemediationAgent:
    """
    Executes the recommended action if it passes safety checks.
    """
    def __init__(self, infra_client: MockInfrastructure, safety_layer: SafetyLayer):
        self.infra = infra_client
        self.safety = safety_layer

    def remediate(self, service_name: str, action: str) -> bool:
        """
        Executes the action. Returns True if successful.
        """
        print(f"[Remediator] Received request to {action} on {service_name}")
        
        if not self.safety.validate_action(action, service_name):
            print("[Remediator] Action failed safety check.")
            return False

        try:
            if action == "restart_service":
                self.infra.restart_pod(service_name)
                return True
            
            elif action == "scale_up":
                # Get current replicas and add 1
                status = self.infra.get_pod_status(service_name)
                current_replicas = status.get("replicas", 1)
                self.infra.scale_deployment(service_name, current_replicas + 1)
                return True
            
            elif action == "escalate":
                print("[Remediator] Escalating to human operator (no auto-fix available).")
                return True
                
            else:
                print(f"[Remediator] Action {action} not implemented.")
                return False
                
        except Exception as e:
            print(f"[Remediator] Execution failed: {e}")
            return False
