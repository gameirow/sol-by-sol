# Making choices matter — game balance plan (15 Nov 2026)

João played a full mission and said it "doesn't at all seem impactful". This plan says why, and what to change.
Numbers come from a simulator (`tools/balance_sim.py`) that plays 2,000 missions per player type with the same rules as the game.

## 1. What is wrong now

| Player type | Survives | 3 stars |
|---|---|---|
| Sensible kid (does the obvious thing) | 100 % | 89 % |
| Never goes outside | 100 % | 0 % |
| Careless (stays out long, ignores the alarm) | 38 % | – |
| Random buttons | 27 % | – |
| Same two things every sol | 0 % | – |

- A sensible kid **never comes close** to losing. Health stays above 5.5 nearly the whole mission.
- Staying inside all game is **perfectly safe**. The only cost is the crystal star.
- The power is so generous that the POWER screen is almost never a real choice.
- Every factor works alone. Low mood, a weak body or being sick change nothing except their own number.

So the decisions don't *feel* like they matter, because they mostly don't.

## 2. Phase 1 — tighter numbers + knock-on effects (prototype built on branch `game-balance`)

### Tighter numbers
| Rule | Now | New |
|---|---|---|
| Sunlight power (very high / high / medium / low) | 11 / 10 / 9 / 7 | 10 / 9 / 8 / 6 |
| Dust on panels per sol (normal / dust storm) | 6 % / 20 % | 8 % / 25 % |
| Exercise lost per sol without the treadmill | 1.5 | 1.3 |
| Mood lost per sol | 1.5 | 1.8 |
| Sleep & food lost per sol without rest | 0.8 | 1.2 |
| Crystals | all near the base | 1st near; 2nd and 3rd farther away (a longer walk = more radiation) |

### Knock-on effects (one bad thing leads to another)
| When… | …then | Sojourner says (short) |
|---|---|---|
| Mood is below 4 | only **1 activity** today | "The crew feels too sad to do much. Just one thing today." |
| Exercise is below 4 | you **walk slower** outside (more time = more radiation) | "Weak legs! Walking outside is slow today." |
| Sleep & food is below 4 | **sick**: the treadmill is closed | "The crew feels sick. No treadmill until they rest." |
| Air & heat gets less power than it needs | the cold farm grows **1 less food** | "Too cold for the plants! The farm grew less food." |

Real-world basis (for the "Real or game?" screen): sad or tired crews really get less done (NASA studies isolation
in HERA and Mars-500); weak muscles really slow astronauts down after spaceflight (OSD-342); plants really grow
badly in the cold. The exact numbers stay game rules.

### What the simulator says with Phase 1
| Player type | Survives | 3 stars | Health dipped below 5.5 |
|---|---|---|---|
| Sensible kid | 82 % | 40 % | 27 % |
| Never goes outside | 50 % (runs out of air & heat: dusty panels!) | 0 % | – |
| Careless | 27 % | 12 % | – |
| Random buttons | 5 % | – | – |
| Same two things every sol | 0 % | – | – |

- A good player still usually wins, but has to **think every sol**, and 3 stars is an achievement, not a given.
- Hiding inside is no longer safe: someone **has** to go out and clean the panels. That is the real Mars trade-off.
- Bad play snowballs, so the kid feels the cause and effect.

Is 82 % too hard for a 7-year-old? Possibly. That is what Phase 2's **Cadet** level is for.

## 3. Phase 2 — ideas for later (needs Thea's OK, she owns the game design)

1. **Two levels.** *Cadet* = today's easy rules (for 7–9). *Commander* = Phase 1 rules (for 10–12). One tap on the title.
2. **A surprise every sol** (a small card with two choices, based on real Mars events):
   a dust devil cleans the panels for free; the water recycler clogs (fix it = 1 activity, or lose sleep & food);
   seeds sprout early (more power to the farm = extra food); a radio message from home (call now or lose mood).
3. **"What your choices did"** lines in the sol report and on the end screen
   ("You skipped the treadmill 3 times, so walking got slow on sol 7").
4. **A radiation star:** finish with less than half the radiation budget used.
5. **Show it, don't just number it:** the astronaut walks slower, the greenhouse looks wilted, Sojourner looks worried.

## 4. How to test
- `python tools/balance_sim.py` prints the table above for the current rules.
- Play on the branch: `python build.py`, serve `dist/`, open the game. Debug: `__S()` shows the state.
- Most important: one real kid plays 10 sols on each level. Watch where they get stuck, not just whether they win.
