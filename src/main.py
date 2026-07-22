"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Distinct user preference profiles to test the recommender against.
# Each maps a friendly name to a preference dictionary.
USER_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.3},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
}


# Adversarial / edge-case profiles designed to stress-test the scoring logic.
# Each is built to expose a specific weakness or surprising behavior.
ADVERSARIAL_PROFILES = {
    # CONTRADICTION: "sad" but max energy. The scorer treats mood and energy
    # independently, so it happily rewards an incoherent combination.
    "Sad but Cranked": {"genre": "pop", "mood": "sad", "energy": 1.0},

    # ENERGY DOMINATES: energy is worth up to +3.0, more than genre (+2) or
    # mood (+2). Wrong genre AND wrong mood but exact energy still scores +3.0.
    "Energy-Only Zealot": {"genre": "zzz-nonexistent", "mood": "zzz-none", "energy": 0.5},

    # CASE-SENSITIVITY TRAP: matching is exact string equality, so "Pop" != "pop".
    # Looks like High-Energy Pop but earns ZERO genre/mood points.
    "Right Genre, Wrong Case": {"genre": "Pop", "mood": "Happy", "energy": 0.8},

    # OUT-OF-RANGE ENERGY: energy is assumed 0..1. At 2.0 the similarity term
    # clamps to 0 for every song, silently killing the strongest signal.
    "Impossible Energy": {"genre": "rock", "mood": "intense", "energy": 2.0},

    # TRUTHINESS BUG: `get("target_energy") or get("energy")` returns None when
    # target_energy is 0.0, so the "calmest music" user loses energy scoring.
    "Wants Total Calm": {"genre": "lofi", "mood": "chill", "target_energy": 0.0},

    # EMPTY PROFILE: no keys at all. Every song ties at 0.0, so the top-5 is
    # just CSV order — a silent, meaningless ranking.
    "Ghost User": {},
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Run the recommender for one profile and print a readable ranked list."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    genre = user_prefs.get("genre", user_prefs.get("favorite_genre", "—"))
    mood = user_prefs.get("mood", user_prefs.get("favorite_mood", "—"))
    energy = user_prefs.get("energy", user_prefs.get("target_energy", "—"))

    print("\n" + "=" * 60)
    print(f"{name}: top {len(recommendations)} for "
          f"{genre} / {mood} (energy {energy})")
    print("=" * 60 + "\n")

    for rank, rec in enumerate(recommendations, start=1):
        # Each returned item is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{rank}. {song['title']} — {song['artist']}")
        print(f"   Score:  {score:.2f}")
        print(f"   Reasons: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in USER_PROFILES.items():
        print_recommendations(name, user_prefs, songs)

    print("\n\n" + "#" * 60)
    print("# ADVERSARIAL / EDGE-CASE PROFILES")
    print("#" * 60)

    for name, user_prefs in ADVERSARIAL_PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
