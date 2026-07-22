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

## Adversarial / Edge-Case Profiles

To stress-test the scoring logic, I added a set of `ADVERSARIAL_PROFILES` in
[src/main.py](src/main.py). Each is designed to see if the scorer can be "tricked"
or produce surprising results. Below is the **actual terminal output** for each,
followed by what it exposes.

### 1. Sad but Cranked — `{genre: pop, mood: sad, energy: 1.0}`

A contradictory profile: a "sad" mood paired with maximum energy.

```
============================================================
Sad but Cranked: top 5 for pop / sad (energy 1.0)
============================================================

1. Gym Hero — Max Pulse
   Score:  4.79
   Reasons: genre match (+2.0); energy similarity (+2.79)

2. Sunrise City — Neon Echo
   Score:  4.46
   Reasons: genre match (+2.0); energy similarity (+2.46)

3. Storm Runner — Voltline
   Score:  2.73
   Reasons: energy similarity (+2.73)

4. Midnight Parade — The Velvet Maps
   Score:  2.67
   Reasons: energy similarity (+2.67)

5. Rising Thunder — Kaia & Co
   Score:  2.64
   Reasons: energy similarity (+2.64)
```

**What it exposes:** The scorer has no concept of coherence. It recommends loud,
high-energy pop to a listener who asked for "sad" music, because mood and energy
are scored independently and added together. No song even matches the "sad" mood,
yet the system returns confident results with no warning that the request was odd.

### 2. Energy-Only Zealot — `{genre: zzz-nonexistent, mood: zzz-none, energy: 0.5}`

Deliberately impossible genre and mood, so only the energy factor can score.

```
============================================================
Energy-Only Zealot: top 5 for zzz-nonexistent / zzz-none (energy 0.5)
============================================================

1. Winter Glass — North Harbor
   Score:  2.85
   Reasons: energy similarity (+2.85)

2. Golden Hour Drive — Marigold Lane
   Score:  2.76
   Reasons: energy similarity (+2.76)

3. Midnight Coding — LoRoom
   Score:  2.76
   Reasons: energy similarity (+2.76)

4. Focus Flow — LoRoom
   Score:  2.70
   Reasons: energy similarity (+2.70)

5. Coffee Shop Stories — Slow Stereo
   Score:  2.61
   Reasons: energy similarity (+2.61)
```

**What it exposes:** Energy is weighted up to **+3.0** — more than genre (+2.0) or
mood (+2.0) alone. A song with the wrong genre *and* wrong mood can still score
+3.0 on energy and outrank a partial genre/mood match. The single energy dimension
can dominate the entire ranking.

### 3. Right Genre, Wrong Case — `{genre: Pop, mood: Happy, energy: 0.8}`

Identical intent to the default "High-Energy Pop" profile, but capitalized.

```
============================================================
Right Genre, Wrong Case: top 5 for Pop / Happy (energy 0.8)
============================================================

1. Sunrise City — Neon Echo
   Score:  2.94
   Reasons: energy similarity (+2.94)

2. Neon Skyline — City Static
   Score:  2.88
   Reasons: energy similarity (+2.88)

3. Rooftop Lights — Indigo Parade
   Score:  2.88
   Reasons: energy similarity (+2.88)

4. Night Drive Loop — Neon Echo
   Score:  2.85
   Reasons: energy similarity (+2.85)

5. Rising Thunder — Kaia & Co
   Score:  2.76
   Reasons: energy similarity (+2.76)
```

**What it exposes:** A real bug. Matching uses exact string equality
(`song["genre"] == "Pop"`), so `"Pop"` never matches the CSV's `"pop"`. Every song
loses its genre and mood points (compare to "High-Energy Pop" where Sunrise City
scored 6.94 — here it scores only 2.94). The fix is to lowercase both sides.

### 4. Impossible Energy — `{genre: rock, mood: intense, energy: 2.0}`

Energy is assumed to live in the 0–1 range; this profile sends it out of bounds.

```
============================================================
Impossible Energy: top 5 for rock / intense (energy 2.0)
============================================================

1. Storm Runner — Voltline
   Score:  4.00
   Reasons: genre match (+2.0); mood match (+2.0); energy similarity (+0.00)

2. Gym Hero — Max Pulse
   Score:  2.00
   Reasons: mood match (+2.0); energy similarity (+0.00)

3. Sunrise City — Neon Echo
   Score:  0.00
   Reasons: energy similarity (+0.00)

4. Midnight Coding — LoRoom
   Score:  0.00
   Reasons: energy similarity (+0.00)

5. Library Rain — Paper Lanterns
   Score:  0.00
   Reasons: energy similarity (+0.00)
```

