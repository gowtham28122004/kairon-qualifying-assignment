from typing import List, TypedDict

class ResearchState(TypedDict):
    """
    Represents the state of our research process.

    Attributes:
        topic: The initial research question or topic.
        plan: A list of sub-questions to research.
        researched_answers: A list of dictionaries, each containing a sub-question and its answer.
        final_report: The final, consolidated report.
    """
    topic: str
    plan: List[str]
    researched_answers: List[dict]
    final_report: str