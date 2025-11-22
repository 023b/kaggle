import time
from typing import Dict, List

class MockInfrastructure:
    """
    Simulates a Kubernetes/Docker environment.
    Manages pod states and logs.
    """
    def __init__(self):
        self.pods = {
            "payment-service": {"status": "Running", "replicas": 2, "version": "v1.2.0"},
            "auth-service": {"status": "Running", "replicas": 3, "version": "v1.1.5"},
            "database": {"status": "Running", "replicas": 1, "version": "postgres:14"},
        }
        self.logs = {
            "payment-service": [
                "INFO: Payment processed successfully",
                "INFO: Health check passed",
            ],
            "auth-service": [
                "INFO: User logged in",
                "INFO: Token refreshed",
            ],
            "database": [
                "INFO: Connection accepted",
                "INFO: Query executed",
            ]
        }

    def get_pod_status(self, service_name: str) -> Dict:
        return self.pods.get(service_name, {"status": "Unknown"})

    def get_logs(self, service_name: str, lines: int = 10) -> List[str]:
        return self.logs.get(service_name, [])[-lines:]

    def restart_pod(self, service_name: str):
        """Simulate a pod restart."""
        print(f"[Infra] Restarting {service_name}...")
        self.pods[service_name]["status"] = "Restarting"
        time.sleep(1) # Simulate delay
        self.pods[service_name]["status"] = "Running"
        self.logs[service_name].append("INFO: Service restarted successfully")
        print(f"[Infra] {service_name} is back online.")

    def scale_deployment(self, service_name: str, replicas: int):
        """Simulate scaling a deployment."""
        print(f"[Infra] Scaling {service_name} to {replicas} replicas...")
        self.pods[service_name]["replicas"] = replicas
        self.logs[service_name].append(f"INFO: Scaled to {replicas} replicas")

    def create_snapshot(self, service_name: str) -> str:
        """Save the current state of a service."""
        import copy
        import uuid
        snapshot_id = str(uuid.uuid4())[:8]
        if not hasattr(self, 'snapshots'):
            self.snapshots = {}
        
        self.snapshots[snapshot_id] = {
            "service": service_name,
            "state": copy.deepcopy(self.pods.get(service_name))
        }
        print(f"[Infra] Created snapshot {snapshot_id} for {service_name}")
        return snapshot_id

    def restore_snapshot(self, snapshot_id: str) -> bool:
        """Restore a service to a saved state."""
        if not hasattr(self, 'snapshots') or snapshot_id not in self.snapshots:
            print(f"[Infra] Snapshot {snapshot_id} not found.")
            return False
            
        snapshot = self.snapshots[snapshot_id]
        service_name = snapshot["service"]
        self.pods[service_name] = snapshot["state"]
        print(f"[Infra] Restored {service_name} from snapshot {snapshot_id}")
        self.logs[service_name].append(f"WARN: Rolled back to snapshot {snapshot_id}")
        return True

    def inject_log_error(self, service_name: str, error_msg: str):
        """Inject an error log."""
        if service_name in self.logs:
            self.logs[service_name].append(f"ERROR: {error_msg}")
