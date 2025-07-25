from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from graph.state import ResearchState
import re
import os

# Get the API key from the environment
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM for the planner using the correct free-tier model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest", # <-- THE CORRECT MODEL NAME
    google_api_key=google_api_key,
    temperature=0, 
    convert_system_message_to_human=True
)

# Define the planner prompt
planner_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert research planner. Your goal is to create a detailed, step-by-step research plan 
    for a given topic.

    The plan should consist of a list of simple, targeted sub-questions that, when answered, will 
    collectively provide a comprehensive understanding of the main topic.

    Generate a Python list of strings, where each string is a sub-question.
    Your output MUST be a valid Python list of strings. For example:
    ["What is the history of AI?", "How does deep learning work?", "What are the ethical concerns of AI?"]

    Research Topic: {topic}
    """
)

# Create the planner chain
planner_chain = planner_prompt | llm

def plan_research(state: ResearchState) -> ResearchState:
    print("---PLANNING RESEARCH---")
    topic = state['topic']
    response_content = planner_chain.invoke({"topic": topic}).content
    
    match = re.search(r'\[\s*".*?"\s*(,\s*".*?"\s*)*\]', response_content, re.DOTALL)
    
    try:
        if match:
            plan = eval(match.group(0))
        else:
            raise ValueError("No valid list found in the planner's response.")
        
        if not isinstance(plan, list):
             raise ValueError("Parsed output is not a list.")

    except Exception as e:
        print(f"Error parsing planner output: {e}. Falling back to line splitting.")
        plan = [line.strip().replace("\"", "").replace(",", "") for line in response_content.split('\n') if line.strip() and "?" in line]

    return {**state, "plan": plan}