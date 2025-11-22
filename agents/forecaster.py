from typing import Dict, Optional
from simulation.grafana import MockGrafana

class ForecasterAgent:
    """
    Analyzes metric trends to predict future failures.
    """
    def __init__(self, grafana_client: MockGrafana):
        self.grafana = grafana_client
        self.thresholds = {
            "cpu": 80.0,
            "memory": 85.0,
            "latency": 0.5
        }

    def forecast(self, service_name: str) -> Optional[Dict]:
        """
        Checks if any metric is trending towards a breach.
        Returns a forecast dict if a risk is detected.
        """
        metrics = ["cpu", "memory", "latency"]
        
        for metric in metrics:
            history = self.grafana.get_metric_history(service_name, metric, window_size=10)
            if not history:
                continue
                
            # Simple linear regression slope
            # x = [0, 1, ... n], y = history
            n = len(history)
            if n < 2:
                continue
                
            slope = (history[-1] - history[0]) / n
            
            # If slope is positive and significant
            if slope > 0.1:
                current_val = history[-1]
                limit = self.thresholds.get(metric, 100.0)
                
                # Predict time to breach
                remaining_headroom = limit - current_val
                if remaining_headroom <= 0:
                     # Already breached, let Monitor handle it
                     continue
                     
                steps_to_breach = remaining_headroom / slope
                
                if steps_to_breach < 20: # If breach predicted within 20 ticks
                    print(f"[Forecaster] PREDICTION: {service_name} {metric} will breach in {steps_to_breach:.1f} ticks (Slope: {slope:.2f})")
                    return {
                        "service": service_name,
                        "metric": metric,
                        "predicted_breach_in": steps_to_breach,
                        "current_value": current_val,
                        "slope": slope,
                        "risk_level": "High" if steps_to_breach < 10 else "Medium"
                    }
        
        return None
