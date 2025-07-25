# graph/builder.py (Corrected conditional edge)

from langgraph.graph import StateGraph, END
from .state import ResearchState
from agents.planner import plan_research
from agents.researcher import research_step, should_continue_research
from agents.writer import write_report

def build_graph():
    """
    Builds the LangGraph for the research process.
    """
    workflow = StateGraph(ResearchState)

    # Add the nodes to the graph
    workflow.add_node("plan_research", plan_research)
    workflow.add_node("research_step", research_step)
    workflow.add_node("write_report", write_report)

    # Set the entry point
    workflow.set_entry_point("plan_research")

    # Add edges to define the flow
    workflow.add_edge("plan_research", "research_step")
    
    # Add the conditional edge for the research loop
    workflow.add_conditional_edges(
        "research_step",
        should_continue_research,
        {
            "research": "research_step", # If it says 'research', loop back
            "write": "write_report"      # If it says 'write', move to writer
        }
    )

    workflow.add_edge("write_report", END)

    # Compile the graph
    app = workflow.compile()
    
    return app