from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from graph.state import ResearchState
import os

# Get the API key from the environment
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM for the writer using the correct free-tier model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest", # <-- THE CORRECT MODEL NAME
    google_api_key=google_api_key,
    temperature=0.1, 
    convert_system_message_to_human=True
)

# Define the writer prompt
writer_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert report writer. Your task is to synthesize a collection of research findings 
    into a single, high-quality, and comprehensive report.

    The report should be well-structured with clear Markdown formatting. Use headings, subheadings,
    bullet points, and bold text to improve readability. It should have a clear introduction, 
    a body that addresses each research point, and a concluding summary. It must be written
    in a formal, professional tone.

    Here are the research findings, provided as a list of question-answer pairs:
    ---
    {research_summary}
    ---

    Based on these findings, please generate the final report on the original topic: "{topic}".
    Ensure the report flows logically and reads as a single, cohesive document.
    """
)

# Create the writer chain
writer_chain = writer_prompt | llm

def format_research_summary(researched_answers: list[dict]) -> str:
    summary = ""
    for item in researched_answers:
        summary += f"### {item['question']}\n{item['answer']}\n\n"
    return summary.strip()

def write_report(state: ResearchState) -> ResearchState:
    print("---WRITING FINAL REPORT---")
    topic = state['topic']
    research_summary = format_research_summary(state['researched_answers'])
    
    report = writer_chain.invoke({
        "topic": topic,
        "research_summary": research_summary
    }).content
    
    return {**state, "final_report": report}