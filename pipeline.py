import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
from dotenv import load_dotenv
from crewai import Crew, Process
from agents.crew_agents import *
from agents.crew_tasks import *
from memory.mem0_client import get_past_research, save_research
from db.history import init_db, log_run
import litellm
litellm.retry_policy = {
    "RateLimitError": {"retry_after": 15}
}
load_dotenv()

def run_pipeline(topic: str, callback=None) -> dict:
    init_db()

    def log(step, msg):
        print(f"[{step}] {msg}")
        if callback:
            callback(step, msg)

    log("Memory", f"Checking past research on '{topic}'...")
    past_context = get_past_research(topic)

    log("Setup", "Initialising agents...")
    planner    = make_planner_agent()
    scout      = make_scout_agent()
    researcher = make_researcher_agent()
    critic     = make_critic_agent()
    reporter   = make_reporter_agent()
    mem_agent  = make_memory_agent()

    t_plan     = make_plan_task(planner, topic, past_context)
    t_scout    = make_scout_task(scout, t_plan)
    t_research = make_research_task(researcher, t_scout)
    t_critic   = make_critic_task(critic, t_research)
    t_report   = make_report_task(reporter, t_critic, topic)
    t_memory   = make_memory_task(mem_agent, t_report, topic)

    log("Planner",    "Breaking down research plan...")
    log("Scout",      "Searching the web for startups...")
    log("Researcher", "Digging into traction and signals...")
    log("Critic",     "Scoring — separating signal from hype...")
    log("Reporter",   "Writing final report...")
    log("Memory",     "Saving to long-term memory...")

    crew = Crew(
        agents=[planner, scout, researcher, critic, reporter, mem_agent],
        tasks=[t_plan, t_scout, t_research, t_critic, t_report, t_memory],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    raw = result.raw if hasattr(result, "raw") else str(result)

    # Parse memory JSON from last task
    memory_data = {}
    try:
        clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        memory_data = json.loads(clean)
    except Exception:
        memory_data = {"startup_names":[],"top_picks":[],"scores":{},"key_trends":[],"run_quality":0}

    report_text = t_report.output.raw if hasattr(t_report, "output") and t_report.output else raw

    startups = memory_data.get("startup_names", [])
    scores   = memory_data.get("scores", {})

    save_research(topic, [{"name": n} for n in startups], report_text[:300])
    log_run(topic, startups, scores, report_text)
    log("Done", "✅ Pipeline complete!")

    return {
        "report":    report_text,
        "startups":  startups,
        "scores":    scores,
        "top_picks": memory_data.get("top_picks", []),
        "trends":    memory_data.get("key_trends", []),
        "quality":   memory_data.get("run_quality", 0),
    }

if __name__ == "__main__":
    r = run_pipeline("AI productivity tools for developers")
    print(r["report"])