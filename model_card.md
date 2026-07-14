# 🎧 Model Card: VibeFinder 1.0

## Model Name

VibeFinder 1.0

---

## Goal / Task

VibeFinder recommends songs from a small catalog based on a user's stated tastes. It ranks songs that match the user's genre, mood, energy level, and tempo preference. The output is a short, ordered list for listening or exploration.

---

## Data Used

The catalog is a small collection of about 18 songs. The dataset contains song attributes such as genre, mood, energy (0–1), tempo (BPM), valence, danceability, and acousticness. Some genres appear several times (for example `lofi`), and several genres appear only once. The dataset was assembled for classroom exploration and is not a large real-world catalog.

---

## Algorithm Summary (plain English)

The recommender looks at four features for each song: genre, mood, energy, and tempo. It gives points for exact genre matches and for exact mood matches. It also gives points when a song's energy is similar to the user's preferred energy. The current point recipe is: genre = +2.0, mood = +1.0, and energy-similarity contributes additional points (higher when energy is close). Tempo is recorded and may be used to break ties or refine rankings but contributes less than genre or energy.

The points are added together to make a final score for each song. Songs are sorted by score, and the top entries are returned as recommendations.

---

## Observed Behavior and Biases

- The system requires exact genre strings to award the genre points. This means `indie pop` will not match `pop`. Similar or nearby genres can be excluded from recommendations because of that exact-match rule.
- Energy similarity is powerful. When energy is close to the user's preferred energy, a song can gain as many or more points than a genre match. This makes the model favor songs with matching intensity even if the genre differs.
- Some useful song attributes (valence, danceability, acousticness) are present but not used. Users who care about those attributes get no benefit from stating them.
- The catalog is small and uneven. Popular genres in the data (e.g., `lofi`) have more items to choose from. Users who prefer rare genres get fewer good options and may see repetitive or cross-genre suggestions.
- Mood matching is exact-string based. Users who use different words for similar feelings (for example `moody` vs `sad`) may miss good matches.
- Ties are broken by song title alphabetically. This non-musical rule systematically favors some tracks when scores tie.

# Limitations 

In testing the system, the biggest bias I found was how heavily the exact-match genre rule dominates the recommendations, creating a rigid 'filter bubble.' For example, when I created a conflicting profile looking for a 'Sad' mood but with high energy, the system completely ignored the sad mood and pushed high-energy pop tracks like Gym Hero and Sunrise City just because the genre matched. Furthermore, when I tested a profile with no genre preference at all, entirely new tracks like Metal Sunrise and Storm Runner finally appeared in the top 5. This proved that my strict genre scoring was hiding diverse, cross-genre songs from users simply because they lacked the exact categorical label.
---

## Evaluation Process

Pop vs. Lofi: The pop profile favored bright, high-energy tracks like Sunrise City, while the lofi profile shifted to calm, low-energy songs like Library Rain because the target energy level flipped completely.

Pop vs. Rock: While both profiles look for higher energy, the exact-match genre filter successfully separated the heavily produced pop tracks from the guitar-heavy rock tracks.

Lofi vs. Rock: These two yielded completely different sets; the system correctly polarized the low-energy/chill mood of Lofi against the high-energy/intense mood of Rock.

What Surprised Me: I was most surprised by the adversarial test results. I expected a high-energy, "Sad" profile to find an angsty, intense rock or metal song. Instead, because the genre and energy weights completely overpowered the mood score, the system recommended an upbeat track like Gym Hero. It showed me how easily a mathematical formula can misunderstand human emotion.

---

## Intended vs Non-Intended Use

Intended use: classroom exploration and small-scale demos of a content-based recommender. It is useful for showing how simple features affect ranking and for prototyping scoring rules.

Not intended: production personalization, handling large catalogs, or serving precise commercial recommendations. The model is not robust to noisy labels or to diverse user vocabularies.

---

## Ideas for Improvement

- Normalize or canonicalize genre labels so related genres match (for example treat `indie pop` as a type of `pop`).
- Use fuzzy or synonym matching for mood and genre to reduce missed matches.
- Make the weight table authoritative and apply it consistently so tuning is easier.
- Use additional attributes (valence, danceability, tempo) when the user states a preference for them.
- Add a diversity penalty to avoid repeating the same artist or genre at the top of the list.
- Replace alphabetical tie-breaks with a musical signal such as higher danceability or a popularity proxy.
- Add an optional small evaluation harness that compares original scoring to a normalized-genre variant to measure how many top-k positions change.

---

If you want, I can apply a simple genre canonicalization and show an A/B comparison of how many top-5 recommendations change. Would you like that?

---

