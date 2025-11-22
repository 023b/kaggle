import time
from typing import List, Dict
from simulation.grafana import MockGrafana

class MonitorAgent:
    """
    Watches metrics and detects anomalies.
    """
    def __init__(self, grafana_client: MockGrafana):
        self.grafana = grafana_client
        self.thresholds = {
            "cpu": 80.0,
            "memory": 85.0,
            "latency": 0.5, # seconds
            "error_rate": 0.05 # 5%
        }

    def check_health(self, service_name: str) -> List[str]:
        """
        Checks metrics for a service against thresholds.
        Returns a list of detected issues.
        """
        issues = []
        try:
            metrics = self.grafana.get_all_metrics(service_name)
            
            if metrics["cpu"] > self.thresholds["cpu"]:
                issues.append(f"High CPU usage: {metrics['cpu']:.1f}%")
            
            if metrics["memory"] > self.thresholds["memory"]:
                issues.append(f"High Memory usage: {metrics['memory']:.1f}%")
                
            if metrics["latency"] > self.thresholds["latency"]:
                issues.append(f"High Latency: {metrics['latency']:.3f}s")
                
            if metrics["error_rate"] > self.thresholds["error_rate"]:
                issues.append(f"High Error Rate: {metrics['error_rate']:.1f}%")
                
        except ValueError as e:
            print(f"[Monitor] Error checking {service_name}: {e}")
            
        return issues
