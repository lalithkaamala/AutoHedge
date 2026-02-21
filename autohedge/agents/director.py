from typing import List
from swarms import Agent
from tickr_agent.main import TickrAgent
from autohedge.config import settings

DIRECTOR_PROMPT = """
You are a Trading Director AI, responsible for orchestrating the trading process. 

Your primary objectives are:
1. Conduct in-depth market analysis to identify opportunities and challenges.
2. Develop comprehensive trading theses, encompassing both technical and fundamental aspects.
3. Collaborate with specialized agents to ensure a cohesive strategy.
4. Make informed, data-driven decisions on trade executions.

For each stock under consideration, please provide the following:

- A concise market thesis, outlining the overall market position and expected trends.
- Key technical and fundamental factors influencing the stock's performance.
- A detailed risk assessment, highlighting potential pitfalls and mitigation strategies.
- Trade parameters, including entry and exit points, position sizing, and risk management guidelines.
"""

class TradingDirector:
    """
    Trading Director Agent responsible for generating trading theses and coordinating strategy.
    """

    def __init__(
        self,
        stocks: List[str],
        output_dir: str = "outputs",
        cryptos: List[str] = None,
    ):
        logger.info("Initializing Trading Director")
        self.director_agent = Agent(
            agent_name="Trading-Director",
            system_prompt=DIRECTOR_PROMPT,
            model_name=settings.DIRECTOR_MODEL,
            output_type="str",
            max_loops=settings.MAX_LOOPS,
            verbose=settings.VERBOSE,
            context_length=settings.CONTEXT_LENGTH,
        )

    def generate_thesis(
        self,
        task: str = "Generate a thesis for the stock",
        stock: str = None,
        crypto: str = None,
    ) -> str:
        """
        Generate trading thesis for a given stock.
        """
        logger.info(f"Generating thesis for {stock}")

        self.tickr = TickrAgent(
            stocks=[stock],
            max_loops=1,
            workers=10,
            retry_attempts=1,
            context_length=settings.CONTEXT_LENGTH,
        )

        try:
            market_data = self.tickr.run(
                f"{task} Analyze current market conditions and key metrics for {stock}"
            )

            prompt = f"""
            Task: {task}
            \n
            Stock: {stock}
            Market Data: {market_data}
            """

            thesis = self.director_agent.run(prompt)
            return thesis, market_data

        except Exception as e:
            logger.error(
                f"Error generating thesis for {stock}: {str(e)}"
            )
            raise

    def make_decision(self, task: str, thesis: str, *args, **kwargs):
        return self.director_agent.run(
            f"According to the thesis, {thesis}, should we execute this order: {task}"
        )