**What it exposes:** With `energy = 2.0`, the similarity term `max(0, 1 - |e - 2.0|)`
clamps to **+0.00** for every song, silently disabling the strongest signal. There
is no input validation warning the user that the value is nonsensical.

### 5. Wants Total Calm — `{genre: lofi, mood: chill, target_energy: 0.0}`

A user who wants the calmest possible music, using `target_energy = 0.0`.

```
============================================================
Wants Total Calm: top 5 for lofi / chill (energy 0.0)
============================================================

1. Midnight Coding — LoRoom
   Score:  4.00
   Reasons: genre match (+2.0); mood match (+2.0)

2. Library Rain — Paper Lanterns
   Score:  4.00
   Reasons: genre match (+2.0); mood match (+2.0)

3. Spacewalk Thoughts — Orbit Bloom
   Score:  2.00
   Reasons: mood match (+2.0)

4. Focus Flow — LoRoom
   Score:  2.00
   Reasons: genre match (+2.0)

5. Sunrise City — Neon Echo
   Score:  0.00
   Reasons: no strong matches
```

**What it exposes:** A real bug. Notice the energy line is **completely missing**
from every reason. The code does `user_prefs.get("target_energy") or user_prefs.get("energy")`,
and since `0.0` is falsy, this evaluates to `None` and the energy dimension is
skipped entirely. The user asking for the calmest music gets no energy scoring at
all — the fix is to use an explicit `is None` check instead of `or`.

### 6. Ghost User — `{}`

An empty profile with no preferences at all.

```
============================================================
Ghost User: top 5 for — / — (energy —)
============================================================

1. Sunrise City — Neon Echo
   Score:  0.00
   Reasons: no strong matches

2. Midnight Coding — LoRoom
   Score:  0.00
   Reasons: no strong matches

3. Storm Runner — Voltline
   Score:  0.00
   Reasons: no strong matches

4. Library Rain — Paper Lanterns
   Score:  0.00
   Reasons: no strong matches

5. Gym Hero — Max Pulse
   Score:  0.00
   Reasons: no strong matches
```

**What it exposes:** Every song ties at 0.0, so the "top 5" is just the first five
rows of the CSV. The system still returns a confident-looking ranked list even
though it has no basis for ranking — a silent, meaningless result.

### Summary of Findings

| Profile | Type | Finding |
|---|---|---|
| Sad but Cranked | Design quirk | No coherence check; contradictory prefs both rewarded |
| Energy-Only Zealot | Design quirk | Energy (+3.0) can outweigh genre + mood combined |
| Right Genre, Wrong Case | **Bug** | Exact string match is case-sensitive (`"Pop"` ≠ `"pop"`) |
| Impossible Energy | Design quirk | Out-of-range energy silently clamps to +0.00 |
| Wants Total Calm | **Bug** | `target_energy = 0.0` disables energy scoring (falsy `or`) |
| Ghost User | Design quirk | Empty profile returns CSV order as a fake ranking |

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

### Reflection on my engineering process

**My biggest learning moment** was realizing that testing is where the real understanding
happens. Writing the scoring rules was quick. But building the "adversarial" profiles — like a
"sad but maximum energy" user and an empty profile — is what taught me how the system actually
behaves. Two of those tests uncovered real bugs I never would have guessed from reading the
code: the genre match was case-sensitive, so "Pop" did not match "pop", and an energy value of
0.0 was skipped by accident. Trying to break my own program taught me more than building it did.

**Using AI tools helped me** move faster and think of edge cases I would have missed. It
suggested profiles that stress-tested my logic and helped me spot the weak points in my scoring
rules. But I learned I could not just trust it. For example, one early idea was that my dataset
was probably dominated by pop music. When I actually checked the CSV, that was wrong — the
genres were spread out, and most genres had only one song. So I had to double-check every claim
against the real data and the real program output before writing it down. The AI was great for
ideas, but the facts had to come from running the code myself.

**What surprised me** was how a very simple algorithm can still "feel" like a real
recommendation. There is no learning and no intelligence here — it just counts matches and adds
up points. Yet the output looks confident and personal, complete with reasons like "genre match"
and "energy similarity." It reminded me that an app can look smart while doing something very
basic, and that the reasons it shows can hide how simple (or biased) the logic really is.

**If I extended this project**, I would first rebalance the points so energy does not
dominate genre and mood, and fix the two bugs I found. Next I would add variety to the top 5 so
the list is not all one genre or energy. After that, I would try adding more song features (like
tempo and valence) and a bigger, more balanced catalog, so the recommendations feel richer and
fairer for more kinds of listeners.



