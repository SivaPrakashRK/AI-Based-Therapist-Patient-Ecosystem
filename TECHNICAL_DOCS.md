# The Polar Emotion Compass - Technical Documentation

## Project Overview
Privacy-first emotional journaling application using local NLP and deterministic mathematical mapping to visualize emotions on a polar coordinate system.

## Architecture Summary

### Core Components
1. **emotion_map.py** - 19 emotions mapped to polar coordinates (6 sectors × 3 intensities)
2. **valence_engine.py** - NLP engine with exponential weighting and Cartesian averaging
3. **app.py** - Streamlit web interface with CSV export

### Algorithm Flow
```
Text Input → Encode (384-dim vector) → Cosine Similarity → 
Exponential Weighting (square) → Threshold Filter (0.30) → 
Cartesian Averaging → Polar Conversion → Output (r, θ, emotion)
```

## Key Technical Decisions

### 1. Exponential Weighting
**Purpose**: Emphasize peak emotional signals  
**Implementation**: Square similarity scores before weighted averaging  
**Effect**: Peak signal gets quadratic emphasis over secondary signals

### 2. Cartesian Averaging
**Problem**: Direct angle averaging is mathematically incorrect  
**Solution**: Convert to (x,y), weight & average, convert back to polar  
**Example**: (350° + 10°) → Cartesian avg → 0° (correct)

### 3. Threshold Filtering
**Value**: 0.30 cosine similarity  
**Rationale**: Balance between sensitivity and confidence  
**Fallback**: Return Neutral (0, 0°) if below threshold

### 4. 6-Sector Design
**Geometry**: 60° intervals forming hexagon  
**Sectors**: Joy (0°), Anger (60°), Fear (120°), Sad (180°), Bad (240°), Peaceful (300°)  
**Intensities**: Core (0.3), Medium (0.6), High (0.9)

## Privacy Architecture

### Zero-Storage Design
- **No database**: All data in `st.session_state` (memory only)
- **No API calls**: Model runs locally
- **No transmission**: Data never leaves device
- **Session-based**: Cleared on tab close
- **Export only**: User controls data via CSV download

### Data Flow
```
User Input → RAM → Display → [Optional] CSV Export to Local Filesystem
          ↓
       (Deleted on close)
```

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Model size | ~80MB (one-time download) |
| RAM usage | ~300MB |
| Encoding time | ~50ms |
| Total analysis | <500ms |
| First load | 5-10s (model init) |
| Subsequent | <1s |

## UI Fixes Applied

### Scrolling Issue
**Problem**: Plotly chart pushed content off-screen  
**Solution**: CSS injection
```css
.main { overflow-y: auto !important; height: 100vh !important; }
section.main { overflow: visible !important; }
```

### Fixed Height
**Chart height**: 500px to prevent overflow

## File Details

### emotion_map.py (30 lines)
- Dictionary: `EMOTION_MAP`
- Structure: `{emotion: {angle: float, radius: float}}`
- Emotions: 18 + Neutral

### valence_engine.py (150 lines)
- Model: `all-MiniLM-L6-v2`
- Functions: 3 (polar↔cartesian, calculate)
- Pre-encoded: 19 emotion anchors

### app.py (200 lines)
- Framework: Streamlit (wide layout)
- Sections: Context, Journal, Analysis, Export
- Features: Auto-timing, CSV download, polar plot

## Dependencies
```
streamlit >= 1.28.0       # Web UI
plotly >= 5.17.0          # Visualization
sentence-transformers >= 2.2.2  # NLP
numpy >= 1.24.0           # Math
pandas >= 2.0.0           # Export
torch >= 2.0.0            # ML backend
```

## Future Enhancements
1. Multi-language support (multilingual models)
2. Emotion trajectory visualization over time
3. PWA conversion for offline mobile use
4. Advanced analytics on exported CSV
5. Custom emotion definitions

## Testing Recommendations
1. **Basic functionality**: Enter text, verify plot appears
2. **Threshold behavior**: Test weak emotional text → expect Neutral
3. **Peak emphasis**: Test mixed emotions → verify strongest wins
4. **Export**: Generate multiple entries, download CSV, verify format
5. **Privacy**: Refresh page, verify data cleared

## Known Limitations
1. CPU-only (no GPU acceleration)
2. English language only (model limitation)
3. Session-based storage (no persistence)
4. Streamlit requires desktop browser (mobile limited)

## Academic Contributions
- Demonstrates **privacy-by-design** architecture
- Novel **exponential weighting** for emotion detection
- Mathematically correct **Cartesian vector averaging**
- **Zero-storage** emotional health application

---

**Version**: 2.0  
**Last Updated**: February 2026  
**Status**: Production-ready
