import random
import time
from typing import Dict, List, Optional

class MockGrafana:
    """
    Simulates a Grafana/Prometheus metrics API.
    Stores in-memory metrics for services.
    """
    def __init__(self):
        self.metrics_store = {
            "payment-service": {"cpu": 15.0, "memory": 40.0, "latency": 0.05, "error_rate": 0.0},
            "auth-service": {"cpu": 10.0, "memory": 30.0, "latency": 0.02, "error_rate": 0.0},
            "database": {"cpu": 25.0, "memory": 60.0, "latency": 0.01, "error_rate": 0.0},
        }
        self.anomalies = {}

    def get_metric(self, service_name: str, metric_name: str) -> float:
        """
        Get a specific metric for a service.
        Adds some random noise to make it look real.
        """
        if service_name not in self.metrics_store:
            raise ValueError(f"Service {service_name} not found")
        
        base_value = self.metrics_store[service_name].get(metric_name, 0.0)
        
        # Check if there's an active anomaly injection
        if service_name in self.anomalies and metric_name in self.anomalies[service_name]:
            return self.anomalies[service_name][metric_name]
        
        # Add noise
        noise = random.uniform(-0.1 * base_value, 0.1 * base_value)
        return max(0.0, base_value + noise)

    def get_all_metrics(self, service_name: str) -> Dict[str, float]:
        """Get all metrics for a service."""
        if service_name not in self.metrics_store:
            raise ValueError(f"Service {service_name} not found")
        
        return {
            k: self.get_metric(service_name, k)
            for k in self.metrics_store[service_name]
        }

    def inject_anomaly(self, service_name: str, metric_name: str, value: float):
        """Inject a static value to simulate an anomaly."""
        if service_name not in self.anomalies:
            self.anomalies[service_name] = {}
        self.anomalies[service_name][metric_name] = value
        print(f"[Grafana] Injected anomaly: {service_name} {metric_name} = {value}")

    def inject_trend(self, service_name: str, metric_name: str, slope: float):
        """Inject a growing trend (e.g., +0.1 per call)."""
        if service_name not in self.anomalies:
            self.anomalies[service_name] = {}
        # Store trend as a dict with 'slope' and 'start_value'
        current_val = self.metrics_store[service_name].get(metric_name, 0.0)
        self.anomalies[service_name][metric_name] = {"type": "trend", "slope": slope, "value": current_val}
        print(f"[Grafana] Injected trend: {service_name} {metric_name} slope={slope}")

    def get_metric(self, service_name: str, metric_name: str) -> float:
        """
        Get a specific metric for a service.
        Adds some random noise to make it look real.
        """
        if service_name not in self.metrics_store:
            raise ValueError(f"Service {service_name} not found")
        
        base_value = self.metrics_store[service_name].get(metric_name, 0.0)
        
        # Check if there's an active anomaly injection
        if service_name in self.anomalies and metric_name in self.anomalies[service_name]:
            anomaly = self.anomalies[service_name][metric_name]
            if isinstance(anomaly, dict) and anomaly.get("type") == "trend":
                # Update trend value
                anomaly["value"] += anomaly["slope"]
                return anomaly["value"]
            elif isinstance(anomaly, (int, float)):
                return float(anomaly)
        
        # Add noise
        noise = random.uniform(-0.1 * base_value, 0.1 * base_value)
        return max(0.0, base_value + noise)

    def get_metric_history(self, service_name: str, metric_name: str, window_size: int = 10) -> List[float]:
        """
        Returns a list of historical data points (simulated).
        If a trend is active, returns points following that trend.
        """
        current = self.get_metric(service_name, metric_name)
        history = []
        
        # Check for trend to generate consistent history
        slope = 0
        if service_name in self.anomalies and metric_name in self.anomalies[service_name]:
            anomaly = self.anomalies[service_name][metric_name]
            if isinstance(anomaly, dict) and anomaly.get("type") == "trend":
                slope = anomaly["slope"]

        # Generate history backwards
        for i in range(window_size):
            val = current - (slope * i)
            noise = random.uniform(-0.05 * val, 0.05 * val) if val > 0 else 0
            history.insert(0, max(0.0, val + noise))
            
        return history

    def clear_anomalies(self):
        """Clear all injected anomalies."""
        self.anomalies = {}
        print("[Grafana] Cleared all anomalies")
