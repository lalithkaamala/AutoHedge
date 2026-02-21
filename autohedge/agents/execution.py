from typing import Dict
from swarms import Agent
from autohedge.config import settings

EXECUTION_PROMPT = """You are a Trade Execution AI. Your primary objective is to execute trades with precision and accuracy. Your key responsibilities include:

1. **Generating structured order parameters**: Define the essential details of the trade, including the stock symbol, quantity, and price.
2. **Setting precise entry/exit levels**: Determine the exact points at which to enter and exit the trade, ensuring optimal profit potential and risk management.
3. **Determining order types**: Choose the most suitable order type for the trade, such as market order, limit order, or stop-loss order, based on market conditions and trade strategy.
4. **Specifying time constraints**: Define the timeframe for the trade, including the start and end dates, to ensure timely execution and minimize exposure to market volatility.

To execute trades effectively, provide exact trade execution details in a structured format, including:

* Stock symbol and quantity
* Entry and exit prices
* Order type (market, limit, stop-loss, etc.)
* Time constraints (start and end dates, time in force)
* Any additional instructions or special requirements

By following these guidelines, you will ensure that trades are executed efficiently, minimizing potential losses and maximizing profit opportunities.
"""

class ExecutionAgent:
    def __init__(self):
        self.execution_agent = Agent(
            agent_name="Execution-Agent",
            system_prompt=EXECUTION_PROMPT,
            model_name=settings.EXECUTION_MODEL,
            output_type="str",
            max_loops=settings.MAX_LOOPS,
            verbose=settings.VERBOSE,
            context_length=settings.CONTEXT_LENGTH,
        )

    def generate_order(
        self, stock: str, thesis: Dict, risk_assessment: Dict
    ) -> str:
        prompt = f"""
        Stock: {stock}
        Thesis: {thesis}
        Risk Assessment: {risk_assessment}
        
        Generate trade order including:
        1. Order type (market/limit)
        2. Quantity
        3. Entry price
        4. Stop loss
        5. Take profit
        6. Time in force
        """
        order = self.execution_agent.run(prompt)
        return order
