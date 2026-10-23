# Template: Game

A visitor wants to know: what does it look like, how do I launch it, and how do I play?

## Skeleton

````markdown
# Game Name

One sentence: the genre and the hook.

![Gameplay](docs/gameplay.gif)

## What it does

A short paragraph on the concept and the goal of the game.

- Feature 1 (e.g. local 2-player mode)
- Feature 2
- Feature 3

## Installation

Requirements: Python 3.x, pygame (etc.)

```bash
git clone https://github.com/user/repo.git
cd repo
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

### Controls

| Key | Action |
|---|---|
| Arrow keys | Move |
| Space | Shoot |
| Esc | Pause |

### How to play

2–4 sentences or bullets: goal, win/lose conditions, any tips.

## Credits   <!-- assets, fonts, music, tutorials used -->
````

## Type-specific notes

- **Visuals matter most.** A GIF or screenshot near the top is the single best improvement for a game README. If none exists, leave a TODO and tell the user how to make one (macOS: Cmd+Shift+5 to record the screen).
- **Controls:** extract them from the key-handling code (`pygame.K_*`, `onKeyPress`, `Input.GetKey`, etc.). Don't guess.
- **Deployed browser games** (Phaser, three.js, plain JS canvas on GitHub Pages, itch.io, etc.): the play link is the main Usage. Put it right under the opening sentence. Local setup becomes a short secondary section, e.g. "Run it yourself", for people who want to read or change the code. Find the URL in the Pages workflow, the repo homepage, a CNAME file, or the existing README.
- **Touch and keyboard:** if the game supports both, use a table with one column per input method, not two separate lists.
- **Credits:** list third-party assets found in `assets/` with their sources or licenses if the repo records them. If you can't find a source, flag it to the user, since unlicensed assets matter when publishing.
