from typing import List
from simulation.infrastructure import MockInfrastructure
from agents.safety import SafetyLayer
from agents.validator import ValidatorAgent

class ExecutorAgent:
    """
    Executes a multi-step plan with rollback capabilities.
    """
    def __init__(self, infra_client: MockInfrastructure, safety_layer: SafetyLayer, validator: ValidatorAgent):
        self.infra = infra_client
        self.safety = safety_layer
        self.validator = validator
        self.active_snapshot = None

    def execute_plan(self, service_name: str, plan: List[str]) -> bool:
        """
        Executes steps in order. Rolls back on failure.
        """
        print(f"[Executor] Starting execution of plan: {plan}")
        
        for step in plan:
            success = self._execute_step(service_name, step)
            if not success:
                print(f"[Executor] Step {step} failed. Initiating ROLLBACK.")
                self._rollback(service_name)
                return False
                
        print("[Executor] Plan executed successfully.")
        return True

    def _execute_step(self, service_name: str, step: str) -> bool:
        if step == "create_snapshot":
            self.active_snapshot = self.infra.create_snapshot(service_name)
            return True
            
        if step == "validate_health":
            return self.validator.validate(service_name)
            
        # Standard Actions
        if not self.safety.validate_action(step, service_name):
            return False
            
        if step == "restart_service":
            self.infra.restart_pod(service_name)
            return True
            
        elif step == "scale_up":
            status = self.infra.get_pod_status(service_name)
            current = status.get("replicas", 1)
            self.infra.scale_deployment(service_name, current + 1)
            return True
            
        elif step == "escalate":
            print("[Executor] Escalating to human.")
            return True
            
        return False

    def _rollback(self, service_name: str):
        if self.active_snapshot:
            print(f"[Executor] Rolling back to snapshot {self.active_snapshot}...")
            self.infra.restore_snapshot(self.active_snapshot)
            self.active_snapshot = None
        else:
            print("[Executor] No snapshot available for rollback!")
