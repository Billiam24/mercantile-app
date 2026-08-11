import time

print("=" * 50)
print(" WEALTH ADVISOR MEETING FOLLOW-UP TOOL (AI)")
print("=" * 50 + "\n")

# 1. Collect inputs
client_name = input("Client Name: ")
investment_goal = input("Primary Goal: ")
rough_notes = input("Rough Meeting Notes: ")

print("\n[AI Engine] Analyzing meeting notes and generating email draft...")
time.sleep(1.5) # Simulates AI processing time

# 2. Format AI Draft
ai_draft = f"""
Dear {client_name},

Thank you for taking the time to meet with me today. It was great discussing your financial roadmap, specifically your focus on {investment_goal}.

Based on our conversation, I noted the following key priorities:
- Strategy focus: {rough_notes}
- Goal alignment: Tailoring portfolio adjustments toward {investment_goal}

Please review these points and let me know if you would like to make any adjustments to your current strategy before our next review.

Best regards,

Your Wealth Management Team
"""

# 3. Output result
print("\n" + "=" * 50)
print("--- GENERATED DRAFT FOR ADVISOR REVIEW ---")
print("=" * 50)
print(ai_draft)