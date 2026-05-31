---
noteId: "7a40f570530711f18f207d68b1aaec40"
tags: []

---

# Wuziqi-AI

A Wuziqi (Gomoku) game built with Python and Tkinter, featuring a PvP mode, a simple AI opponent, and an LLM-powered commentator that explains the AI's moves in natural language.
 
> This branch uses **Groq's online API** for the commentator. For the local Ollama version, see the [`main`](../../tree/main) branch.
 
## Features
 
- **PvP Mode:** Two players take turns placing pieces on a 15×15 board. The first to connect five in a row, column, or diagonal wins.
- **PvE Mode:** Play against an AI that evaluates every empty position across four directions and picks the highest-scoring move — prioritizing winning, blocking threats, and extending its own lines.
- **AI Commentator:** A Groq-hosted LLM acts as the AI player's voice, offering short commentary on each move it makes.
## Getting Started
 
### Prerequisites
 
- Python 3.10+
- A free [Groq](https://console.groq.com) account and API key
### Installation
 
```bash
git clone -b online-api https://github.com/BrianYuyuan/wuziqi-ai.git
cd wuziqi-ai
pip install -r requirements.txt
```
 
### Set Your API Key
 
Sign up at [console.groq.com](https://console.groq.com), create an API key, then set it as an environment variable.
 
**On Windows (PowerShell):**
 
```powershell
$env:GROQ_API_KEY = "your_key_here"
```
 
**On macOS / Linux:**
 
```bash
export GROQ_API_KEY="your_key_here"
```
 
Note: this setting only persists for the current terminal session. Run the game from the same terminal where you set the variable.
 
### Running the Game
 
```bash
python wuziqi.py
```
 
Choose a mode (PvP or PvE) in the selection window. In PvE, pick your side (White or Black), then click on the board to place pieces.
 
## Project Structure
 
| File | Description |
|------|-------------|
| `wuziqi.py` | Main entry point — contains the game logic (`TicTacToeGame`) and GUI (`TicTacToeGUI`) |
| `ai_player.py` | AI opponent — scores empty positions and selects the best move |
| `ai_commentator.py` | LLM commentator — converts the board to text, builds a prompt, and calls Groq's API |
 
## Configuration
 
You can adjust the following constants in `wuziqi.py`:
 
| Constant | Default | Description |
|----------|---------|-------------|
| `SIZE` | 15 | Board dimensions (SIZE × SIZE) |
| `WIN_LENGTH` | 5 | Number of pieces in a row needed to win |
| `MODEL_NAME` | `llama-3.3-70b-versatile` | Groq model to use for commentary |
 
To use a different model, see the [Groq model list](https://console.groq.com/docs/models) and update `MODEL_NAME`.
