import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autohedge.main import AutoHedge

def test_init():
    try:
        AutoHedge(stocks=["AAPL"], output_dir="tests/outputs")
        print("AutoHedge initialized successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")
        raise

if __name__ == "__main__":
    test_init()
