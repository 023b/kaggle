from typing import List, Dict
from simulation.infrastructure import MockInfrastructure

class DiagnoserAgent:
    """
    Analyzes logs and metrics to find the root cause of an issue.
    In a real scenario, this would call an LLM.
    """
    def __init__(self, infra_client: MockInfrastructure):
        self.infra = infra_client

    def diagnose(self, service_name: str, issues: List[str]) -> Dict:
        """
        Diagnose the root cause based on issues and logs.
        Returns a structured diagnosis.
        """
        print(f"[Diagnoser] Analyzing {service_name} for issues: {issues}")
        
        # Fetch recent logs
        logs = self.infra.get_logs(service_name, lines=20)
        log_text = "\n".join(logs)
        
        # Simple heuristic-based diagnosis (Simulating LLM reasoning)
        diagnosis = {
            "root_cause": "Unknown",
            "recommended_action": "escalate",
            "confidence": 0.0,
            "reasoning": "Could not determine cause from logs."
        }
        
        # Heuristic 1: High CPU/Memory + "Out of Memory" or "GC overhead" in logs
        if any("Memory" in i for i in issues) or any("CPU" in i for i in issues):
            if "OutOfMemoryError" in log_text or "Kill process" in log_text:
                diagnosis = {
                    "root_cause": "Memory Leak / OOM",
                    "recommended_action": "restart_service",
                    "confidence": 0.95,
                    "reasoning": "Logs contain OOM errors and memory usage is high."
                }
            else:
                # Default to scaling if just high load
                diagnosis = {
                    "root_cause": "High Traffic Load",
                    "recommended_action": "scale_up",
                    "confidence": 0.8,
                    "reasoning": "High resource usage without specific errors suggests load spike."
                }

        # Heuristic 2: High Error Rate + "Connection refused"
        if any("Error Rate" in i for i in issues):
            if "Connection refused" in log_text or "Timeout" in log_text:
                diagnosis = {
                    "root_cause": "Dependency Failure",
                    "recommended_action": "restart_service",
                    "confidence": 0.85,
                    "reasoning": "Connection errors in logs indicate stuck connection pool or dependency issue."
                }
        
        print(f"[Diagnoser] Diagnosis: {diagnosis['root_cause']} -> {diagnosis['recommended_action']}")
        return diagnosis
