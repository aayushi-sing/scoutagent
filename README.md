# ScoutAgent — Autonomous Startup Scout

An agentic AI pipeline that researches a startup space end-to-end: it plans a research strategy, searches the web for emerging companies, digs into their traction and red flags, scores them like an analyst would, and writes a scannable investment-style report — all without a human in the loop between steps.

Built with [CrewAI](https://www.crewai.com/) for agent orchestration, [Tavily](https://tavily.com/) for live web search, and [Streamlit](https://streamlit.io/) for the interface.

## How it works

Six agents run in a strict sequential pipeline, each one handing its output to the next as context:

1. **Research Planner** — turns a raw topic into 3–5 targeted search queries, key categories to look for, and scoring criteria, while pulling in relevant notes from past runs on similar topics.
2. **Startup Scout** — uses Tavily search to find 5–8 startups matching the plan, each with a description, founding year, a traction signal, and a source URL.
3. **Deep Researcher** — goes deeper on each startup: funding rounds, social proof, competitors, team background, and red flags.
4. **Investment Critic** — scores every startup 1–10 with reasoning, flags hype-driven picks, and calls out the top 2–3 as "high signal."
5. **Report Writer** — compiles everything into a markdown report under 800 words: Executive Summary, Market Pulse, a scorecard table, Top Picks, and Recommended Next Actions.
6. **Memory Manager** — distills the run into a structured JSON summary (topic, startup names, top picks, scores, key trends, run quality) for long-term recall.

Each run is also logged to a local SQLite history and checked against past runs on similar topics, so repeat research on a topic can build on what the agent already found before.

## Stack

- **Orchestration:** CrewAI (sequential process)
- **LLM:** OpenRouter (currently configured to a free-tier model — see note below)
- **Search:** Tavily API
- **Frontend:** Streamlit
- **Persistence:** local JSON for agent memory, SQLite for run history

## Running it locally

```bash
git clone https://github.com/aayushi-sing/scoutagent.git
cd scoutagent
python -m venv venv
venv\Scripts\activate        # or source venv/bin/activate on Mac/Linux
pip install -r requirements.txt
```

Create a `.env` file in the project root with:
```
OPENROUTER_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
```

Then run:
```bash
streamlit run app.py
```

## Known limitations

Being upfront about these — they're the honest tradeoffs of building this on free-tier infra rather than gaps I didn't notice:

- **Free-tier LLM reliability.** The pipeline is currently wired to a free OpenRouter model to keep the project runnable at zero cost. Free models can vary in throughput and in how consistently they support tool/function calling, which occasionally affects the Scout and Researcher agents (the two that call the search tool). Swapping in a paid model is a one-line change in `llm_config.py`.
- **Storage is local, not cloud-persistent.** Run history and agent memory are stored on disk (SQLite + JSON), which works well locally but won't survive a redeploy or a sleep/wake cycle on free hosting tiers like Streamlit Community Cloud. A natural next step would be swapping in a hosted database (e.g. Supabase or a managed Postgres) for true cross-session persistence.
- **Sequential, not parallel.** All six agents run one after another by design, for predictable, debuggable context-passing. This means a single research run takes longer than a parallel-agent design would, in exchange for simpler reasoning about what each agent saw.

## Possible extensions

- Hosted database for durable memory across deploys
- Parallelizing the Scout and Researcher steps where they don't depend on each other's live output
- A model-agnostic config to switch between paid and free LLMs without code changes
