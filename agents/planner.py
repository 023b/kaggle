from typing import List, Dict

class PlannerAgent:
    """
    Generates multi-step mitigation plans based on forecasts or diagnoses.
    """
    def create_plan(self, context: Dict) -> List[str]:
        """
        Context can be a 'forecast' or a 'diagnosis'.
        Returns a list of action steps.
        """
        plan = []
        
        # Scenario 1: Proactive (Forecast)
        if "predicted_breach_in" in context:
            metric = context.get("metric")
            print(f"[Planner] Generating PROACTIVE plan for {metric} trend...")
            
            plan.append("create_snapshot") # Safety first
            
            if metric == "memory":
                # Proactive restart usually clears memory leaks
                plan.append("restart_service")
            elif metric == "cpu" or metric == "latency":
                # Scale up to handle load
                plan.append("scale_up")
                
            plan.append("validate_health")
            
        # Scenario 2: Reactive (Diagnosis)
        elif "root_cause" in context:
            cause = context.get("root_cause")
            print(f"[Planner] Generating REACTIVE plan for {cause}...")
            
            plan.append("create_snapshot")
            
            if "Memory" in cause:
                plan.append("restart_service")
            elif "Load" in cause:
                plan.append("scale_up")
            else:
                plan.append("escalate")
                
            plan.append("validate_health")
            
        return plan
