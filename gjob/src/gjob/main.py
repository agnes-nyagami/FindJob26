#!/usr/bin/env python
import sys
import warnings
from pathlib import Path
from datetime import datetime

from mcp_adapter import start_mcp_adapter, stop_mcp_adapter
from gjob.crew import Gjob

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def load_resume(resume_path: str) -> str:
    """
    Load resume text from a file.
    Assumes text or PDF parsing is handled here or inside the parser tool.
    """
    path = Path(resume_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_path}")

    return path.read_text(encoding="utf-8")

def run():
    """
    Entry point for running the sponsored job discovery crew.
    """

    # ---- USER INPUTS ----
    user_query = input("Enter your job search query (e.g. 'Data Scientist roles in Texas'): ").strip()
    resume_path = input("Enter path to your resume file: ").strip()

    resume_text = load_resume(resume_path)

    inputs = {
        "user_query": user_query,
        "resume_text": resume_text,
    }

    # ---- MCP LIFECYCLE ----
    start_mcp_adapter()

    try:
        crew = SponsoredJobCrew().crew()
        result = crew.kickoff(inputs=inputs)
        print("\n=== FINAL RESULTS ===\n")
        print(result)

    except Exception as e:
        raise RuntimeError(f"An error occurred while running the crew: {e}")

    finally:
        stop_mcp_adapter()


if __name__ == "__main__":
    run()


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         Gjob().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Gjob().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }

#     try:
#         Gjob().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")

# def run_with_trigger():
#     """
#     Run the crew with trigger payload.
#     """
#     import json

#     if len(sys.argv) < 2:
#         raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

#     try:
#         trigger_payload = json.loads(sys.argv[1])
#     except json.JSONDecodeError:
#         raise Exception("Invalid JSON payload provided as argument")

#     inputs = {
#         "crewai_trigger_payload": trigger_payload,
#         "topic": "",
#         "current_year": ""
#     }

#     try:
#         result = Gjob().crew().kickoff(inputs=inputs)
#         return result
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew with trigger: {e}")
