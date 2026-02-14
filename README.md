# The Polar Emotion Compass

**A Privacy-First, Deterministic Emotional Journaling Web Application**

> Final Year Project | Zero-Storage Architecture | Local NLP Processing

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Technical Architecture](#technical-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Algorithm Deep Dive](#algorithm-deep-dive)
- [File Structure](#file-structure)
- [Privacy & Security](#privacy--security)
- [Future Enhancements](#future-enhancements)

---

## Overview

The Polar Emotion Compass replaces traditional chatbot-based emotion tracking with a **deterministic mathematical engine**. Users write journal entries, and the system uses local NLP to map their emotional state onto a 2D polar coordinate grid (the Feeling Wheel).

### Core Philosophy
**No LLMs. No APIs. No Databases. Just Math.**

All processing happens locally on the user's device. No data is transmitted, stored in databases, or sent to external services.

---

## Key Features

### Privacy-First Design
- **Zero external API calls** - All processing is local
- **No database storage** - In-memory session only
- **No cloud uploads** - Data never leaves your device
- **Export to CSV** - Download your data for personal records

### Mathematical Precision
- **Deterministic output** - Same input always produces same result
- **Top-2 Scalar Blending** - Advanced emotion blending algorithm
- **Conditional blending logic** - SCALAR radius averaging + CARTESIAN angle interpolation
- **6-sector emotion wheel** - 48 emotions across 6 primary sectors at 60° intervals

### Advanced NLP
- **Sentence transformers** - `all-MiniLM-L6-v2` model (~80MB)
- **Semantic matching** - Cosine similarity against emotion anchors
- **Threshold filtering** - 0.30 confidence threshold
- **Local inference** - No GPU required

---

## Technical Architecture

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Web UI framework |
| **Visualization** | Plotly Express | Interactive polar plots |
| **NLP Engine** | sentence-transformers | Semantic text encoding |
| **Math** | NumPy | Vector operations & trigonometry |
| **Data Export** | Pandas | CSV generation |

### System Architecture

```
┌─────────────────────────────────────────────────┐
│           Streamlit Web Interface               │
│  (Grounding Context + Journal Entry + Export)   │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│         Valence Engine (NLP + Math)             │
│  • Encode text with sentence-transformers      │
│  • Calculate cosine similarities                │
│  • Apply exponential weighting (square)         │
│  • Threshold filtering (0.30)                   │
│  • Cartesian weighted averaging                 │
│  • Polar coordinate conversion                  │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│           Emotion Map (Constants)               │
│  • 6 sectors × 8 emotions per sector            │
│  • 48 emotions total (47 + Neutral)             │
│  • Deterministic polar coordinates              │
└─────────────────────────────────────────────────┘
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- ~200MB free disk space (for model)

### Step-by-Step Installation

1. **Navigate to project directory:**
   ```bash
   cd "d:\College\Final Year Project"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - `streamlit` - Web UI
   - `plotly` - Visualization
   - `sentence-transformers` - NLP model
   - `numpy` - Math operations
   - `pandas` - Data export
   - `torch` - ML backend

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the web interface:**
   - Open browser to `http://localhost:8501`
   - First run will download the model (~80MB, one-time only)

---

## Usage Guide

### 1. Set Grounding Context
- **Theme**: Select life area (Academic, Freelance, Relationships, Health, Other)
- **Location**: Select physical location (Desk Setup, College, Public, Other)

### 2. Write Journal Entry
Express your thoughts and feelings in natural language:
```
Example: "I'm feeling overwhelmed with all these deadlines. 
The pressure is getting to me and I can't seem to focus."
```

### 3. Calculate Emotion
Click **"Calculate Emotion"** to analyze your entry.

### 4. View Results
- **Polar plot**: Visual representation of your emotional state
- **Metrics**: Closest emotion, intensity (radius), angle, time of day
- **Context**: Your selected theme and location

### 5. Export Data
Download your session data as CSV with columns:
- Exact Time
- Time of Day (Morning/Afternoon/Evening/Night)
- Theme
- Location
- Journal Entry
- Radius (0.0-1.0)
- Angle (0-360°)
- Closest Emotion

---

## Algorithm Deep Dive

### Emotion Wheel Geometry

The emotion wheel uses a **hexagonal design** with 6 primary sectors at 60° intervals, each containing 8 distinct emotions:

| Sector | Angle Range | Sample Emotions (8 total per sector) |
|--------|-------------|---------------------------------------|
| **Joy** | 330°-30° | Happy, Grateful, Excited, Optimistic, Euphoric, Proud, Confident, Accomplished |
| **Anger** | 30°-90° | Mad, Irritated, Frustrated, Infuriated, Furious, Resentful, Bitter, Jealous |
| **Fear** | 90°-150° | Scared, Nervous, Anxious, Overwhelmed, Terrified, Insecure, Helpless, Inadequate |
| **Sad** | 150°-210° | Sad, Hurt, Lonely, Isolated, Grief, Disappointed, Depressed, Despair |
| **Bad/Disgust** | 210°-270° | Bad, Tired, Bored, Apathetic, Disgusted, Guilty, Repelled, Ashamed |
| **Peaceful** | 270°-330° | Peaceful, Content, Relaxed, Serene, Surprised, Trusting, Awestruck, Intimate |

**Total Emotions: 48** (47 active emotions + 1 Neutral state)

**Radius levels:**
- 0.3 = Low intensity
- 0.5-0.6 = Moderate intensity
- 0.7-0.8 = High intensity
- 0.9 = Extreme intensity

### NLP Pipeline

#### Step 1: Text Encoding
```python
user_embedding = MODEL.encode(user_text)
# Converts text to 384-dimensional vector
```

#### Step 2: Semantic Matching
```python
similarities = cosine_similarity(user_embedding, anchor_embeddings)
# Compares against 48 emotion anchors (47 emotions + Neutral)
```

#### Step 3: Top-2 Scalar Blending
The system uses an advanced blending algorithm that combines the top 2 emotions:

```python
# Select top 2 emotions by similarity score
top_2_emotions = get_top_2_by_similarity(similarities)

# SCALAR blending for radius (simple average)
blended_radius = (radius_1 + radius_2) / 2

# CARTESIAN blending for angle (mathematically correct)
x1, y1 = polar_to_cartesian(radius_1, angle_1)
x2, y2 = polar_to_cartesian(radius_2, angle_2)
avg_x = (x1 + x2) / 2
avg_y = (y1 + y2) / 2
blended_angle = cartesian_to_polar(avg_x, avg_y)
```

**Why Top-2 Blending?**
- Captures emotional nuance (e.g., "anxious but hopeful")
- Avoids dilution from weak signals
- Mathematically stable and deterministic

#### Step 4: Threshold Filtering
```python
if max(similarities) < 0.30:
    return (0.0, 0, "Neutral")
```

#### Step 5: Closest Emotion Matching
After blending, the system finds the closest predefined emotion:

```python
# Calculate distance to all 48 emotions
for emotion in EMOTION_MAP:
    distance = sqrt((r - emotion.radius)² + angular_distance(θ, emotion.angle)²)

# Return the emotion with minimum distance
closest_emotion = min(distances)
```

#### Step 6: Output
Returns `(radius, angle, closest_emotion_name)`

---

## File Structure

```
Final Year Project/
├── emotion_map.py          # Emotion → Polar coordinate mappings
├── valence_engine.py       # NLP processing & trigonometry
├── app.py                  # Streamlit web interface
├── requirements.txt        # Python dependencies
└── README.md              # This documentation
```

### `emotion_map.py`
- **Purpose**: Define deterministic emotion mappings
- **Structure**: Dictionary with 48 emotions (47 + Neutral)
- **Data**: Each emotion has:
  - `radius` (0.0-0.9): Intensity level
  - `angle` (0-360°): Position on emotion wheel
  - `energy` (Low/Moderate/High/Extreme): Energy classification
  - `desc`: Human-readable description for UI tooltips

### `valence_engine.py`
- **Purpose**: Core NLP and mathematical engine
- **Model**: sentence-transformers `all-MiniLM-L6-v2`
- **Functions**:
  - `polar_to_cartesian()` - Convert polar to Cartesian
  - `cartesian_to_polar()` - Convert Cartesian to polar
  - `calculate_polar_coordinates()` - Main analysis function

### `app.py`
- **Purpose**: User interface and interaction
- **Features**:
  - Wide layout with CSS scrolling fix
  - Grounding context inputs (Theme, Location)
  - Journal entry text area
  - Polar visualization (fixed 500px height)
  - Auto-timing categorization
  - CSV export functionality

---

## Privacy & Security

### Data Flow
```
User Input → Local NLP Model → In-Memory Processing → Display/Export
```

### Privacy Guarantees

| Aspect | Implementation |
|--------|----------------|
| **Storage** | Session-only (in-memory), deleted on tab close |
| **Network** | No external API calls, no data transmission |
| **Processing** | 100% local on user's device |
| **Export** | CSV file saved to user's local filesystem only |
| **Model** | Downloaded once, cached locally |

### Security Features
- No authentication required (no accounts)
- No server-side data storage
- No cookies or tracking
- No third-party services
- No telemetry or analytics

---

## Future Enhancements

### Potential Improvements

1. **Multi-language Support**
   - Add multilingual sentence-transformer models
   - Support emotion detection in Hindi, Spanish, etc.

2. **Advanced Visualizations**
   - Emotion trajectory over time
   - Heat maps showing emotional patterns
   - Comparative analysis (week-over-week)

3. **Enhanced Emotion Wheel**
   - Add more granular emotions (8 or 12 sectors)
   - Support custom emotion definitions
   - Intensity blending between sectors

4. **Offline PWA**
   - Convert to Progressive Web App
   - Install on mobile devices
   - Work completely offline

5. **Data Analysis**
   - Pattern recognition in exported CSV
   - Correlation analysis (theme vs. emotion)
   - Time-of-day emotional trends

6. **Export Formats**
   - JSON export for data science workflows
   - PDF reports with visualizations
   - Integration with journaling apps

---

## Technical Specifications

### Model Details
- **Name**: `all-MiniLM-L6-v2`
- **Type**: Sentence transformer
- **Embedding dimension**: 384
- **Model size**: ~80MB
- **Inference speed**: ~50ms per encoding
- **Hardware**: CPU-only (no GPU required)

### Performance
- **First load**: 5-10 seconds (model download + initialization)
- **Subsequent loads**: <1 second (cached model)
- **Analysis time**: <500ms per journal entry
- **Memory usage**: ~300MB (model + embeddings)

### Browser Compatibility
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Mobile browsers (limited due to Streamlit)

---

## Troubleshooting

### Common Issues

**Issue**: Model download fails
- **Solution**: Check internet connection, retry installation

**Issue**: Plot not visible
- **Solution**: Scroll down (CSS fix applied), or resize browser window

**Issue**: "Neutral" for all entries
- **Solution**: Write more descriptive emotional language, increase entry length

**Issue**: Streamlit not found
- **Solution**: Run `pip install -r requirements.txt` again

---

## Academic Context

### Research Foundation
This project demonstrates:
- **Applied NLP**: Practical use of transformer models
- **Mathematical modeling**: Vector space emotion representation
- **Privacy engineering**: Zero-storage architecture design
- **UI/UX**: Accessible emotional health tooling

### Key Innovations
1. **Top-2 Scalar Blending** - Advanced emotion blending with conditional logic
2. **Deterministic** emotion mapping (reproducible results)
3. **Privacy-first** architecture (no data collection)
4. **48-emotion system** - Comprehensive emotional granularity across 6 sectors

---

## License & Attribution

This project is developed as a Final Year Project for educational purposes.

**Technologies Used:**
- [Streamlit](https://streamlit.io/) - Web framework
- [Plotly](https://plotly.com/) - Visualization library
- [sentence-transformers](https://www.sbert.net/) - NLP models
- [NumPy](https://numpy.org/) - Numerical computing
- [Pandas](https://pandas.pydata.org/) - Data manipulation

---

## Contact & Support

For questions, issues, or contributions related to this Final Year Project, please refer to the project repository or contact the developer.

---

**Built with Mathematics and Privacy in Mind**

*Privacy-First • Deterministic • Local • Open Source*
