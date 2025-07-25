from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from graph.state import ResearchState
from tools.scraper import scraper_tool
import os

# Get the API key from the environment
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM for the researcher using the correct free-tier model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest", # <-- THE CORRECT MODEL NAME
    google_api_key=google_api_key,
    temperature=0, 
    convert_system_message_to_human=True
)

# Define the tools for the researcher
tools = [TavilySearchResults(max_results=3), scraper_tool]

# The required prompt template for the ReAct agent
template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {question}
Thought:{agent_scratchpad}
"""

researcher_prompt = ChatPromptTemplate.from_template(template)

# Create the researcher agent
researcher_agent = create_react_agent(llm, tools, researcher_prompt)

# Create the agent executor
researcher_agent_executor = AgentExecutor(agent=researcher_agent, tools=tools, verbose=True, handle_parsing_errors=True)

def research_step(state: ResearchState) -> ResearchState:
    print("---CONDUCTING RESEARCH STEP---")
    current_question_index = len(state.get('researched_answers', []))
    if current_question_index >= len(state['plan']):
        return state
        
    question = state['plan'][current_question_index]
    print(f"Researching question: {question}")
    
    answer_payload = researcher_agent_executor.invoke({"question": question, "input": question})
    answer = answer_payload['output']
    
    new_answer = {"question": question, "answer": answer}
    researched_answers = state.get('researched_answers', []) + [new_answer]
    
    return {**state, "researched_answers": researched_answers}

def should_continue_research(state: ResearchState) -> str:
    print("---CHECKING IF RESEARCH IS COMPLETE---")
    if len(state['researched_answers']) >= len(state['plan']):
        print("Research complete. Proceeding to writing.")
        return "write"
    else:
        print("More questions to research. Continuing research loop.")
        return "research"