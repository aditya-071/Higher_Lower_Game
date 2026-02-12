import random
import tkinter as tk
from tkinter import font
from game_data import data


class HigherLowerApp:
    def __init__(self, root):
        self.root = root
        root.title("Higher — Lower: Followers Showdown")
        root.configure(bg="#0f1724")
        root.geometry("760x420")
        root.resizable(False, False)

        self.score = 0
        self.current_a = None
        self.current_b = None

        self._build_ui()
        self._next_round()

    def _build_ui(self):
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        card_title = font.Font(family="Helvetica", size=12, weight="bold")
        body_font = font.Font(family="Helvetica", size=11)

        header = tk.Label(self.root, text="Higher — Lower", fg="#e6eef8", bg="#0f1724", font=title_font)
        header.pack(pady=(12, 6))

        score_frame = tk.Frame(self.root, bg="#0f1724")
        score_frame.pack()
        self.score_label = tk.Label(score_frame, text=f"Score: {self.score}", fg="#9be7ff", bg="#0f1724", font=body_font)
        self.score_label.pack()

        board = tk.Frame(self.root, bg="#0f1724")
        board.pack(pady=12, fill="x", expand=True)

        # Left card (A)
        self.card_a = tk.Frame(board, bg="#123", bd=0, relief="ridge", padx=12, pady=12)
        self.card_a.pack(side="left", padx=18, pady=8, expand=True, fill="both")
        self.a_name = tk.Label(self.card_a, text="", fg="#f8fafc", bg="#123", font=card_title)
        self.a_name.pack(anchor="w")
        self.a_desc = tk.Label(self.card_a, text="", fg="#cbd5e1", bg="#123", font=body_font, wraplength=300, justify="left")
        self.a_desc.pack(anchor="w", pady=(6, 0))
        self.a_country = tk.Label(self.card_a, text="", fg="#9fb7c9", bg="#123", font=body_font)
        self.a_country.pack(anchor="w", pady=(6, 0))

        vs = tk.Label(board, text="VS", fg="#ffd166", bg="#0f1724", font=card_title)
        vs.pack(side="left", padx=6)

        # Right card (B)
        self.card_b = tk.Frame(board, bg="#123", bd=0, relief="ridge", padx=12, pady=12)
        self.card_b.pack(side="left", padx=18, pady=8, expand=True, fill="both")
        self.b_name = tk.Label(self.card_b, text="", fg="#f8fafc", bg="#123", font=card_title)
        self.b_name.pack(anchor="w")
        self.b_desc = tk.Label(self.card_b, text="", fg="#cbd5e1", bg="#123", font=body_font, wraplength=300, justify="left")
        self.b_desc.pack(anchor="w", pady=(6, 0))
        self.b_country = tk.Label(self.card_b, text="", fg="#9fb7c9", bg="#123", font=body_font)
        self.b_country.pack(anchor="w", pady=(6, 0))

        # Controls
        controls = tk.Frame(self.root, bg="#0f1724")
        controls.pack(pady=(6, 12))

        self.result_label = tk.Label(controls, text="Make your pick:", fg="#e6eef8", bg="#0f1724", font=body_font)
        self.result_label.pack(pady=(0, 8))

        btn_frame = tk.Frame(controls, bg="#0f1724")
        btn_frame.pack()

        self.btn_a = tk.Button(btn_frame, text="A — Higher", bg="#00b894", fg="#072227", width=14, command=lambda: self._guess("A"))
        self.btn_a.grid(row=0, column=0, padx=8)
        self.btn_b = tk.Button(btn_frame, text="B — Higher", bg="#0984e3", fg="#071428", width=14, command=lambda: self._guess("B"))
        self.btn_b.grid(row=0, column=1, padx=8)

        self.restart_btn = tk.Button(controls, text="Restart", bg="#ff7675", fg="#111", command=self._restart)
        self.restart_btn.pack(pady=(8, 0))

        # Keyboard shortcuts
        self.root.bind("a", lambda e: self._guess("A"))
        self.root.bind("A", lambda e: self._guess("A"))
        self.root.bind("b", lambda e: self._guess("B"))
        self.root.bind("B", lambda e: self._guess("B"))

    def _choose_two(self):
        if len(data) < 2:
            raise ValueError("Need at least two entries in data")
        a = random.choice(data)
        b = random.choice(data)
        while b is a or b["name"] == a["name"]:
            b = random.choice(data)
        return a, b

    def _next_round(self):
        if self.current_a is None:
            self.current_a, self.current_b = self._choose_two()
        else:
            # keep winner as A, choose new B
            self.current_a = self.current_a
            self.current_b = random.choice(data)
            while self.current_b["name"] == self.current_a["name"]:
                self.current_b = random.choice(data)

        self._render_cards()
        self.result_label.config(text="Make your pick:")
        self._enable_buttons(True)

    def _render_cards(self):
        a = self.current_a
        b = self.current_b
        self.a_name.config(text=f"A: {a['name']}")
        self.a_desc.config(text=f"{a['description']}")
        self.a_country.config(text=f"Country: {a['country']}")

        self.b_name.config(text=f"B: {b['name']}")
        self.b_desc.config(text=f"{b['description']}")
        self.b_country.config(text=f"Country: {b['country']}")

    def _enable_buttons(self, enable: bool):
        state = "normal" if enable else "disabled"
        self.btn_a.config(state=state)
        self.btn_b.config(state=state)

    def _guess(self, pick: str):
        self._enable_buttons(False)
        a_count = self.current_a["follower_count"]
        b_count = self.current_b["follower_count"]

        correct = (pick == "A" and a_count >= b_count) or (pick == "B" and b_count >= a_count)

        if correct:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.result_label.config(text=f"Correct! {self._format_counts()}")
            # keep winner as A (the one with higher followers)
            if a_count >= b_count:
                self.current_a = self.current_a
            else:
                self.current_a = self.current_b

            self.root.after(1000, self._next_round)
        else:
            self.result_label.config(text=f"Wrong — final score: {self.score}. {self._format_counts()}")
            self._enable_buttons(False)

    def _format_counts(self):
        return f"A: {self.current_a['follower_count']}M — B: {self.current_b['follower_count']}M"

    def _restart(self):
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.current_a, self.current_b = self._choose_two()
        self._render_cards()
        self.result_label.config(text="Make your pick:")
        self._enable_buttons(True)


def main():
    root = tk.Tk()
    app = HigherLowerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
