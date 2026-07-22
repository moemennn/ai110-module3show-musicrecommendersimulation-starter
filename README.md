# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation systems often combine many signals, such as what users listen to, save, skip, or replay, with information about the content itself. In this simulation, I will build a simple content-based recommender that prioritizes songs matching a user’s preferred style and vibe, especially genre, mood, and energy, while also using other audio-style features to make the recommendations feel more personalized.

The simulation uses the following features:

- `Song` features:
  - `id`, `title`, and `artist`
  - `genre`
  - `mood`
  - `energy`
  - `tempo_bpm`
  - `valence`
  - `danceability`
  - `acousticness`

- `UserProfile` features:
  - `favorite_genre`
  - `favorite_mood`
  - `target_energy`
  - `likes_acoustic`

The recommender will score each song against the user profile and rank the highest-matching songs at the top of the list.

### Data Flow Diagram

See [docs/data_flow_diagram.md](docs/data_flow_diagram.md) for the diagram.

### Algorithm Recipe

My recommender will use a simple content-based recipe:

1. Compare each song to a user taste profile made of preferred genre, mood, energy, tempo, valence, and acoustic preference.
2. Give each song a score based on how closely it matches those preferences.
3. Reward songs that are close to the user’s target values rather than just “higher” or “lower” on a feature.
4. Rank all songs by score and return the top $k$ recommendations.
5. Provide a short explanation for each recommendation, such as matching mood or energy.

### Expected Biases

This system may over-prioritize obvious style features such as genre and mood, which could cause it to miss great songs that are less obvious but still a strong fit. It may also be too narrow for users with changing tastes because it relies on a single fixed profile.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Below is the actual terminal output from running `python -m src.main` with the
default profile (`genre=pop`, `mood=happy`, `energy=0.8`):

```
Loading songs from data/songs.csv...
Loaded songs: 18

============================================================
Top 5 recommendations for pop / happy (energy 0.8)
============================================================

1. Sunrise City — Neon Echo
   Score:  6.94
   Reasons: genre match (+2.0); mood match (+2.0); energy similarity (+2.94)

2. Rooftop Lights — Indigo Parade
   Score:  4.88
   Reasons: mood match (+2.0); energy similarity (+2.88)

3. Gym Hero — Max Pulse
   Score:  4.61
   Reasons: genre match (+2.0); energy similarity (+2.61)

4. Neon Skyline — City Static
   Score:  2.88
   Reasons: energy similarity (+2.88)

5. Night Drive Loop — Neon Echo
   Score:  2.85
   Reasons: energy similarity (+2.85)
```

The top result, **Sunrise City**, is a pop/happy song with energy 0.82 — it matches
all three preferences, so it scores highest, exactly as expected.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



