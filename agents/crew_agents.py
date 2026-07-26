import os
from crewai import Agent
from llm_config import llm
from tools.search import TavilySearchTool


# Shared Search Tool
search_tool = TavilySearchTool()

def make_planner_agent():
    return Agent(
        role="Research Planner",
        goal="Create a brief research plan for a startup topic.",
        backstory="Venture analyst who scopes research tightly and thinks about signal quality.",
        verbose=False,
        allow_delegation=False,
        tools=[],
        llm=llm
    )

def make_scout_agent():
    return Agent(
        role="Startup Scout",
        goal="Find new startups matching the research plan using web search.",
        backstory="Startup hunter who spots breakout companies early on Product Hunt and HN.",
        verbose=False,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )


def make_researcher_agent():
    return Agent(
        role="Deep Researcher",
        goal="Extract traction, funding, competitors and red flags for each startup.",
        backstory="Due-diligence specialist who finds real momentum beyond surface claims.",
        verbose=False,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )


def make_critic_agent():
    return Agent(
        role="Investment Critic",
        goal="Score each startup 1-10 and identify the top 2 picks.",
        backstory="Skeptical analyst who separates real businesses from well-marketed science projects.",
        verbose=False,
        allow_delegation=False,
        tools=[],
        llm=llm
    )


def make_reporter_agent():
    return Agent(
        role="Report Writer",
        goal="Write a short, scannable startup intelligence report in markdown.",
        backstory="Writes concise reports for busy investors. Always under 400 words.",
        verbose=False,
        allow_delegation=False,
        tools=[],
        llm=llm
    )


def make_memory_agent():
    return Agent(
        role="Memory Manager",
        goal="Summarize the research run as a compact JSON memory entry.",
        backstory="The agent's long-term memory. Distills runs into retrievable summaries.",
        verbose=False,
        allow_delegation=False,
        tools=[],
        llm=llm
    )