## Test Profiles — Top-5 Outputs

Below are the exact top-5 outputs from `src/main.py` for the three test profiles used in the project. Each block is the verbatim terminal output for that profile.

**High-Energy Pop**

```
Top 5 recommendations for: High-Energy Pop

Rank | Title | Artist | Score | Reasons
1 | Sunrise City | Neon Echo | 3.97 | genre match (+2.00), mood match (+1.0), energy similarity (+0.97)
2 | Gym Hero | Max Pulse | 2.92 | genre match (+2.00), energy similarity (+0.92)
3 | Rooftop Lights | Indigo Parade | 1.91 | mood match (+1.0), energy similarity (+0.91)
4 | Beach Fiesta | Sol Caribe | 0.97 | energy similarity (+0.97)
5 | Steel Heart | Neon Reign | 0.95 | energy similarity (+0.95)
```

**Chill Lofi**

```
Top 5 recommendations for: Chill Lofi

Rank | Title | Artist | Score | Reasons
1 | Library Rain | Paper Lanterns | 4.00 | genre match (+2.00), mood match (+1.0), energy similarity (+1.00)
2 | Midnight Coding | LoRoom | 3.93 | genre match (+2.00), mood match (+1.0), energy similarity (+0.93)
3 | Focus Flow | LoRoom | 2.95 | genre match (+2.00), energy similarity (+0.95)
4 | Spacewalk Thoughts | Orbit Bloom | 1.93 | mood match (+1.0), energy similarity (+0.93)
5 | Coffee Shop Stories | Slow Stereo | 0.98 | energy similarity (+0.98)
```

**Deep Intense Rock**

```
Top 5 recommendations for: Deep Intense Rock

Rank | Title | Artist | Score | Reasons
1 | Storm Runner | Voltline | 3.99 | genre match (+2.00), mood match (+1.0), energy similarity (+0.99)
2 | Gym Hero | Max Pulse | 1.97 | mood match (+1.0), energy similarity (+0.97)
3 | Metal Sunrise | Iron Pulse | 1.96 | mood match (+1.0), energy similarity (+0.96)
4 | Steel Heart | Neon Reign | 1.00 | energy similarity (+1.00)
5 | Beach Fiesta | Sol Caribe | 0.98 | energy similarity (+0.98)
```

**Adversarial: Conflicting energy vs mood**

```
Top 5 recommendations for: Adv: Conflicting energy vs mood

Rank | Title | Artist | Score | Reasons
1 | Gym Hero | Max Pulse | 2.98 | genre match (+2.00), energy similarity (+0.98)
2 | Sunrise City | Neon Echo | 2.87 | genre match (+2.00), energy similarity (+0.87)
3 | Metal Sunrise | Iron Pulse | 0.99 | energy similarity (+0.99)
4 | Storm Runner | Voltline | 0.96 | energy similarity (+0.96)
5 | Steel Heart | Neon Reign | 0.95 | energy similarity (+0.95)
```

**Adversarial: Missing genre high-energy**

```
Top 5 recommendations for: Adv: Missing genre high-energy

Rank | Title | Artist | Score | Reasons
1 | Metal Sunrise | Iron Pulse | 1.99 | mood match (+1.0), energy similarity (+0.99)
2 | Gym Hero | Max Pulse | 1.98 | mood match (+1.0), energy similarity (+0.98)
3 | Storm Runner | Voltline | 1.96 | mood match (+1.0), energy similarity (+0.96)
4 | Steel Heart | Neon Reign | 0.95 | energy similarity (+0.95)
5 | Beach Fiesta | Sol Caribe | 0.93 | energy similarity (+0.93)
```
---

## Reflection

Building this simulation taught me that recommendation systems aren't magic; they are essentially just mathematical scoring rules. Recommenders turn data into predictions by breaking down subjective 'vibes'—like mood or energy—into numerical features and categorical labels. By comparing a user's target numbers against a catalog of songs using simple formulas (like calculating the absolute difference between values), the system can instantly rank and sort tracks. It showed me how a few basic add-and-subtract rules can create an output that genuinely feels like a curated, personalized playlist.

However, I also learned exactly how easily bias and unfairness can be programmed into these systems. In my experiments, the system's exact-match rule for genre was so rigid that it completely overpowered the user's mood and energy preferences. This creates a severe 'filter bubble.' For instance, a user looking for a sad, low-energy track might get bombarded with upbeat pop songs simply because the algorithm prioritizes the 'Pop' label above all else. This kind of algorithmic bias unfairly hides diverse, cross-genre artists from users and proves that if a system's weights are unbalanced, it will completely misunderstand human nuance.

---