import streamlit as st
import pandas as pd
import altair as alt
import time
from datetime import datetime

# Import Agents
from simulation.grafana import MockGrafana
from simulation.infrastructure import MockInfrastructure
from simulation.ticketing import MockTicketing
from agents.monitor import MonitorAgent
from agents.diagnoser import DiagnoserAgent
from agents.forecaster import ForecasterAgent
from agents.planner import PlannerAgent
from agents.validator import ValidatorAgent
from agents.executor import ExecutorAgent
from agents.safety import SafetyLayer
from agents.auditor import AuditorAgent

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Reliability Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Enterprise Look
st.markdown("""
<style>
    /* Font & Colors */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #f0f2f6;
        font-weight: 600;
    }
    
    /* KPI Cards */
    div[data-testid="metric-container"] {
        background-color: #1e2127;
        border: 1px solid #2e333d;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Terminal Log Window */
    .terminal-window {
        background-color: #0e1117;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #58a6ff;
        height: 350px;
        overflow-y: auto;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    
    /* Status Badges */
    .status-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
    .status-ok { background-color: #238636; color: white; }
    .status-warn { background-color: #9e6a03; color: white; }
    .status-crit { background-color: #da3633; color: white; }
    
</style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'grafana' not in st.session_state:
    st.session_state.grafana = MockGrafana()
    st.session_state.infra = MockInfrastructure()
    st.session_state.ticketing = MockTicketing()
    
    # Agents
    st.session_state.monitor = MonitorAgent(st.session_state.grafana)
    st.session_state.diagnoser = DiagnoserAgent(st.session_state.infra)
    st.session_state.safety = SafetyLayer()
    st.session_state.auditor = AuditorAgent(st.session_state.ticketing)
    st.session_state.forecaster = ForecasterAgent(st.session_state.grafana)
    st.session_state.planner = PlannerAgent()
    st.session_state.validator = ValidatorAgent(st.session_state.grafana)
    st.session_state.executor = ExecutorAgent(
        st.session_state.infra, 
        st.session_state.safety, 
        st.session_state.validator
    )
    
    st.session_state.logs = []
    st.session_state.metrics_history = pd.DataFrame(columns=['Time', 'CPU', 'Memory', 'Latency'])
    st.session_state.status = "HEALTHY"

def log_message(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {msg}")

# --- SIDEBAR ---
st.sidebar.title("COMMAND CENTER")
st.sidebar.markdown("---")
service_name = st.sidebar.selectbox("Target Service", ["payment-service", "auth-service", "database"])

st.sidebar.subheader("Simulation Controls")
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    if st.button("Inject Leak", type="primary", use_container_width=True):
        st.session_state.grafana.inject_anomaly(service_name, "memory", 95.0)
        st.session_state.infra.inject_log_error(service_name, "java.lang.OutOfMemoryError: Java heap space")
        log_message(f"⚠️ INJECTED: Memory Leak -> {service_name}")
        st.rerun()

with col_s2:
    if st.button("Inject Trend", use_container_width=True):
        st.session_state.grafana.inject_trend(service_name, "latency", 0.05)
        log_message(f"📈 INJECTED: Latency Trend -> {service_name}")
        st.rerun()

if st.sidebar.button("Reset System", use_container_width=True):
    st.session_state.grafana.clear_anomalies()
    st.session_state.status = "HEALTHY"
    log_message(f"♻️ SYSTEM RESET: {service_name}")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("v2.0.0 | Reliability Command Agent")

# --- MAIN DASHBOARD ---
st.title("Reliability Command Center")

# 1. KPI ROW
metrics = st.session_state.grafana.get_all_metrics(service_name)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("CPU Usage", f"{metrics['cpu']:.1f}%", delta=f"{metrics['cpu']-15:.1f}%", delta_color="inverse")
with kpi2:
    st.metric("Memory Usage", f"{metrics['memory']:.1f}%", delta=f"{metrics['memory']-40:.1f}%", delta_color="inverse")
with kpi3:
    st.metric("Latency", f"{metrics['latency']:.3f}s", delta=f"{metrics['latency']-0.05:.3f}s", delta_color="inverse")
with kpi4:
    status_color = "green" if st.session_state.status == "HEALTHY" else "red"
    st.markdown(f"""
    <div style="text-align: center; padding: 10px; background-color: #1e2127; border-radius: 8px; border: 1px solid #2e333d;">
        <div style="font-size: 14px; color: #8b949e;">System Status</div>
        <div style="font-size: 24px; font-weight: bold; color: {status_color};">{st.session_state.status}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 2. MAIN CONTENT
col_main, col_logs = st.columns([2, 1])

with col_main:
    st.subheader("Real-time Telemetry")
    
    # RUN CYCLE BUTTON
    if st.button("⚡ Run Agent Cycle", type="primary"):
        # 1. Metrics
        new_row = {
            'Time': datetime.now(),
            'CPU': metrics['cpu'],
            'Memory': metrics['memory'],
            'Latency': metrics['latency'] * 100
        }
        st.session_state.metrics_history = pd.concat([
            st.session_state.metrics_history, 
            pd.DataFrame([new_row])
        ]).tail(40)
        
        # 2. FORECAST
        forecast = st.session_state.forecaster.forecast(service_name)
        if forecast:
            st.session_state.status = "PREDICTED FAILURE"
            log_message(f"🔮 FORECAST: {forecast['metric']} breach in {forecast['predicted_breach_in']:.1f} ticks")
            plan = st.session_state.planner.create_plan(forecast)
            log_message(f"📋 PLAN: {plan}")
            success = st.session_state.executor.execute_plan(service_name, plan)
            if success:
                log_message("✅ MITIGATION: Success")
                st.session_state.grafana.clear_anomalies()
                st.session_state.status = "HEALTHY"
            else:
                log_message("❌ MITIGATION: Failed (Rolled Back)")

        # 3. MONITOR
        issues = st.session_state.monitor.check_health(service_name)
        if issues and not forecast:
            st.session_state.status = "CRITICAL"
            log_message(f"🚨 ALERT: {issues}")
            ticket_id = st.session_state.auditor.log_incident(service_name, issues)
            diagnosis = st.session_state.diagnoser.diagnose(service_name, issues)
            st.session_state.auditor.log_diagnosis(ticket_id, diagnosis)
            log_message(f"🧠 DIAGNOSIS: {diagnosis['root_cause']}")
            plan = st.session_state.planner.create_plan(diagnosis)
            success = st.session_state.executor.execute_plan(service_name, plan)
            st.session_state.auditor.log_action(ticket_id, str(plan), success)
            
            if success:
                log_message(f"✅ RESOLVED: {diagnosis['recommended_action']}")
                if "restart_service" in plan:
                    st.session_state.grafana.clear_anomalies()
                st.session_state.status = "HEALTHY"
            else:
                log_message(f"❌ FAILED: Resolution unsuccessful")
        
        if not issues and not forecast:
             st.session_state.status = "HEALTHY"

    # CHARTS
    if not st.session_state.metrics_history.empty:
        chart_data = st.session_state.metrics_history.melt('Time', var_name='Metric', value_name='Value')
        
        # Area Chart with Gradient
        chart = alt.Chart(chart_data).mark_area(
            line={'color':'darkblue'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='darkblue', offset=0),
                       alt.GradientStop(color='rgba(0,0,0,0)', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            )
        ).encode(
            x='Time:T',
            y='Value:Q',
            color='Metric:N',
            tooltip=['Time', 'Metric', 'Value']
        ).properties(height=350).interactive()
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("System initialized. Waiting for telemetry...")

with col_logs:
    st.subheader("Live Audit Log")
    log_html = "<div class='terminal-window'>"
    for log in reversed(st.session_state.logs):
        color = "#58a6ff" # Blue
        if "ALERT" in log or "❌" in log: color = "#ff7b72" # Red
        if "✅" in log or "RESOLVED" in log: color = "#3fb950" # Green
        if "FORECAST" in log: color = "#d2a8ff" # Purple
        
        log_html += f"<div style='color: {color}; margin-bottom: 4px; border-bottom: 1px solid #21262d;'>{log}</div>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)

# 3. TICKETS
st.subheader("Active Incidents")
tickets = st.session_state.ticketing.tickets
if tickets:
    df_tickets = pd.DataFrame.from_dict(tickets, orient='index')
    st.dataframe(
        df_tickets[['id', 'title', 'status', 'priority', 'created_at']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "status": st.column_config.SelectboxColumn(
                "Status",
                help="Ticket Status",
                options=["Open", "Resolved", "Escalated", "Failed"],
                required=True,
            )
        }
    )
else:
    st.markdown("<div style='color: #8b949e; font-style: italic;'>No active incidents. System operating normally.</div>", unsafe_allow_html=True)
