import tkinter as tk
from collections import deque 

N = 8
CELL_SIZE = 60

class EightQueensUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Queens Puzzle")

        frame_top = tk.Frame(root, pady=5)
        frame_top.pack()

        btn_clear = tk.Button(frame_top, text="Clear", width=10, command=self.clear_board)
        btn_clear.pack(side=tk.LEFT, padx=5)

        btn_solve = tk.Button(frame_top, text="Solve DFS", width=10, command=self.prepare_solutions)
        btn_solve.pack(side=tk.LEFT, padx=5)

        btn_prev = tk.Button(frame_top, text="Previous", width=10, command=self.prev_solution)
        btn_prev.pack(side=tk.LEFT, padx=5)

        btn_next = tk.Button(frame_top, text="Next", width=10, command=self.next_solution)
        btn_next.pack(side=tk.LEFT, padx=5)

        self.lbl_status = tk.Label(frame_top, text="Click để đặt/gỡ quân hậu ♛", font=("Arial", 10, "bold"))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(root, width=N * CELL_SIZE, height=N * CELL_SIZE)
        self.canvas.pack()

        self.queens = set()
        self.solutions = []
        self.current_index = -1

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(N):
            for c in range(N):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "white" if (r + c) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        for (r, c) in self.queens:
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + CELL_SIZE // 2
            fill_color = "black" if (r + c) % 2 == 0 else "white"
            self.canvas.create_text(x, y, text="♛", font=("Segoe UI Symbol", 32), fill=fill_color)

    def on_click(self, event):
        r, c = event.y // CELL_SIZE, event.x // CELL_SIZE
        if (r, c) in self.queens:
            self.queens.remove((r, c))
        else:
            if len(self.queens) >= 8:
                self.root.bell()
                return
            self.queens.add((r, c))
        self.draw_board()
        self.update_status()

    def clear_board(self):
        self.queens.clear()
        self.solutions = []
        self.current_index = -1
        self.draw_board()
        self.update_status()

    def update_status(self):
        q = len(self.queens)
        if self.solutions:
            self.lbl_status.config(text=f"Queens: {q}/8 | Solution {self.current_index + 1}/{len(self.solutions)}")
        else:
            self.lbl_status.config(text=f"Queens: {q}/8")

    # --- Giải thuật DFS  ---

    def is_safe(self, current_solution, row, col):
        for r, c in enumerate(current_solution):
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def dfs_all_solutions(self):
        solutions = []
        def _solve_recursively(current_solution, row):
            if row == N:
                solutions.append(list(current_solution))
                return
            for col in range(N):
                if self.is_safe(current_solution, row, col):
                    current_solution.append(col)
                    _solve_recursively(current_solution, row + 1)
                    current_solution.pop()

        _solve_recursively([], 0)
        return solutions

    # --- Hiển thị nghiệm ---

    def prepare_solutions(self):
        self.solutions = self.dfs_all_solutions()
        self.current_index = 0 if self.solutions else -1
        if self.solutions:
            self.show_solution_at(self.current_index)
        else:
            self.lbl_status.config(text="Không tìm được nghiệm nào!")

    def show_solution_at(self, idx):
        sol = self.solutions[idx]
        self.queens = {(r, sol[r]) for r in range(N)}
        self.draw_board()
        self.update_status()

    def next_solution(self):
        if not self.solutions:
            self.lbl_status.config(text="Hãy nhấn Solve DFS trước!")
            return
        self.current_index = (self.current_index + 1) % len(self.solutions)
        self.show_solution_at(self.current_index)

    def prev_solution(self):
        if not self.solutions:
            self.lbl_status.config(text="Hãy nhấn Solve DFS trước!")
            return
        self.current_index = (self.current_index - 1) % len(self.solutions)
        self.show_solution_at(self.current_index)


# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = EightQueensUI(root)
    root.mainloop()