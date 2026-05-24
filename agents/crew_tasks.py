from crewai import Task

def make_plan_task(planner, topic, past_context):
    return Task(
        description=(
            f"Create a research plan for: '{topic}'.\n\n{past_context}\n\n"
            "Output:\n1. 3-5 search queries\n2. Key categories\n3. Scoring criteria\n4. Notes from past research"
        ),
        expected_output="Structured markdown plan with search queries, categories, scoring criteria.",
        agent=planner
    )

def make_scout_task(scout, plan_task):
    return Task(
        description=(
            "Using the plan, find 5-8 startups. For each:\n"
            "- Name\n- What they do (1-2 sentences)\n- Founded year\n- Traction signal\n- Source URL\n\n"
            "Focus on companies launched or gaining traction in last 12-18 months."
        ),
        expected_output="Numbered list of 5-8 startups with name, description, traction, source URL.",
        agent=scout, context=[plan_task]
    )

def make_research_task(researcher, scout_task):
    return Task(
        description=(
            "For each startup from the Scout, dig deeper:\n"
            "- Funding rounds\n- Social proof / reviews\n- Competitors\n- Team\n- Red flags"
        ),
        expected_output="Enriched profile per startup: funding, team, social proof, competitors, red flags.",
        agent=researcher, context=[scout_task]
    )

def make_critic_task(critic, research_task):
    return Task(
        description=(
            "Score every startup 1-10. Give 2-3 sentence justification per score.\n"
            "Flag hype-driven ones. Identify top 2-3 as 'high signal' picks."
        ),
        expected_output="Scored list with reasoning and a Top Picks section. Markdown format.",
        agent=critic, context=[research_task]
    )

def make_report_task(reporter, critic_task, topic):
    return Task(
        description=(
            f"Write the final report for: '{topic}'.\n\n"
            "## Executive Summary\n## Market Pulse\n## Startup Scorecard (table)\n"
            "## Top Picks\n## Recommended Next Actions\n\nUnder 800 words. Scannable."
        ),
        expected_output="Complete markdown report with all 5 sections.",
        agent=reporter, context=[critic_task]
    )

def make_memory_task(memory_agent, report_task, topic):
    return Task(
        description=(
            f"Summarize this run on '{topic}' as JSON with keys:\n"
            "- topic\n- startup_names (list)\n- top_picks (list)\n- scores (dict name->score)\n"
            "- key_trends (list of 3)\n- run_quality (1-10)\n\n"
            "Return ONLY valid JSON. No markdown fences."
        ),
        expected_output="Valid JSON object with all 6 keys.",
        agent=memory_agent, context=[report_task]
    )