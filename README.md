# Mancala AI — Python Minimax with Alpha-Beta Pruning

This is a simple **Mancala** game implemented in Python.  
Play against an AI opponent that uses **Minimax search** with **Alpha-Beta pruning** for efficient decision making.

---

## 🎮 Features

- Play interactively against the AI (you are **Player 1**).
- Or let the AI play both sides for demonstration (`self` mode).
- Configurable search depth for difficulty:  
  - **Easy**: Depth 1–3  
  - **Intermediate**: Depth 4–6  
  - **Hard**: Depth 7–9  
  - **Pro**: Depth 10–12

- Clear ASCII board shows:
  - Pit indices for **Player 1** and **Player 2**.
  - Endzone (Mancala) scores.
  - Seeds in each pit.

- Full support for:
  - **Extra turn** when your last seed lands in your own endzone.
  - **Capture** when your last seed lands in an empty pit on your side.

---

## ⚙️ How to Run

1. **Save the script** (e.g., `mancala.py`).

2. Run it with:
```bash
python mancala.py
```
Choose a mode:
- play → Play against the AI
- self → Watch AI play against itself
Choose AI depth:
Example: 3 for easy, 8 for strong AI
For your move, pick a pit number (1–6).

## 📜 Gameplay Rules (implemented)

Pits: Each player has 6 pits with seeds.
Endzones: Each player has an endzone (Mancala) to collect captured seeds.
Move: Pick all seeds from one of your pits and sow them counter-clockwise.
Endzone rule: If your last seed lands in your endzone, you play again.
Capture rule: If your last seed lands in an empty pit on your side, you capture the opposite pit's seeds.
Game over: When one side's pits are empty, the other player keeps remaining seeds.

## 🧠 AI Logic

The AI uses:

Minimax search for optimal decision making.
Alpha-Beta pruning to reduce search time.
A simple evaluation:
Current score difference.
Bonus for extra turn.
📌 Example Board

      [6] [5] [4] [3] [2] [1]   <- Pit indices for Player 2
 P2  [4] [4] [4] [4] [4] [4]
[EZ2:0]                     [EZ1:0]
 P1  [4] [4] [4] [4] [4] [4]
      [1] [2] [3] [4] [5] [6]   <- Pit indices for Player 1
      
## ✅ Requirements

Python 3.x
No external packages — only built-in libraries (copy).

## 👑 Author

Ryan Miller


