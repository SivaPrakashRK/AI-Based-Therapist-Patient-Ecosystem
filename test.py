"""
Test Suite for The Polar Emotion Compass
=========================================
Tests the Angular Guardrail with 10 comprehensive test cases.
Outputs expected vs actual results to 'test_results.txt'.
"""

from valence_engine import calculate_polar_coordinates

# 10 comprehensive test cases with expected outputs
test_cases = [
    {
        "name": "Stolen Web App Code",
        "text": "My teammate took credit for the web app code I wrote. I feel betrayed and furious about this situation.",
        "expected": "Furious / Infuriated"
    },
    {
        "name": "Dream School Acceptance",
        "text": "I just got accepted into my dream college! I'm so excited and proud of myself!",
        "expected": "Excited / Euphoric"
    },
    {
        "name": "Overwhelming Final Exams",
        "text": "Final exams are next week and I haven't studied enough. I'm anxious and overwhelmed by everything.",
        "expected": "Overwhelmed / Anxious"
    },
    {
        "name": "Peaceful Weekend Morning",
        "text": "Woke up on Saturday with no deadlines. Just relaxing with coffee and music. I feel peaceful and content.",
        "expected": "Peaceful / Content"
    },
    {
        "name": "Loss of a Loved One",
        "text": "I lost my grandfather yesterday and the house feels so empty. I miss him so much, I feel incredibly sad and lonely.",
        "expected": "Grief / Sad"
    },
    {
        "name": "Forgot Best Friend's Birthday",
        "text": "I completely forgot my best friend's birthday. I feel like a terrible person, so guilty and ashamed.",
        "expected": "Guilty / Ashamed"
    },
    {
        "name": "Imposter Syndrome",
        "text": "Everyone in my class seems so much smarter than me. I feel inadequate and insecure about my abilities.",
        "expected": "Inadequate / Insecure"
    },
    {
        "name": "Unexpected Kindness",
        "text": "My neighbor helped me fix my flat tire in the rain without me even asking. I'm so grateful and touched by their kindness.",
        "expected": "Grateful"
    },
    {
        "name": "Mixed Emotions - Close Angles (Should Blend)",
        "text": "I'm excited about the new job but also nervous about meeting expectations.",
        "expected": "Excited (blended with Nervous if close enough)"
    },
    {
        "name": "Conflicting Emotions - Far Angles (Should NOT Blend)",
        "text": "I'm happy I graduated but sad to leave my friends behind forever.",
        "expected": "Happy (snapped, NOT blended with Sad)"
    }
]

def run_tests():
    output_filename = "test_results.txt"
    
    # Open file for writing
    with open(output_filename, "w", encoding="utf-8") as f:
        # Header
        header = (
            "=" * 80 + "\n"
            "POLAR EMOTION COMPASS - ANGULAR GUARDRAIL TEST RESULTS\n"
            "=" * 80 + "\n\n"
        )
        print(header)
        f.write(header)
        
        for i, test_case in enumerate(test_cases, 1):
            # Calculate emotion
            radius, angle, actual_emotion = calculate_polar_coordinates(test_case['text'])
            
            # Format output
            result_str = (
                f"Test Case {i}: {test_case['name']}\n"
                f"{'-' * 80}\n"
                f"Input:    {test_case['text']}\n"
                f"Expected: {test_case['expected']}\n"
                f"Actual:   {actual_emotion}\n"
                f"Stats:    Intensity={radius:.4f}, Angle={angle:.2f}°\n"
                f"{'=' * 80}\n\n"
            )
            
            # Print to console and file
            print(result_str)
            f.write(result_str)
        
        # Summary
        summary = f"\n{'=' * 80}\nTest results saved to: {output_filename}\n{'=' * 80}\n"
        print(summary)
        f.write(summary)

if __name__ == "__main__":
    run_tests()
