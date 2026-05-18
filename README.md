# Wuziqi-AI

A Wuziqi (Gomoku) game built with Python and Tkinter, featuring a PvP mode, a simple AI opponent, and an LLM-powered commentator that explains the AI's moves in natural language.

## Features

- **PvP Mode:** Two players take turns placing pieces on a 15×15 board. The first to connect five in a row, column, or diagonal wins.
- **PvE Mode:** Play against an AI that evaluates every empty position across four directions and picks the highest-scoring move — prioritizing winning, blocking threats, and extending its own lines.
- **AI Commentator:** An Ollama-hosted LLM acts as the AI player's voice, offering short commentary on each move it makes.

## Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally
- An Ollama model pulled (default: `qwen2.5:7b`)

### Installation

```bash
git clone https://github.com/BrianYuyuan/wuziqi-ai.git
cd wuziqi-ai
pip install requests
ollama pull qwen2.5:7b
```

### Running the Game

```bash
python wuziqi.py
```

Choose your side (White or Black) in the selection window, then click on the board to place pieces.

## Project Structure

| File | Description |
|------|-------------|
| `wuziqi.py` | Main entry point — contains the game logic (`WuziqiGame`) and GUI (`WuziqiGUI`) |
| `ai_player.py` | AI opponent — scores empty positions and selects the best move |
| `ai_commentator.py` | LLM commentator — converts the board to text, builds a prompt, and calls Ollama's API |

## Configuration

You can adjust the following constants in `wuziqi.py`:

| Constant | Default | Description |
|----------|---------|-------------|
| `SIZE` | 15 | Board dimensions (SIZE × SIZE) |
| `WIN_LENGTH` | 5 | Number of pieces in a row needed to win |

To use a different Ollama model, change the `model` parameter when the `Commentator` is initialized in the GUI class.
