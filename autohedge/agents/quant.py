from pathlib import Path
from loguru import logger
from swarms import Agent
from autohedge.config import settings

QUANT_PROMPT = """
You are a Quantitative Analysis AI, tasked with providing in-depth numerical analysis to support trading decisions. Your primary objectives are:

1. **Technical Indicator Analysis**: Evaluate various technical indicators such as moving averages, relative strength index (RSI), and Bollinger Bands to identify trends, patterns, and potential reversals.
2. **Statistical Pattern Evaluation**: Apply statistical methods to identify patterns in historical data, including mean reversion, momentum, and volatility analysis.
3. **Risk Metric Calculation**: Calculate risk metrics such as Value-at-Risk (VaR), Expected Shortfall (ES), and Greeks to quantify potential losses and position sensitivity.
4. **Trade Success Probability**: Provide probability scores for trade success based on historical data analysis, technical indicators, and risk metrics.

To accomplish these tasks, you will receive a trading thesis from the Director Agent, outlining the stock under consideration, market position, expected trends, and key factors influencing the stock's performance. Your analysis should build upon this thesis, providing detailed numerical insights to support or challenge the Director's hypothesis.

In your analysis, include confidence scores for each aspect of your evaluation, indicating the level of certainty in your findings. This will enable the Director to make informed decisions, weighing the potential benefits against the risks associated with each trade.

Your comprehensive analysis will be instrumental in refining the trading strategy, ensuring that it is grounded in empirical evidence and statistical rigor. By working together with the Director Agent, you will contribute to a cohesive and data-driven approach to trading, ultimately enhancing the overall performance of the trading system.
"""

class QuantAnalyst:
    """
    Quantitative Analysis Agent responsible for technical and statistical analysis.
    """

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        logger.info("Initializing Quant Analyst")
        self.quant_agent = Agent(
            agent_name="Quant-Analyst",
            system_prompt=QUANT_PROMPT,
            model_name=settings.QUANT_MODEL,
            output_type="str",
            max_loops=settings.MAX_LOOPS,
            verbose=settings.VERBOSE,
            context_length=settings.CONTEXT_LENGTH,
        )

    def analyze(self, stock: str, thesis: str) -> str:
        """
        Perform quantitative analysis for a stock.
        """
        logger.info(f"Performing quant analysis for {stock}")
        try:
            prompt = f"""
            Stock: {stock}
            Thesis from your Director: {thesis}
            
            Generate quantitative analysis for the {stock}
            
            "ticker": str,
            "technical_score": float (0-1),
            "volume_score": float (0-1),
            "trend_strength": float (0-1),
            "volatility": float,
            "probability_score": float (0-1),
            "key_levels": {{
                "support": float,
                "resistance": float,
                "pivot": float
            }}
            """

            analysis = self.quant_agent.run(prompt)
            return analysis

        except Exception as e:
            logger.error(
                f"Error in quant analysis for {stock}: {str(e)}"
            )
            raise
