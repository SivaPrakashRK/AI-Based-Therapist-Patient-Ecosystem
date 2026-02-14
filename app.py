"""
The Polar Emotion Compass - Interactive Bubble Wheel UI
========================================================
Zoomed-in polar scatter with clickable emotion bubbles.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from valence_engine import calculate_polar_coordinates
from emotion_map import EMOTION_MAP

# PAGE CONFIGURATION
st.set_page_config(
    page_title="The Polar Emotion Compass",
    page_icon="🧭",
    layout="wide"
)

# CSS INJECTION: Fix scrollbar and viewport
st.markdown("""
<style>
    .main {
        overflow-y: auto !important;
        height: 100vh !important;
    }
    .stApp {
        overflow-y: auto !important;
    }
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "selected_emotion" not in st.session_state:
    st.session_state["selected_emotion"] = "Neutral"

# HELPERS
def get_time_of_day():
    """Categorize current hour into time period."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

# BUILD BUBBLE WHEEL DATAFRAME
def build_wheel_df(selected_emotion):
    """Convert EMOTION_MAP to a DataFrame with highlight color."""
    rows = []
    for emotion, data in EMOTION_MAP.items():
        if emotion == "Neutral":
            continue  # Skip neutral in the wheel
        rows.append({
            "emotion": emotion,
            "radius": data["radius"],
            "angle": data["angle"],
            "energy": data["energy"],
            "desc": data["desc"],
            "color": "red" if emotion == selected_emotion else "lightblue",
            "size": 10
        })
    return pd.DataFrame(rows)

# MAIN APPLICATION
st.title("🧭 The Polar Emotion Compass")
st.markdown("**Interactive Bubble Wheel — click, zoom, and explore your emotions.**")

# LAYOUT: left input | right wheel
col_input, col_wheel = st.columns([1, 2])

# LEFT COLUMN — Input Controls
with col_input:
    st.subheader("🎯 Manual Override")
    emotion_keys = list(EMOTION_MAP.keys())
    default_idx = emotion_keys.index(st.session_state["selected_emotion"]) if st.session_state["selected_emotion"] in emotion_keys else 0
    manual_emotion = st.selectbox(
        "Select Emotion",
        emotion_keys,
        index=default_idx
    )
    # Update session state when manually changed
    if manual_emotion != st.session_state["selected_emotion"]:
        st.session_state["selected_emotion"] = manual_emotion

    st.markdown("---")

    st.subheader("📋 Context")
    ctx1, ctx2 = st.columns(2)
    with ctx1:
        theme = st.selectbox("Theme", ["Academic", "Freelance", "Relationships", "Health", "Other"])
    with ctx2:
        location = st.selectbox("Location", ["Desk Setup", "College", "Public", "Other"])

    st.markdown("---")

    st.subheader("✍️ Journal")
    user_text = st.text_area(
        "How are you feeling?",
        height=150,
        placeholder="Write freely. The engine picks the strongest sentence."
    )

    if st.button("📊 Log Emotion", type="primary", use_container_width=True):
        if user_text and user_text.strip():
            radius, angle, detected = calculate_polar_coordinates(user_text)
            st.session_state["selected_emotion"] = detected

            # Display result
            if detected == "Neutral":
                st.warning("🤷 Neutral — no strong emotion detected.")
            else:
                meta = EMOTION_MAP.get(detected, {})
                st.success(f"**{detected}** — {meta.get('desc', '')}")
                st.caption(f"Intensity: {radius:.3f} | Angle: {angle:.1f}° | Energy: {meta.get('energy', 'N/A')}")

            # CSV export section
            time_of_day = get_time_of_day()
            export_df = pd.DataFrame([{
                "Exact_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Time_of_Day": time_of_day,
                "Theme": theme,
                "Location": location,
                "Journal": user_text,
                "Radius": round(radius, 4),
                "Angle": round(angle, 2),
                "Emotion": detected,
                "Energy": meta.get("energy", "N/A")
            }])
            csv = export_df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                file_name=f"emotion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.error("Please write something first!")

# RIGHT COLUMN — The Interactive Bubble Wheel
with col_wheel:
    st.subheader("🫧 Emotion Bubble Wheel")

    df = build_wheel_df(st.session_state["selected_emotion"])

    fig = px.scatter_polar(
        df,
        r="radius",
        theta="angle",
        color="color",
        color_discrete_map={"red": "crimson", "lightblue": "lightskyblue"},
        size="size",
        size_max=18,
        hover_name="emotion",
        hover_data={"energy": True, "desc": True, "color": False, "size": False, "radius": ":.2f", "angle": ":.0f"},
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                range=[0, 0.5],
                showticklabels=True,
                ticks="outside",
                gridcolor="rgba(200,200,200,0.3)"
            ),
            angularaxis=dict(
                direction="clockwise",
                rotation=90,
                tickmode="array",
                tickvals=[0, 60, 120, 180, 240, 300],
                ticktext=["Joy ☀️", "Anger 🔥", "Fear 😨", "Sad 💧", "Bad 🌑", "Peaceful 🍃"],
                tickfont=dict(size=13)
            ),
            bgcolor="rgba(245,245,250,0.4)"
        ),
        showlegend=False,
        height=700,
        margin=dict(t=40, b=40),
        paper_bgcolor="white"
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color="DarkSlateGrey")),
    )

    st.plotly_chart(fig, use_container_width=True)

    sel = st.session_state["selected_emotion"]
    if sel != "Neutral" and sel in EMOTION_MAP:
        meta = EMOTION_MAP[sel]
        st.info(f"**{sel}** — {meta['desc']}  \nEnergy: **{meta['energy']}** | Radius: {meta['radius']} | Angle: {meta['angle']}°")
    else:
        st.caption("Select or detect an emotion to highlight it on the wheel.")
