# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

It matches songs to your vibe using genre, mood, and energy.

---

## 2. Intended Use  

**Goal / Task.** VibeMatch tries to guess which songs a person will like. You tell it
your favorite genre, mood, and energy level. It then ranks the songs in the catalog and
suggests the top 5. It also gives a short reason for each pick.

**What it assumes about the user.** It assumes you can name one favorite genre, one mood,
and one energy level. It assumes your taste stays the same for the whole session.

**Intended use.** This is a classroom project. It is made for learning how recommenders
turn data into suggestions. It is good for testing ideas and running experiments.

**Non-intended use.** It is not for real users or real apps. Do not use it to make real
choices for real listeners. The song list is tiny and made up. It should not be used where
fair or safe recommendations actually matter.

---

## 3. How the Model Works  

The model gives each song points. More points means a better match.

Here are the rules:

- Same genre as you want: **+2 points**.
- Same mood as you want: **+2 points**.
- Energy close to what you want: **up to +3 points**. The closer, the more points.
- Acoustic song, if you like acoustic: **+1 point**.

Then it adds up the points for every song. It sorts the songs from most points to least.
It shows you the top 5. For each one, it lists the reasons it earned points.

Energy is the strongest rule. It can give more points than genre or mood. It also gives
partial points, so every song gets a little energy credit. Genre and mood are all-or-nothing.

---

## 4. Data  

The catalog has **18 songs**. It is a small, made-up dataset.

Each song has these features:

- Title and artist
- Genre and mood
- Energy, tempo, valence, danceability, and acousticness (all numbers)

There are 12 different genres. Most genres have only **one** song. A few have two or three
(like lofi, pop, and hip hop). There are 13 different moods, and many appear just once.

I did not add or remove any songs. I used the starter dataset as is.

Some parts of music taste are missing. There are no lyrics and no languages. There are no
real listening habits, like skips or replays. The catalog is too small to cover real taste.

---

## 5. Strengths  

The system works well for clear, simple tastes.

- It tells apart very different listeners. A party fan and a study fan get almost no
  overlap in their lists. That felt right.
- When a song matches all three things (genre, mood, and energy), it goes to the top.
  For example, Sunrise City is the clear #1 for the Happy Pop fan. That matched my guess.
- It gives a short reason for every pick. So you can see *why* a song was chosen.
- It is fast and easy to run. This makes it great for testing ideas in class.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

**Weakness discovered: the "energy gap" creates a filter bubble that overrides genre.**
During my experiments I found that the energy factor is the single most powerful part of the score — it is worth up to +3.0, more than a genre match (+2.0) or a mood match (+2.0), and unlike those two it gives *partial* credit to every song instead of being all-or-nothing. Because of this, energy proximity quietly dominates the ranking: my "Energy-Only Zealot" and "Right Genre, Wrong Case" test profiles were served songs of completely wrong genres simply because the energy lined up, meaning the system can ignore what a user actually asked for. This bias is made worse by the catalog itself, whose 18 songs cluster at the energy extremes (a loud group around 0.75–0.93 and a calm group around 0.24–0.45) with almost nothing in the middle. As a result, users who like high-energy or low-energy music get strong, satisfying matches, while a user with moderate energy taste (around 0.5) has no true match and receives weaker recommendations across the board — an entire type of listener is effectively underserved. In short, the scoring unintentionally favors listeners at the energy extremes and can trap any user in an "energy bubble" that talks over their stated genre and mood.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

### Profiles I tested

I tested nine user profiles. Three were realistic everyday listeners — **High-Energy Pop**
(pop / happy / energy 0.8), **Chill Lofi** (lofi / chill / energy 0.3), and **Deep Intense
Rock** (rock / intense / energy 0.9). The other six were deliberately tricky "adversarial"
profiles built to try to break the scoring, such as a contradictory "sad but maximum energy"
listener and an empty profile with no preferences at all (see the full outputs in the README).

### What surprised me

The biggest surprise was how often a song showed up on a list even though it didn't really
match the *feeling* the user asked for. The clearest example: **Gym Hero keeps appearing for
the Happy Pop listener** (it ranked #3), even though Gym Hero is an "intense" workout song, not
a "happy" one. I expected the mood to matter more than it does.

### Comparing the profiles (why the differences make sense)

- **High-Energy Pop vs. Chill Lofi** — These two are almost mirror images, and the results
  reflect that. High-Energy Pop's list is full of loud, upbeat songs (Sunrise City, Rooftop
  Lights, Gym Hero), while Chill Lofi's list is full of quiet, mellow ones (Library Rain,
  Midnight Coding, Focus Flow). This makes sense: the one thing that changed most was the
  energy number (0.8 vs 0.3), and energy is the strongest ingredient in the score, so the two
  lists barely overlap. Good sign — the system clearly separates "party" listeners from
  "study" listeners.

- **High-Energy Pop vs. Deep Intense Rock** — Both want loud music (energy 0.8 vs 0.9), and you
  can see that overlap: **Gym Hero appears on both lists**. But the top pick is different —
  Sunrise City (a happy pop song) wins for the pop fan, and Storm Runner (an intense rock song)
  wins for the rock fan. This makes sense because genre and mood act like tie-breakers once the
  energy is similar. The shared high energy is why Gym Hero fits both, but each person's own
  genre/mood pushes their "perfect" song to the very top.

- **Chill Lofi vs. Deep Intense Rock** — These are the two most opposite profiles, and their
  lists share **zero songs**. The rock fan gets fast, aggressive tracks; the lofi fan gets slow,
  calm ones. This is exactly what should happen — nobody who wants energy 0.9 should ever see
  the same songs as someone who wants energy 0.3.

### Explaining "Gym Hero" in plain language

Imagine you tell the app: "I want happy pop music, played at a lively-but-not-crazy level."
The app checks every song against three boxes: is it pop? is it happy? is the energy about
right? Gym Hero is a pop song (box 1 ✓) and it's very high energy, which is close enough to
"lively" to earn most of those points (box 3 mostly ✓). It fails only the "happy" box, because
it's actually an intense, sweaty workout song. But the app doesn't *feel* the difference
between "happy" and "intense" — it just counts how many boxes are checked and adds up the
points. Two-and-a-bit checks out of three is still a high score, so Gym Hero muscles its way
onto the Happy Pop list even though a real person would say, "that's not a happy song, that's
a gym song." The lesson: the system understands *labels and numbers*, not the actual *mood* a
listener is going for.

---

## 8. Future Work  

Here are three things I would change next:

1. **Balance the points.** Right now energy is too strong. I would lower its weight so
   genre and mood matter more. This would stop workout songs from sneaking onto happy lists.

2. **Fix the small bugs.** Matching is case-sensitive, so "Pop" does not match "pop". Also,
   an energy of 0.0 gets skipped by accident. I would fix both so the app is more forgiving.

3. **Add variety to the top 5.** The list can feel same-y. I would make sure the top picks
   are not all the same genre or energy, so the user sees more choices.

---

## 9. Personal Reflection  

I learned that a recommender is really just a points system. It does not understand music.
It just counts matches and adds numbers.

The surprising part was how one rule can take over. Energy was so strong that it changed
the whole list. Small choices about points had big effects on the results.

Now I think about real music apps differently. When a song shows up on my playlist, I know
it is not magic. Some rule gave it points. And those rules can be biased or just plain odd,
even when the app looks smart.
