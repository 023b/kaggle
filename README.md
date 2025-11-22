# Autonomous Incident-to-Resolution Ops Agent

An agentic system that autonomously detects, diagnoses, and resolves infrastructure incidents in a simulated environment.

## Project Structure
- `dashboard.py`: The main Streamlit application.
- `agents/`: Contains the AI agents (Monitor, Diagnoser, Remediation, Auditor, Safety).
- `simulation/`: Mock infrastructure (Grafana, K8s, Ticketing).
- `notebooks/`: Interactive demos.

## How to Run Locally

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Dashboard**:
    ```bash
    streamlit run dashboard.py
    ```

3.  **Open Browser**:
    The app will open at `http://localhost:8501`.

## How to Deploy for Free

This project is ready for **Streamlit Community Cloud**.

1.  Push this code to a GitHub repository.
2.  Go to [share.streamlit.io](https://share.streamlit.io/).
3.  Connect your GitHub account.
4.  Select your repository and the main file `dashboard.py`.
5.  Click **Deploy**.

## Agents Overview
1. **Monitor**: Watches metrics.
2. **Diagnoser**: Analyzes root cause (simulated LLM).
3. **Safety**: Validates actions.
4. **Remediator**: Fixes the issue.
5. **Auditor**: Manages tickets.
