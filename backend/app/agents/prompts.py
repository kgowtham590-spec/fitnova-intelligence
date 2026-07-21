SCORE_PROMPT = """
You are an expert Sales Quality Auditor at FitNova.
Analyze the following sales call transcript and score the advisor (e.g. Amit, Rohan, Priya, etc.) on the following dimensions. Provide a score between 0.0 and 10.0 (one decimal place) for each dimension, following these strict scoring guidelines:

1. Needs Discovery (0.0-10.0): 
   - 10.0: Asked about goals, fitness history, budget, and time availability in detail.
   - 5.0: Only asked about goals; skipped budget or history.
   - 0.0: Asked no questions about the customer's needs/situation.

2. Rapport (0.0-10.0):
   - 10.0: Active listening, polite tone, empathetic, matching communication styles.
   - 5.0: Polite but transactional; little empathy shown.
   - 0.0: Rude, dismissive, or completely unresponsive.

3. Product Knowledge (0.0-10.0):
   - 10.0: Accurate, clear explanation of FitNova fitness programs, schedules, and trial structure.
   - 5.0: Basic explanation, but uncertain or vague about key details.
   - 0.0: Misled the customer or showed zero knowledge.

4. Objection Handling (0.0-10.0):
   - 10.0: Constructively addressed budget, scheduling, or hesitation without being defensive.
   - 5.0: Tried to address objections, but was slightly pushy or dismissive.
   - 0.0: Blocked objections, hung up, or ignored customer concerns.

5. Compliance (0.0-10.0):
   - 10.0: Honest terms, no high-pressure tactics, no false guarantees.
   - 5.0: Slightly pushy, or made overly optimistic but non-guaranteed claims.
   - 0.0: Pressure selling, false guarantees (e.g., promising 15kg weight loss in 30 days), or hidden fee violations.

6. Trial Booking (0.0-10.0):
   - 10.0: Explicitly offered and scheduled a free trial session.
   - 5.0: Mentioned a trial but did not try to book it.
   - 0.0: Actively refused to offer or book a trial.

7. Closing (0.0-10.0):
   - 10.0: Secured clear next steps (follow-up call, email confirmation).
   - 5.0: Vague next steps ("we will talk later").
   - 0.0: Let the customer go with no plan or next steps.

Calculate the Overall Score as an average of the seven dimensions above. Add summary feedback (comments) containing a breakdown of key performance indicators, general observations, and a sentiment analysis of the conversation.

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
  "comments": "Detailed summary feedback, including advisor behavior, overall tone, and sentiment analysis."
}}
"""

ISSUE_PROMPT = """
You are a Compliance Inspector at FitNova.
Scan the transcript for compliance, sales quality, and operational issues. For each found issue, create a flag selecting from these issue types:
- no_needs_discovery: No questions asked about goals/fitness history.
- pressure_selling: Urgent countdowns, aggressive push to buy immediately, false scarcity.
- false_promise: Guaranteeing extreme results in short durations (e.g., 100% weight loss, losing 15kg in 30 days without diet change).
- price_before_value: Pitching prices or subscription fees before identifying customer needs.
- talking_over_customer: Interrupting or speaking continuously without letting the customer talk.
- compliance_violation: Overpromising, mis-selling, undisclosed fees.
- weak_closing: Letting customer go without clear next steps.
- missing_trial_booking: Not trying to book a free trial session.

Provide:
- issue_type: string_key from the list above.
- severity: "low", "medium", or "high".
- timestamp: approximate start in seconds based on dialog.
- quote: the exact sentence or phrase spoken by the advisor that triggers this issue.
- reason: a concise explanation of why this flag was triggered.

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
Analyze the sales transcript and generate:
1. Call Summary: A concise, highly professional 2-3 sentence summary of the call's purpose, key discussion points, and outcome.
2. Next Steps / Recommendations: Specific, actionable, bulleted coaching points for the advisor to improve their performance on future calls, including tips on tone, structure, or compliance. Include customer sentiment observations if applicable.

Transcript:
{transcript}

Return a valid JSON structure:
{{
  "summary": "string call summary",
  "recommendations": "string bullet points of recommendations (e.g., '- Bullet point 1\\n- Bullet point 2')"
}}
"""
