"""
Emotion Map for The Polar Emotion Compass
==========================================
Defines the polar coordinate system for emotions with UI metadata.

Each emotion has:
- radius: Intensity (0.0 = neutral, 0.9 = maximum)
- angle: Direction in degrees (0-360)
- energy: Energy level (Low / Moderate / High / Extreme)
- desc: Short description for tooltip display
"""

EMOTION_MAP = {
    # Joy (330° to 30°)
    "Happy": {"radius": 0.3, "angle": 0, "energy": "Moderate", "desc": "A general sense of pleasure and contentment."},
    "Grateful": {"radius": 0.5, "angle": 5, "energy": "Moderate", "desc": "Warm appreciation for something received or experienced."},
    "Excited": {"radius": 0.6, "angle": 10, "energy": "High", "desc": "Eager anticipation and energetic enthusiasm."},
    "Optimistic": {"radius": 0.7, "angle": 15, "energy": "High", "desc": "A hopeful confidence about the future."},
    "Euphoric": {"radius": 0.9, "angle": 15, "energy": "Extreme", "desc": "Intense, overwhelming joy and elation."},
    "Proud": {"radius": 0.6, "angle": 350, "energy": "High", "desc": "Deep satisfaction from personal achievement."},
    "Confident": {"radius": 0.9, "angle": 350, "energy": "High", "desc": "Strong belief in one's own abilities and worth."},
    "Accomplished": {"radius": 0.8, "angle": 355, "energy": "High", "desc": "Fulfillment from completing a meaningful goal."},

    # Anger (30° to 90°)
    "Mad": {"radius": 0.3, "angle": 60, "energy": "Moderate", "desc": "A mild, simmering irritation or displeasure."},
    "Irritated": {"radius": 0.5, "angle": 55, "energy": "Moderate", "desc": "Annoyed by a persistent minor disturbance."},
    "Frustrated": {"radius": 0.6, "angle": 50, "energy": "High", "desc": "Blocked from achieving a goal, feeling stuck."},
    "Infuriated": {"radius": 0.9, "angle": 50, "energy": "Extreme", "desc": "Extreme anger at a perceived injustice."},
    "Furious": {"radius": 0.9, "angle": 65, "energy": "Extreme", "desc": "Explosive, uncontainable rage."},
    "Resentful": {"radius": 0.6, "angle": 70, "energy": "Moderate", "desc": "Lingering bitterness from past unfair treatment."},
    "Bitter": {"radius": 0.8, "angle": 75, "energy": "High", "desc": "Deep-seated anger hardened over time."},
    "Jealous": {"radius": 0.9, "angle": 75, "energy": "Extreme", "desc": "Painful envy of what others possess or achieve."},

    # Fear (90° to 150°)
    "Scared": {"radius": 0.3, "angle": 120, "energy": "Moderate", "desc": "A basic sense of fear from a perceived threat."},
    "Nervous": {"radius": 0.5, "angle": 115, "energy": "Moderate", "desc": "Uneasy anticipation about an upcoming event."},
    "Anxious": {"radius": 0.6, "angle": 110, "energy": "High", "desc": "Persistent worry and unease about the future."},
    "Overwhelmed": {"radius": 0.9, "angle": 110, "energy": "Extreme", "desc": "Completely buried under pressure and demands."},
    "Terrified": {"radius": 0.9, "angle": 125, "energy": "Extreme", "desc": "Paralysing fear that shuts down rational thought."},
    "Insecure": {"radius": 0.6, "angle": 130, "energy": "Moderate", "desc": "Self-doubt about one's value or competence."},
    "Helpless": {"radius": 0.8, "angle": 135, "energy": "High", "desc": "Feeling powerless with no way to change a situation."},
    "Inadequate": {"radius": 0.9, "angle": 135, "energy": "Extreme", "desc": "A deep belief of not being good enough."},

    # Sad (150° to 210°)
    "Sad": {"radius": 0.3, "angle": 180, "energy": "Low", "desc": "A gentle, quiet unhappiness."},
    "Hurt": {"radius": 0.7, "angle": 175, "energy": "High", "desc": "Emotional pain caused by someone's actions or words."},
    "Lonely": {"radius": 0.6, "angle": 170, "energy": "Low", "desc": "A painful sense of social isolation and disconnection."},
    "Isolated": {"radius": 0.9, "angle": 170, "energy": "Low", "desc": "Cut off from all meaningful human connection."},
    "Grief": {"radius": 0.9, "angle": 185, "energy": "Extreme", "desc": "Profound sorrow from a significant loss."},
    "Disappointed": {"radius": 0.6, "angle": 190, "energy": "Low", "desc": "Let down when reality falls short of expectations."},
    "Depressed": {"radius": 0.8, "angle": 195, "energy": "Low", "desc": "A heavy, persistent sadness and loss of interest."},
    "Despair": {"radius": 0.9, "angle": 195, "energy": "Extreme", "desc": "Complete loss of hope and the will to continue."},

    # Bad / Disgust (210° to 270°)
    "Bad": {"radius": 0.3, "angle": 240, "energy": "Low", "desc": "A vague, undefined negative feeling."},
    "Tired": {"radius": 0.5, "angle": 235, "energy": "Low", "desc": "Mentally or physically drained of energy."},
    "Bored": {"radius": 0.6, "angle": 230, "energy": "Low", "desc": "Weary and restless from lack of stimulation."},
    "Apathetic": {"radius": 0.9, "angle": 230, "energy": "Low", "desc": "Complete absence of interest or motivation."},
    "Disgusted": {"radius": 0.8, "angle": 245, "energy": "High", "desc": "Strong revulsion towards something offensive."},
    "Guilty": {"radius": 0.6, "angle": 250, "energy": "Moderate", "desc": "Remorse for having done something wrong."},
    "Repelled": {"radius": 0.9, "angle": 255, "energy": "High", "desc": "Intense aversion driving you to pull away."},
    "Ashamed": {"radius": 0.9, "angle": 250, "energy": "High", "desc": "Deep embarrassment about who you are or what you did."},

    # Peaceful (270° to 330°)
    "Peaceful": {"radius": 0.3, "angle": 300, "energy": "Low", "desc": "A calm, undisturbed state of mind."},
    "Content": {"radius": 0.5, "angle": 295, "energy": "Low", "desc": "Quietly satisfied with the present moment."},
    "Relaxed": {"radius": 0.6, "angle": 290, "energy": "Low", "desc": "Free from tension, at ease physically and mentally."},
    "Serene": {"radius": 0.9, "angle": 290, "energy": "Low", "desc": "A profound, unshakable inner tranquility."},
    "Surprised": {"radius": 0.7, "angle": 305, "energy": "High", "desc": "Caught off guard by something unexpected."},
    "Trusting": {"radius": 0.6, "angle": 310, "energy": "Moderate", "desc": "A secure feeling of reliance on someone."},
    "Awestruck": {"radius": 0.8, "angle": 315, "energy": "High", "desc": "Overwhelmed by wonder and admiration."},
    "Intimate": {"radius": 0.9, "angle": 310, "energy": "Moderate", "desc": "A deep emotional closeness and vulnerability."},

    "Neutral": {"radius": 0.0, "angle": 0, "energy": "Low", "desc": "No strong emotional signal detected."}
}