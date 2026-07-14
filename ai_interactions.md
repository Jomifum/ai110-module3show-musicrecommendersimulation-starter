# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

What task did you give the agent?
I used an AI coding agent to help me build a content-based music recommender simulation from a starter repository. Instead of handing the agent the entire project at once, I guided it phase by phase. I had it help me implement the data classes, the CSV loader, and the scoring and ranking functions. Once the core logic was built, I used the agent to expand the dataset, run multi-profile evaluations, and draft the initial documentation.

Prompts used:
Here are the key prompts I used that required multi-step reasoning:

"Refactor the scoring formula to use a point-based system: give +2.0 points for an exact genre match, +1.0 point for an exact mood match, and add the energy similarity score (up to +1.0). Also, include a 'reasons list' in the output explaining exactly where a song's points came from."

"Expand our songs.csv dataset by generating 8 new songs. Make sure to include a diverse mix of genres like metal, indie pop, ambient, and classical, ensuring all columns match the existing formatting."

"Update main.py to include two new adversarial UserProfiles to test for biases: one that has conflicting energy and mood (e.g., high energy but a 'sad' mood), and another that has no preferred genre but wants high energy."

"Run an experiment where we halve the genre weight and double the energy weight to see if it breaks our filter bubble. Output the new top-5 recommendations, but make sure to revert to the official scoring recipe after the test."

What did the agent generate or change?
The agent generated the core architecture of the project. It created the Song and UserProfile dataclasses, as well as the load_songs, score_song, and recommend_songs functions in recommender.py. It successfully refactored the scoring logic from normalized weights to my custom point system. It also updated main.py with the CLI output and instantiated all five user profiles (three standard, two adversarial). Additionally, it drafted the model_card.md and README.md sections, updated the test suite, and appended the 8 new rows to songs.csv.

What did you verify or fix manually?
I made sure to stay in control of the project and manually verified several elements rather than trusting the AI blindly:

Hallucinated files: When the agent generated 8 new songs, I noticed it didn't actually save them to songs.csv (my local load check still returned only 10 songs). I caught the hallucination and forced it to properly append and save the rows.

Un-reverted experiments: After running the "halve genre / double energy" experiment, the agent left the experimental weights in the codebase. I caught this and reverted the code to the official recipe myself so my Model Card wouldn't contradict the actual code.

Syntax errors: I had to manually fix a Python bug in an early inspection command where the AI wrote from import Path instead of the correct from pathlib import Path.

Math verification: I independently verified the math to ensure the tempo feature was properly normalized in the scoring logic so that high BPM values (60–152) wouldn't break the 0–1 scale and overwhelm the energy score.

Double-checking outputs: Finally, I re-ran pytest and the CSV load checks locally on my own machine to ensure the code worked, rather than just taking the agent's summary at its word.
