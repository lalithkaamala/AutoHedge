import concurrent.futures
from typing import List
from pathlib import Path
from loguru import logger
from swarms import Conversation

from autohedge.config import settings
from autohedge.utils import setup_logging, AutoHedgeOutputMain
from autohedge.agents import (
    TradingDirector,
    QuantAnalyst,
    RiskManager,
    ExecutionAgent,
    SentimentAgent
)

setup_logging()

class AutoHedge:
    """
    Main trading system that coordinates all agents and manages the trading cycle.
    """

    def __init__(
        self,
        stocks: List[str],
        name: str = "autohedge",
        description: str = "fully autonomous hedgefund",
        output_dir: str = "outputs",
        output_file_path: str = None,
        strategy: str = None,
        output_type: str = "list",
    ):
        self.name = name
        self.description = description
        self.stocks = stocks
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.strategy = strategy
        self.output_type = output_type
        self.output_file_path = output_file_path
        
        logger.info("Initializing Automated Trading System")
        self.director = TradingDirector(stocks, str(output_dir))
        self.quant = QuantAnalyst(str(output_dir))
        self.risk = RiskManager()
        self.execution = ExecutionAgent()
        self.sentiment = SentimentAgent()
        
        self.logs = AutoHedgeOutputMain(
            name=self.name,
            description=self.description,
            stocks=stocks,
            task="",
            logs=[],
        )
        self.conversation = Conversation(time_enabled=True)

    def fetch_stock_news(self, stock: str) -> str:
        """
        Placeholder for fetching stock news.
        In a real implementation, this would connect to a news API or use a web search tool.
        """
        return f"Market sentiment analysis for {stock}: Reviewing recent financial news, earnings reports, and social media trends."

    def run(self, task: str, *args, **kwargs):
        """
        Execute one complete trading cycle for all stocks.
        """
        logger.info("Starting trading cycle")
        self.conversation.add(role="user", content=f"Task: {task}")

        try:
            for stock in self.stocks:
                logger.info(f"Processing {stock}")
                
                # Parallel Execution of Thesis Generation and Sentiment Analysis
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    thesis_future = executor.submit(self.director.generate_thesis, task=task, stock=stock)
                    sentiment_future = executor.submit(self.sentiment.analyze, self.fetch_stock_news(stock))
                    
                    thesis, market_data = thesis_future.result()
                    sentiment_analysis = sentiment_future.result()

                self.conversation.add(
                    role="Trading-Director",
                    content=f"Stock: {stock}\nMarket Data: {market_data}\nThesis: {thesis}"
                )
                
                self.conversation.add(
                    role="Sentiment-Agent",
                    content=sentiment_analysis
                )

                # Perform Quant Analysis
                analysis = self.quant.analyze(stock + market_data, thesis)
                self.conversation.add(role="Quant-Analyst", content=analysis)

                # Assess Risk
                risk_assessment = self.risk.assess_risk(stock + market_data, thesis, analysis)
                self.conversation.add(role="Risk-Manager", content=risk_assessment)

                # Generate Order
                order = self.execution.generate_order(stock, thesis, risk_assessment)
                self.conversation.add(role="Execution-Agent", content=str(order))

                # Final Decision
                decision = self.director.make_decision(
                    str(order) + market_data + str(risk_assessment) + sentiment_analysis, 
                    thesis
                )
                self.conversation.add(role="Trading-Director", content=decision)

            if self.output_type == "list":
                return self.conversation.return_messages_as_list()
            elif self.output_type == "dict":
                return self.conversation.return_messages_as_dictionary()
            elif self.output_type == "str":
                return self.conversation.return_history_as_string()

        except Exception as e:
            logger.error(f"Error in trading cycle: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    api = AutoHedge(stocks=["AAPL", "TSLA"])
    # api.run("Run a trading cycle")
