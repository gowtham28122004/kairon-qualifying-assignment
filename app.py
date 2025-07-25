# app.py (Improved Version)

import streamlit as st
from dotenv import load_dotenv
import os

# --- Step 1: Load environment variables and check keys AT THE VERY TOP ---
# This is the most important change. We do this before any other project imports.
load_dotenv()

# Check for necessary API keys BEFORE trying to import any modules that use them.
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not openai_api_key or not tavily_api_key:
    st.title("🚨 API Key Error")
    st.error(
        "One or more required API keys (OPENAI_API_KEY, TAVILY_API_KEY) are missing. "
        "If you are running this on Streamlit Cloud, please add them to your Secrets. "
        "If running locally, ensure they are in your .env file."
    )
    st.stop()


# --- Step 2: Now that keys are verified, import the graph builder ---
# This import will now only run if the keys exist, preventing the Pydantic error.
try:
    from graph.builder import build_graph
    graph = build_graph()
except Exception as e:
    st.error(f"Failed to build the graph: {e}")
    st.stop()


# --- Step 3: The rest of the Streamlit UI ---
st.set_page_config(page_title="Deep Research AI Agent", layout="wide")

st.title("🧠 Deep Research AI Agent")
st.markdown("""
This AI agent performs deep research on a given topic by planning, searching, and synthesizing information 
into a comprehensive report.
""")

st.sidebar.header("How it works")
st.sidebar.info("""
1.  **Planner Agent:** Breaks down the topic into a research plan.
2.  **Researcher Agent:** Searches the web (Tavily) and scrapes content for each point in the plan.
3.  **Writer Agent:** Compiles the gathered information into a final report.
The entire process is orchestrated using LangGraph.
""")

topic = st.text_input(
    "Enter a research topic:",
    placeholder="e.g., The impact of AI on the future of software development"
)

if st.button("Start Research"):
    if not topic:
        st.warning("Please enter a topic to research.")
    else:
        with st.spinner("Research in progress... This may take a few minutes."):
            try:
                # Initial state for the graph
                initial_state = {
                    "topic": topic,
                    "plan": [],
                    "researched_answers": [],
                    "final_report": ""
                }
                
                status = st.status("Kicking off the research process...", expanded=True)
                final_state = None
                
                for event in graph.stream(initial_state, {"recursion_limit": 25}):
                    node_name = list(event.keys())[0]
                    node_output = event[node_name]
                    
                    if node_name == "plan_research":
                        status.write(f"**Research Plan Created:**\n" + "\n".join([f"- {q}" for q in node_output['plan']]))
                    elif node_name == "research_step":
                        latest_answer = node_output['researched_answers'][-1]
                        status.write(f"**Researching:** {latest_answer['question']}\n\n**Finding:** {latest_answer['answer'][:200]}...")
                    elif node_name == "write_report":
                        status.write("📝 **Compiling the final report...**")
                    
                    final_state = node_output

                status.update(label="Research Complete!", state="complete", expanded=False)
                
                st.subheader("Final Research Report")
                st.markdown(final_state['final_report'])

            except Exception as e:
                st.error(f"An error occurred during the research process: {e}")
