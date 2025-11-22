class SafetyLayer:
    """
    Guardrails to prevent dangerous actions.
    """
    def __init__(self):
        self.allowed_actions = {
            "restart_service",
            "scale_up",
            "clear_cache",
            "escalate" # Always allowed
        }
        self.forbidden_actions = {
            "delete_database",
            "shutdown_cluster",
            "rm_rf_root"
        }

    def validate_action(self, action: str, service_name: str) -> bool:
        """
        Returns True if the action is safe to execute.
        """
        if action in self.forbidden_actions:
            print(f"[Safety] BLOCKED dangerous action: {action} on {service_name}")
            return False
        
        if action in self.allowed_actions:
            print(f"[Safety] Allowed action: {action} on {service_name}")
            return True
            
        print(f"[Safety] Unknown action blocked: {action}")
        return False
