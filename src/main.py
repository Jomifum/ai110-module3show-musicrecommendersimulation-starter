"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, UserProfile


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Define three distinct user profiles
    profiles = {
        "High-Energy Pop": UserProfile(
            preferred_genre="pop",
            preferred_mood="happy",
            preferred_energy=0.85,
            preferred_tempo=125,
        ),
        "Chill Lofi": UserProfile(
            preferred_genre="lofi",
            preferred_mood="chill",
            preferred_energy=0.35,
            preferred_tempo=75,
        ),
        "Deep Intense Rock": UserProfile(
            preferred_genre="rock",
            preferred_mood="intense",
            preferred_energy=0.9,
            preferred_tempo=140,
        ),
    }

    for name, user in profiles.items():
        user_prefs = {
            "preferred_genre": user.preferred_genre,
            "preferred_mood": user.preferred_mood,
            "preferred_energy": user.preferred_energy,
            "preferred_tempo": user.preferred_tempo,
        }
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\nTop 5 recommendations for: {name}\n")
        print("Rank | Title | Artist | Score | Reasons")
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            reasons_str = ", ".join(reasons) if reasons else "(no reasons)"
            print(f"{rank} | {song.title} | {song.artist} | {score:.2f} | {reasons_str}")

    # Adversarial edge-case profiles (examples, not used above):
    # 1) Conflicting energy vs mood: very high energy but 'sad' mood — tests conflicting signals
    adversarial_1 = {"preferred_genre": "pop", "preferred_mood": "sad", "preferred_energy": 0.95, "preferred_tempo": 130}
    # 2) Genre absent but extreme energy: empty genre, high energy — tests reliance on numeric features
    adversarial_2 = {"preferred_genre": "", "preferred_mood": "intense", "preferred_energy": 0.95, "preferred_tempo": 140}

    print("\nAdversarial profiles (examples):")
    print("- Conflicting energy vs mood (tests mixed signals):", adversarial_1)
    print("- Missing genre but extreme energy (tests numeric fallback):", adversarial_2)

    # Build adversarial UserProfile objects and print their top-5 recommendations
    adversarial_profiles = {
        "Adv: Conflicting energy vs mood": UserProfile(
            preferred_genre="pop",
            preferred_mood="sad",
            preferred_energy=0.95,
            preferred_tempo=130,
        ),
        "Adv: Missing genre high-energy": UserProfile(
            preferred_genre="",
            preferred_mood="intense",
            preferred_energy=0.95,
            preferred_tempo=140,
        ),
    }

    for name, user in adversarial_profiles.items():
        user_prefs = {
            "preferred_genre": user.preferred_genre,
            "preferred_mood": user.preferred_mood,
            "preferred_energy": user.preferred_energy,
            "preferred_tempo": user.preferred_tempo,
        }
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\nTop 5 recommendations for: {name}\n")
        print("Rank | Title | Artist | Score | Reasons")
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            reasons_str = ", ".join(reasons) if reasons else "(no reasons)"
            print(f"{rank} | {song.title} | {song.artist} | {score:.2f} | {reasons_str}")


if __name__ == "__main__":
    main()
