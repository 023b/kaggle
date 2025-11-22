from typing import Dict
from simulation.grafana import MockGrafana

class ValidatorAgent:
    """
    Validates if the service is healthy after an action.
    """
    def __init__(self, grafana_client: MockGrafana):
        self.grafana = grafana_client

    def validate(self, service_name: str) -> bool:
        """
        Returns True if metrics are within safe limits.
        """
        try:
            metrics = self.grafana.get_all_metrics(service_name)
            
            # Stricter validation thresholds
            if metrics["cpu"] > 90.0:
                print(f"[Validator] FAIL: CPU is {metrics['cpu']:.1f}%")
                return False
            if metrics["memory"] > 90.0:
                print(f"[Validator] FAIL: Memory is {metrics['memory']:.1f}%")
                return False
            if metrics["error_rate"] > 0.01:
                print(f"[Validator] FAIL: Error Rate is {metrics['error_rate']:.2f}%")
                return False
                
            print(f"[Validator] PASS: Service {service_name} is healthy.")
            return True
            
        except Exception as e:
            print(f"[Validator] Error during validation: {e}")
            return False
