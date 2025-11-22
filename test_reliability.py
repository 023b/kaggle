from simulation.grafana import MockGrafana
from simulation.infrastructure import MockInfrastructure
from agents.forecaster import ForecasterAgent
from agents.planner import PlannerAgent
from agents.validator import ValidatorAgent
from agents.executor import ExecutorAgent
from agents.safety import SafetyLayer

def test_reliability_flow():
    print("=== Testing Reliability Command Agent ===\n")
    
    # Setup
    grafana = MockGrafana()
    infra = MockInfrastructure()
    safety = SafetyLayer()
    validator = ValidatorAgent(grafana)
    executor = ExecutorAgent(infra, safety, validator)
    forecaster = ForecasterAgent(grafana)
    planner = PlannerAgent()
    
    service = "payment-service"
    
    # 1. Inject Trend (Latency increasing)
    print("--- 1. Injecting Latency Trend ---")
    grafana.inject_trend(service, "latency", 0.05)
    
    # Simulate time passing to build history
    print("Simulating 15 ticks...")
    for _ in range(15):
        grafana.get_metric(service, "latency")
        
    # 2. Forecast
    print("\n--- 2. Forecasting ---")
    forecast = forecaster.forecast(service)
    if forecast:
        print(f"SUCCESS: Forecasted breach in {forecast['predicted_breach_in']:.1f} ticks")
    else:
        print("FAIL: No forecast generated")
        return

    # 3. Plan
    print("\n--- 3. Planning ---")
    plan = planner.create_plan(forecast)
    print(f"Plan: {plan}")
    assert "create_snapshot" in plan
    assert "scale_up" in plan
    
    # 4. Execute
    print("\n--- 4. Execution ---")
    success = executor.execute_plan(service, plan)
    if success:
        print("SUCCESS: Plan executed.")
    else:
        print("FAIL: Plan execution failed.")

if __name__ == "__main__":
    test_reliability_flow()
