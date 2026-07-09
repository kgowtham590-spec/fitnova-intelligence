SCORE_PROMPT = """
You are an expert Sales Quality Auditor at FitNova.
Analyze the following sales call transcript and score the advisor (Amit/Rohan/Priya etc.) on the following dimensions:
1. Needs Discovery (0-10): Asking questions to discover budget, goals, current status.
2. Rapport (0-10): Tone, friendliness, matching communication styles.
3. Product Knowledge (0-10): Correct explanation of fitness programs.
4. Objection Handling (0-10): Responding constructively to budget, timing, or trust issues.
5. Compliance (0-10): Giving accurate terms, no pushy tactics, no false guarantees.
6. Trial Booking (0-10): Clear effort to book a trial session.
7. Closing (0-10): Securing next step.

Calculate the Overall Score as an average of these. Add summary feedback.
Transcript:
{transcript}

Return a valid JSON structure:
{{
  "needs_discovery": float,
  "rapport": float,
  "product_knowledge": float,
  "objection_handling": float,
  "compliance": float,
  "trial_booking": float,
  "closing": float,
  "overall_score": float,
  "comments": "string summary feedback"
}}
"""

ISSUE_PROMPT = """
You are a Compliance Inspector at FitNova.
Scan the transcript for the following issues. For each found issue, create a flag:
- no_needs_discovery: No questions asked about goals/fitness history.
- pressure_selling: Urgent countdowns, aggressive push to buy immediately.
- false_promise: Guaranteeing 100% weight loss in short durations (e.g. 15kg in 30 days).
- price_before_value: Pitching price before identifying customer needs.
- talking_over_customer: Interrupting or speaking continuously without pausing.
- compliance_violation: Overpromising, mis-selling, undisclosed fees.
- weak_closing: Letting customer go without clear next steps.
- missing_trial_booking: Not trying to book a free trial session.

Provide the timestamp (approximate start in seconds based on dialog), exact quote from advisor, severity (low, medium, high), and short reasoning.

Transcript:
{transcript}

Return a valid JSON structure:
{{
  "issues": [
    {{
      "issue_type": "string_key",
      "severity": "low|medium|high",
      "timestamp": float,
      "quote": "exact quote from transcript",
      "reason": "explanation of flag"
    }}
  ]
}}
"""

SUMMARY_PROMPT = """
Analyze the transcript and generate:
1. Call Summary: A brief 2-3 sentence summary of the conversation.
2. Next Steps / Recommendations: Actionable tips for the advisor to improve their performance next time.

Transcript:
{transcript}

Return JSON:
{{
  "summary": "string summary",
  "recommendations": "string bullet points of recommendations"
}}
"""
