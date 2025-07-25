# --- CRITICAL: LOAD ENV VARS FIRST ---
# This must be the very first thing to run so that all other modules
# can access the environment variables from the .env file.
from dotenv import load_dotenv
load_dotenv()

# Now we can import the rest of our modules
import streamlit as st
import os
from graph.builder import build_graph

# Check for necessary API keys (Changed to GOOGLE_API_KEY)
if not os.getenv("GOOGLE_API_KEY") or not os.getenv("TAVILY_API_KEY"):
    st.error("🚨 Please check your .env file. It must contain GOOGLE_API_KEY and TAVILY_API_KEY.")
    st.stop()

# Build the graph
try:
    graph = build_graph()
except Exception as e:
    st.error(f"Failed to build the graph: {e}")
    st.exception(e) # Print full traceback for debugging
    st.stop()


# --- Streamlit UI ---
st.set_page_config(page_title="Deep Research AI Agent (Gemini Edition)", layout="wide")

st.title("🧠 Deep Research AI Agent (Gemini Edition)")
st.markdown("""
This AI agent performs deep research on a given topic by planning, searching, and synthesizing information 
into a comprehensive report using Google's Gemini Pro.
""")

st.sidebar.header("How it works")
st.sidebar.info("""
1.  **Planner Agent:** Breaks down the topic into a research plan.
2.  **Researcher Agent:** Searches the web (Tavily) and scrapes content for each point in the plan.
3.  **Writer Agent:** Compiles the gathered information into a final report.
The entire process is orchestrated using LangGraph and powered by Google Gemini.
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
                
                # Use a status container to show progress
                status = st.status("Kicking off the research process...", expanded=True)
                final_state = None
                
                # Stream the graph execution
                for event in graph.stream(initial_state):
                    # The event key is the name of the node that just finished
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
                st.error(f"An error occurred during the research process:")
                st.exception(e) # This will print the full traceback for easier debugging