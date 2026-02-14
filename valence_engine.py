"""
Valence Engine for The Polar Emotion Compass
=============================================
Sentence-based NLP with Top-2 Scalar Blending and Angular Guardrail.

Key Features:
- Sentence chunking for granular analysis
- Local sentence-transformers model (all-MiniLM-L6-v2)
- Top-2 emotion blending with ANGULAR GUARDRAIL (60° max)
- Prevents "Semantic Whiplash" (e.g., blending Happy + Sad)
- SCALAR radius averaging + CARTESIAN angle interpolation
- Lower threshold (0.22) for sensitivity
"""

import numpy as np
import math
import re
from sentence_transformers import SentenceTransformer, util
from emotion_map import EMOTION_MAP

# Global model cache - loaded once at import time
print("Loading sentence transformer model...")
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully!")

# Pre-encode emotion anchors as lowercase text
EMOTION_LABELS = list(EMOTION_MAP.keys())
EMOTION_ANCHORS = [emotion.lower() for emotion in EMOTION_LABELS]
ANCHOR_EMBEDDINGS = MODEL.encode(EMOTION_ANCHORS, convert_to_tensor=False)

print(f"Pre-encoded {len(EMOTION_LABELS)} emotion anchors.")


def polar_to_cartesian(radius: float, angle_degrees: float) -> tuple[float, float]:
    """Convert polar coordinates to Cartesian coordinates."""
    angle_radians = math.radians(angle_degrees)
    x = radius * math.cos(angle_radians)
    y = radius * math.sin(angle_radians)
    return x, y


def cartesian_to_polar(x: float, y: float) -> tuple[float, float]:
    """Convert Cartesian coordinates to polar coordinates."""
    radius = math.sqrt(x**2 + y**2)
    angle_radians = math.atan2(y, x)
    angle_degrees = math.degrees(angle_radians)
    
    # Normalize angle to 0-360 range
    if angle_degrees < 0:
        angle_degrees += 360
    
    return radius, angle_degrees


def calculate_angular_distance(angle1: float, angle2: float) -> float:
    """
    Calculate shortest angular distance between two angles (0-180 degrees).
    
    Args:
        angle1: First angle in degrees (0-360)
        angle2: Second angle in degrees (0-360)
    
    Returns:
        Shortest distance in degrees (0-180)
    """
    diff = abs(angle1 - angle2)
    if diff > 180:
        diff = 360 - diff
    return diff


def calculate_polar_coordinates(user_text: str) -> tuple[float, float, str]:
    """
    Calculate polar coordinates using Top-2 Scalar Blending with Angular Guardrail.
    
    Algorithm:
    1. Split text into sentences
    2. Find sentence with highest peak similarity
    3. Guardrail: if max_score < 0.22, return Neutral
    4. Get top 2 emotions from winning sentence
    5. Calculate angular distance between them
    6. BLEND if: score2 > (score1 * 0.75) AND angle_diff <= 60°
       - SCALAR averaging for radius
       - CARTESIAN interpolation for angle
    7. SNAP if: conflicting emotions or clear winner
    8. Return (radius, angle, closest_emotion)
    
    Args:
        user_text: The journal entry text
    
    Returns:
        Tuple of (radius, angle_degrees, closest_emotion_name)
    """
    if not user_text or not user_text.strip():
        return 0.0, 0, "Neutral"
    
    # Step 1: Sentence Chunking
    sentences = re.split(r'[.!?\n]+', user_text)
    valid_sentences = [s.strip() for s in sentences if s.strip()]
    
    # Step 2: Guardrail - Check if we have valid sentences
    if not valid_sentences:
        return 0.0, 0, "Neutral"
    
    # Step 3: Find the "Winning Sentence"
    best_global_score = 0.0
    best_scores_array = None
    
    for sentence in valid_sentences:
        # Encode the sentence
        sentence_embedding = MODEL.encode(sentence, convert_to_tensor=False)
        
        # Calculate cosine similarities
        similarities = np.dot(ANCHOR_EMBEDDINGS, sentence_embedding) / (
            np.linalg.norm(ANCHOR_EMBEDDINGS, axis=1) * np.linalg.norm(sentence_embedding)
        )
        
        # Find max score for this sentence
        max_score = np.max(similarities)
        
        # Update winning sentence if this is better
        if max_score > best_global_score:
            best_global_score = max_score
            best_scores_array = similarities
    
    # Step 4: Guardrail - Check threshold
    GUARDRAIL_THRESHOLD = 0.22
    if best_global_score < GUARDRAIL_THRESHOLD:
        return 0.0, 0, "Neutral"
    
    # Step 5: Get Top-2 emotions from winning sentence
    top2_indices = np.argsort(best_scores_array)[-2:][::-1]  # Get indices of top 2, descending
    idx1, idx2 = top2_indices[0], top2_indices[1]
    score1, score2 = best_scores_array[idx1], best_scores_array[idx2]
    
    emotion1_name = EMOTION_LABELS[idx1]
    emotion2_name = EMOTION_LABELS[idx2]
    
    emotion1_data = EMOTION_MAP[emotion1_name]
    emotion2_data = EMOTION_MAP[emotion2_name]
    
    # Step 6: Calculate angular distance
    angle1 = emotion1_data["angle"]
    angle2 = emotion2_data["angle"]
    angle_diff = calculate_angular_distance(angle1, angle2)
    
    # Step 7: Conditional Blending with ANGULAR GUARDRAIL
    SCORE_THRESHOLD = 0.75
    ANGULAR_THRESHOLD = 60  # degrees
    
    if score2 > (score1 * SCORE_THRESHOLD) and angle_diff <= ANGULAR_THRESHOLD:
        # BLEND: Emotions are close in both score AND angle
        weight1 = score1 ** 2
        weight2 = score2 ** 2
        total_weight = weight1 + weight2
        
        # SCALAR averaging for radius
        r1 = emotion1_data["radius"]
        r2 = emotion2_data["radius"]
        final_radius = (r1 * weight1 + r2 * weight2) / total_weight
        
        # CARTESIAN interpolation for angle
        x1, y1 = polar_to_cartesian(1.0, angle1)
        x2, y2 = polar_to_cartesian(1.0, angle2)
        
        # Weighted average in Cartesian space
        avg_x = (x1 * weight1 + x2 * weight2) / total_weight
        avg_y = (y1 * weight1 + y2 * weight2) / total_weight
        
        # Convert back to get final angle
        _, final_angle = cartesian_to_polar(avg_x, avg_y)
        
        closest_emotion = emotion1_name  # Primary emotion is still the strongest
    else:
        # SNAP: Conflicting emotions (far apart) or clear winner
        final_radius = emotion1_data["radius"]
        final_angle = emotion1_data["angle"]
        closest_emotion = emotion1_name
    
    # Step 8: Cap radius at 1.0 and return
    final_radius = min(1.0, final_radius)
    
    return final_radius, final_angle, closest_emotion