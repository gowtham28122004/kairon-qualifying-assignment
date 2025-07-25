# AI-Powered Deep Research Agentic System
### Kairon Qualifying Assignment Submission

## 1. Introduction

This project is a sophisticated, multi-agent AI system designed to perform deep research on any given topic. The system takes a high-level topic, autonomously creates a research plan, gathers information from the internet, and synthesizes the findings into a comprehensive, well-structured report.

This solution was built for the Kairon qualifying assignment, demonstrating proficiency in modern AI engineering frameworks like **LangChain & LangGraph**, agentic design principles, and the integration of external tools for robust information gathering.

The core of this project is its agentic workflow, where specialized AI agents collaborate to achieve a complex goal, mirroring a real-world human research team.

## 2. System Architecture & Workflow

The system is architected as a **cyclical, stateful graph** using the LangGraph framework. This is more powerful than a simple chain as it allows for loops, conditional logic, and a persistent state that is passed between agents.

The `ResearchState` object acts as the shared memory for the agents, containing the topic, the evolving research plan, the collected answers, and the final report.

**The agentic workflow consists of the following nodes:**

1.  **Planner Agent**: The "Team Lead." Upon receiving the user's topic, this agent's sole responsibility is to break it down into a logical, step-by-step list of sub-questions. This forms the research plan, ensuring comprehensive and structured data collection.

2.  **Researcher Agent**: The "Data Collector." This agent works in a loop, taking one sub-question at a time from the plan. It has access to two critical tools:
    -   **Tavily Search Tool**: To perform targeted web searches for the most relevant articles, papers, and sources.
    -   **Web Scraper Tool**: To read the full text content of the most promising URLs returned by the search.
    It then synthesizes the information from these sources to generate a factual answer for that *specific* sub-question.

3.  **Conditional Edge (Decision Point)**: After each research step, the graph's logic checks if the number of researched answers matches the number of questions in the plan.
    -   **If NO**, the graph loops back to the Researcher Agent, feeding it the next question.
    -   **If YES**, the research phase is complete, and the graph proceeds to the final writing phase.

4.  **Writer Agent**: The "Report Drafter." This agent receives the complete, structured set of all questions and their corresponding researched answers. Its job is not to find new information, but to weave the existing findings into a single, coherent, and well-formatted final report, complete with an introduction, body, and conclusion.

### Workflow Diagram

```mermaid
graph TD
    A[Start: User Topic] --> B(Planner Agent);
    B --> C{Research Plan Created};
    C --> D(Researcher Agent);
    D -- Gathers data for one sub-question --> E{Is Plan Complete?};
    E -- No, more questions exist --> D;
    E -- Yes, all questions answered --> F(Writer Agent);
    F -- Synthesizes all findings --> G[End: Final Report];
```

## 3. Core Technologies & Components

- **Primary Frameworks**: **LangChain** (for agent components and tools), **LangGraph** (for orchestrating the multi-agent workflow).
- **Language Model (LLM)**: **Google Gemini (`gemini-1.5-flash-latest`)** accessed via the `langchain-google-genai` library, providing a powerful and free-tier-friendly reasoning engine.
- **User Interface**: **Streamlit**, for creating a simple, interactive web-based front-end.
- **Online Search Tool**: **Tavily AI**, integrated via `langchain-community` for fast, accurate, and AI-optimized search results.
- **Web Scraping**: **BeautifulSoup4** & **Requests**, built into a custom LangChain tool for on-demand content extraction.
- **Environment Management**: **`python-dotenv`** for securely managing API keys without hard-coding them.

## 4. Project Structure

The project is organized into modular components for clarity, maintainability, and scalability.

/kairon-qualifying-assignment/
|
|-- .gitignore # Ensures secret keys and virtual env are not tracked by Git.
|-- README.md # This detailed explanation document.
|-- requirements.txt # A list of all project dependencies for easy installation.
|-- .env.example # A safe template for the required environment variables.
|-- app.py # The main Streamlit application entry point.
|
|-- agents/ # Contains the Python modules for each specialized AI agent.
| |-- planner.py
| |-- researcher.py
| |-- writer.py
|
|-- graph/ # Defines and builds the LangGraph agentic workflow.
| |-- builder.py # Assembles the nodes and edges into a compiled graph.
| |-- state.py # Defines the shared state object for the graph.
|
|-- tools/ # Contains custom-built tools for the agents to use.
| |-- scraper.py


## 5. Setup and Installation Guide

Follow these steps to set up and run the project on your local machine.

**1. Clone the repository:**
```bash
git clone https://github.com/gowtham28122004/kairon-qualifying-assignment.git
cd kairon-qualifying-assignment
```
2. Create and activate a Python virtual environment:
Generated bash
# Create the environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Use code with caution.
Bash
3. Install all required dependencies:
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash

4. Configure your API Keys:
Find the .env.example file in the project folder.
Rename it to simply .env.
Open the new .env file and paste your personal API keys for GOOGLE_API_KEY and TAVILY_API_KEY. The LangSmith key is optional but highly recommended for debugging.

6. How to Run the Application
Once the setup is complete and your virtual environment is active, run the following command in your terminal:
Generated bash
streamlit run app.py
Use code with caution.
Bash
Your default web browser will automatically open a new tab with the application interface, ready for you to start your research.

8. Unique Perspectives & Future Improvements
To address the assignment's call for imagination, here are several ways this system could be enhanced:
Parallel Research: The current research loop is sequential. LangGraph supports parallel execution, so multiple Researcher Agents could tackle different sub-questions simultaneously, drastically reducing total research time.
Human-in-the-Loop Feedback: Before the Writer Agent drafts the final report, the system could present the user with the research findings and ask for validation. The user could flag a specific answer as "incomplete" or "incorrect," triggering a targeted re-research step for that point.
Dynamic Report Formatting: The Writer Agent could be given tools to format the output in different ways, such as generating a PowerPoint presentation, a PDF document, or even a blog post, based on user preference.
Source Citation and Reliability Scoring: The Researcher Agent could be enhanced to not only extract information but also to provide citations for each claim. A separate "Fact-Checker" agent could be added to the graph to score the reliability of sources before they are used.
Cost & Token Tracking: In a real-world scenario, every LLM call costs money. The ResearchState could be updated to track the token usage of each agent, providing a final cost breakdown for the entire research task.
