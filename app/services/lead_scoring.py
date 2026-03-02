"""
Lead Scoring Service
--------------------
Contains business intelligence logic for calculating lead score.

This file is intentionally separated from models and routes
to keep business logic clean and scalable.
"""


def calculate_lead_score(business) -> int:
    """
    Calculate dynamic lead score for a Business instance.

    Scoring Factors:
    - Website Quality (0–20)
    - Phone Presence (0–15)
    - Google Rating (0–25)
    - Review Volume (0–20)
    - Name Intelligence (+/-10)

    Final score is capped between 0 and 100.
    """

    score = 0

    # -----------------------------------
    # 1️⃣ Website Quality (0–20)
    # -----------------------------------
    if business.website:
        website = business.website.lower()

        # Penalize social-only links
        if any(social in website for social in ["facebook", "instagram", "linkedin"]):
            score += 5
        else:
            score += 20

    # -----------------------------------
    # 2️⃣ Phone Presence (0–15)
    # -----------------------------------
    if business.phone and business.phone != "N/A":
        score += 15

    # -----------------------------------
    # 3️⃣ Google Rating (0–25)
    # Rating scale: 0–5
    # -----------------------------------
    if business.rating:
        try:
            rating_score = int(float(business.rating) * 5)
            score += min(rating_score, 25)
        except (ValueError, TypeError):
            pass

    # -----------------------------------
    # 4️⃣ Review Volume (0–20)
    # -----------------------------------
    if business.reviews:
        try:
            reviews = int(business.reviews)

            if reviews >= 1000:
                score += 20
            elif reviews >= 300:
                score += 17
            elif reviews >= 100:
                score += 14
            elif reviews >= 50:
                score += 10
            elif reviews >= 10:
                score += 5
            else:
                score += 2

        except (ValueError, TypeError):
            pass

    # -----------------------------------
    # 5️⃣ Name Intelligence (+/-10)
    # -----------------------------------
    if business.name:
        name = business.name.lower()

        # Private sector boost
        if any(word in name for word in ["private", "medical center", "clinic", "specialist"]):
            score += 5

        # Government penalty
        if any(word in name for word in ["government", "public hospital", "general hospital"]):
            score -= 10

    # -----------------------------------
    # Final Safety Cap
    # -----------------------------------
    return max(min(score, 100), 0)