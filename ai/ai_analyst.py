from .prompts import PROMPT


def analyze_with_ai(report):
    """
    Placeholder for future AI (Gemini/OpenAI) integration.
    Currently just displays the generated incident report.
    """

    print("\n")
    print("=" * 60)
    print("AI SECURITY ANALYST")
    print("=" * 60)

    print(PROMPT)

    print("\nIncident Sent To AI:\n")

    print(report)

    print("\n")
    print("AI Integration Coming Next...")