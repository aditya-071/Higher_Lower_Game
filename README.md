# Higher-Lower: Followers Showdown

A sleek, interactive Python game where players test their knowledge of social media influence. Compare two famous accounts and guess who has the higher follower count!

## 🚀 Features

- **Dual Mode Gameplay:** Play directly in your terminal or launch a modern **Tkinter GUI**.
- **Responsive Logic:** The winner of the previous round stays for the next challenge, increasing the difficulty.
- **Interactive GUI:** - Visual cards for contestants.
  - Real-time score tracking.
  - **Keyboard Shortcuts:** Press `A` or `B` on your keyboard to make a selection quickly.
- **Clean Architecture:** Modular code structure for easy maintenance and scalability.

## 📸 Preview
![Higher Lower Game Interface](screenshot.png)

## 🛠️ Project Structure

- `main.py`: The entry point. Handles console logic and mode switching.
- `gui.py`: Contains the `HigherLowerApp` class and all Tkinter UI code.
- `game_data.py`: A dictionary-based database of celebrities, descriptions, and follower counts.
- `art.py`: ASCII art and branding for the console interface.

## 📥 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/higher-lower-game.git](https://github.com/YOUR_USERNAME/higher-lower-game.git)
   cd higher-lower-game
