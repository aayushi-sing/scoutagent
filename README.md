Autonomous Startup Scout Agent

An autonomous multi-agent AI system that researches startups, analyzes market signals, scores opportunities, and generates intelligence reports using collaborative AI agents with persistent memory.

Features
    -Multi-agent orchestration using CrewAI
    
    -Web research powered by Tavily
    
    -Persistent memory with Mem0
    
    -Live execution logs in Streamlit
    
    -Startup scoring and opportunity analysis

    -Research history tracking
    
    -Long-term contextual memory across runs

## What it does

Give it a topic like *"AI productivity tools for developers"* and it:

1. Plans a research strategy
2. Searches the web for relevant startups
3. Digs into traction, funding, and red flags
4. Scores each startup using a 4-dimension framework
5. Writes an investment-grade report
6. Remembers what it found — second run builds on the first

Agent Workflow

User Query
   ↓
Planner Agent
   ↓
Scout Agent
   ↓
Research Agent
   ↓
Critic Agent
   ↓
Report Agent
   ↓
Memory Manager

## 6 Specialized Agents

| Agent | Role |
|---|---|
| **Planner** | Breaks topic into search queries and scoring criteria |
| **Scout** | Finds 5-8 startups via live web search |
| **Researcher** | Extracts funding, traction, competitors, red flags |
| **Critic** | Scores each startup across 4 dimensions |
| **Reporter** | Writes a scannable markdown report |
| **Memory Manager** | Decides what's worth remembering for future runs |

---

## Scoring Framework

The Critic agent evaluates every startup on:

- **Founder-Market Fit** — does the team have an unfair advantage?
- **Timing** — why now, not 2 years ago?
- **Distribution** — how do they grow without paid ads?
- **Defensibility** — what stops a big player copying this in 6 months?
