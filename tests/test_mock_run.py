import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set dummy API key for testing
os.environ["OPENAI_API_KEY"] = "dummy_key"


from autohedge.main import AutoHedge

@patch('autohedge.agents.director.TickrAgent')
@patch('autohedge.agents.sentiment.Agent')
@patch('autohedge.agents.execution.Agent')
@patch('autohedge.agents.risk.Agent')
@patch('autohedge.agents.quant.Agent')
@patch('autohedge.agents.director.Agent')
def test_mock_run(mock_dir_agent, mock_quant_agent, mock_risk_agent, mock_exec_agent, mock_sent_agent, mock_tickr):
    # Setup mock returns
    mock_instance = MagicMock()
    mock_instance.run.return_value = "Mocked Response"
    
    mock_dir_agent.return_value = mock_instance
    mock_quant_agent.return_value = mock_instance
    mock_risk_agent.return_value = mock_instance
    mock_exec_agent.return_value = mock_instance
    mock_sent_agent.return_value = mock_instance
    
    mock_tickr_instance = MagicMock()
    mock_tickr_instance.run.return_value = "Mocked Market Data"
    mock_tickr.return_value = mock_tickr_instance

    print("Initializing AutoHedge...")
    hedge = AutoHedge(stocks=["AAPL"], output_dir="tests/outputs")
    
    print("Running mock trade cycle...")
    try:
        hedge.run("Test Task")
        print("Mock run completed successfully.")
    except Exception as e:
        print(f"Mock run failed: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    test_mock_run()
