from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import os

# Score weights can be tuned later.
WEIGHTS = {
    "genre": 0.35,
    "mood": 0.20,
    "energy": 0.25,
    "tempo": 0.20,
}

TEMPO_MIN = 60
TEMPO_MAX = 152
TEMPO_RANGE = TEMPO_MAX - TEMPO_MIN

@dataclass
class Song:
    """
    Represents a song and its content-based attributes.
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: int

@dataclass
class UserProfile:
    """
    Represents a user's taste profile for recommendation matching.
    """
    preferred_genre: str
    preferred_mood: str
    preferred_energy: float
    preferred_tempo: int

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Song]:
    """Load songs from CSV and return a list of Song objects."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Song file not found: {csv_path}")

    songs: List[Song] = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not row or not row.get('id'):
                continue
            try:
                song = Song(
                    id=int(row['id']),
                    title=row['title'],
                    artist=row['artist'],
                    genre=row['genre'],
                    mood=row['mood'],
                    energy=float(row['energy']),
                    tempo_bpm=int(row['tempo_bpm']),
                )
            except KeyError as exc:
                raise ValueError(f"Missing expected column in CSV: {exc}") from exc
            except ValueError as exc:
                raise ValueError(f"Invalid value in CSV row {row}: {exc}") from exc
            songs.append(song)
    return songs


def score_song(user_prefs: Dict, song: Song) -> Tuple[float, List[str]]:
    """Compute point-based score and reasons for a song against user prefs."""
    reasons: List[str] = []
    total = 0.0

    # Genre exact match -> +2.0 (official recipe)
    target_genre = user_prefs.get("favorite_genre") or user_prefs.get("genre") or user_prefs.get("preferred_genre")
    if target_genre and song.genre.lower() == str(target_genre).lower():
        total += 2.0
        reasons.append("genre match (+2.00)")

    # Mood exact match -> +1.0
    target_mood = user_prefs.get("favorite_mood") or user_prefs.get("mood") or user_prefs.get("preferred_mood")
    if target_mood and song.mood.lower() == str(target_mood).lower():
        total += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity -> up to +1.0
    target_energy = None
    if "target_energy" in user_prefs:
        target_energy = user_prefs.get("target_energy")
    elif "energy" in user_prefs:
        target_energy = user_prefs.get("energy")
    elif "preferred_energy" in user_prefs:
        target_energy = user_prefs.get("preferred_energy")

    if target_energy is not None:
        try:
            target_energy = float(target_energy)
            # Energy similarity contributes up to +1.0 (closer energy -> more points)
            energy_points = max(0.0, 1.0 * (1.0 - abs(song.energy - target_energy)))
            total += energy_points
            reasons.append(f"energy similarity (+{energy_points:.2f})")
        except (TypeError, ValueError):
            # ignore invalid energy value
            pass

    return total, reasons


def recommend(songs: List[Song], user: UserProfile, top_n: int = 5) -> List[Tuple[Song, float]]:
    """
    Scores every song, sorts by descending score, breaks ties by title, and returns the top N.
    """
    scored_songs: List[Tuple[Song, float]] = []
    # Convert user profile into a dict compatible with score_song
    user_prefs = {
        "favorite_genre": user.preferred_genre,
        "favorite_mood": user.preferred_mood,
        "target_energy": user.preferred_energy,
        "target_tempo": user.preferred_tempo,
    }

    for song in songs:
        score, _reasons = score_song(user_prefs, song)
        scored_songs.append((song, score))

    # Sort by score descending, then title ascending for deterministic tie-breaking.
    scored_songs.sort(key=lambda item: (-item[1], item[0].title.lower()))
    return scored_songs[:top_n]


def recommend_songs(user_prefs: Dict, songs: List[Song], k: int = 5) -> List[Tuple[Song, float, List[str]]]:
    """Return the top-k songs scored with reasons for given user preferences."""
    scored: List[Tuple[Song, float, List[str]]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    # Sort in-place by score descending, then by title ascending for deterministic tie-breaking.
    scored.sort(key=lambda item: (-item[1], item[0].title.lower()))

    return scored[:k]
