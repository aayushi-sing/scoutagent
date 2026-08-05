import streamlit as st
import time
from pipeline import run_pipeline
from memory.mem0_client import get_all_memories
from db.history import get_history, get_report_by_id, init_db

st.set_page_config(page_title="Startup Scout", page_icon="🔭", layout="wide")
init_db()

# Sidebar — Memory + History
with st.sidebar:
    st.markdown("### Agent Memory")
    

    st.markdown("### 📜 History")
    for row in get_history(10):
        if st.button(f"🕐 {row['timestamp']} · {row['topic'][:20]}", key=f"h{row['id']}"):
            st.session_state["loaded_report"] = get_report_by_id(row["id"])
            st.session_state["loaded_topic"]  = row["topic"]

    st.markdown("### 🧪 Eval Results")
    import glob, json
    eval_files = sorted(glob.glob("eval/results/*.json"))
    if eval_files:
        with open(eval_files[-1]) as f:
            eval_data = json.load(f)
        st.metric("Passed", f"{eval_data['passed']}/{eval_data['total']}")
        for r in eval_data["runs"]:
            icon = "✅" if r["pass"] else "❌"
            st.write(f"{icon} {r['id']}")
    else:
        st.caption("No eval results found yet.")

# Main
st.title("🔭 Autonomous Startup Scout Agent")
st.caption("CrewAI · Tavily · Mem0 · Persistent Memory")

col1, col2 = st.columns([1, 1])

with col1:
    topic = st.text_input("Research Topic", "AI productivity tools for developers")
    run_btn = st.button("▶ Run Agent", type="primary")

with col2:
    st.markdown("**⚙️ Live Execution Log**")
    log_box = st.empty()

# Run
if run_btn and topic.strip():
    st.session_state.pop("loaded_report", None)
    steps = []

    def on_step(step, msg):
        steps.append(f"**[{step}]** {msg}")
        log_box.markdown("\n\n".join(steps))
        st.session_state["steps"] = steps


    with st.spinner("Running pipeline..."):
        result = run_pipeline(topic, callback=on_step)

    st.session_state["result"] = result
    st.session_state["steps"] = steps
    st.rerun()

elif "steps" not in st.session_state:
    log_box.info("Log will appear here when you run the agent.")

# Results
if "result" in st.session_state:
    res = st.session_state["result"]
    st.divider()

    c1, c2, c3 = st.columns(3)
    c1.metric("Startups Found", len(res["startups"]))
    c2.metric("Top Picks",      len(res["top_picks"]))
    c3.metric("Run Quality",    f"{res['quality']}/10")

    if res["scores"]:
        st.markdown("#### 🏆 Scores")
        def _num(v):
            try:
                return float(v)
            except (ValueError, TypeError):
                return 0.0
        for name, score in sorted(res["scores"].items(), key=lambda x: _num(x[1]), reverse=True):
            score_val = _num(score)
            color = "🟢" if score_val >= 7 else ("🟡" if score_val >= 4 else "🔴")
            st.write(f"{color} **{name}** — {score}/10")

    st.divider()
    st.markdown(res["report"].replace("\$", "  \\$"))
    st.download_button("⬇️ Download Report", res["report"],
                       file_name="scout_report.md", mime="text/markdown")

elif "loaded_report" in st.session_state:
    st.divider()
    st.info(f"Past run: **{st.session_state.get('loaded_topic','')}**")
    st.markdown(st.session_state["loaded_report"].replace("\$", "  \\$"))