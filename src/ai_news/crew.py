from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv()

@CrewBase
class AiNews:
    """AiNews crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # ✅ Option 1: Use OpenAI (easiest setup - just set OPENAI_API_KEY in .env)
    # Leave this commented out to use CrewAI's default OpenAI configuration
    # llm = LLM(model="gpt-4o-mini")
    
    # ✅ Option 2: Use Gemini (requires: uv add google-generativeai)
    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7
    )

    @agent
    def retrieve_news(self) -> Agent:
        return Agent(
            config=self.agents_config['retrieve_news'], 
            tools=[SerperDevTool()],
            verbose=True,
            llm=self.llm
        )

    @agent
    def website_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['website_scraper'],
            tools=[ScrapeWebsiteTool()],
            verbose=True,
            llm=self.llm
        )

    @agent
    def ai_news_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['ai_news_writer'],
            tools=[],
            verbose=True,
            llm=self.llm
        )

    @agent
    def file_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['file_writer'],
            tools=[FileWriterTool()],
            verbose=True,
            llm=self.llm
        )

    @task
    def retrieve_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieve_news_task']
        )

    @task
    def website_scraper_task(self) -> Task:
        return Task(
            config=self.tasks_config['website_scraper_task']
        )

    @task
    def ai_news_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['ai_news_writer_task']
        )

    @task
    def file_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['file_writer_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )