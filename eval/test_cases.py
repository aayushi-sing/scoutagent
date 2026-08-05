"""Test queries for ScoutAgent eval harness.
Each case: a topic + the minimum bar a healthy run should clear.
"""

TEST_CASES = [
    {
     
        "id": "tc01_narrow_niche",
        "topic": "AI note-taking tools for students",
        "min_startups": 4,
    },
    {
        "id": "tc02_broad_category",
       "topic": "climate tech startups",
        "min_startups": 5,
    },
    {
        "id": "tc03_saturated_space",
        "topic": "AI coding assistants",
        "min_startups": 5,
    },
      {
        "id": "tc04_recent_trend",
        "topic": "AI agents for customer support",
        "min_startups": 4,
    },
    {
       "id": "tc05_ambiguous_query",
       "topic": "productivity",  # deliberately vague — stress test for Planner
       "min_startups": 3,
    },
    {
        "id": "tc06_repeat_topic",
        # run the same topic as tc01 a second time to test memory recall path
       "topic": "AI note-taking tools for students",
        "min_startups": 4,
    },  
]

REQUIRED_REPORT_SECTIONS = [
    "Executive Summary",
    "Market Pulse",
    "Startup Scorecard",
    "Top Picks",
    "Recommended Next Actions",
]