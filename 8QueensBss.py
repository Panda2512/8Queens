import tkinter as tk
from collections import deque

N = 8
CELL_SIZE = 60

class BeliefStateSearchUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Queens Puzzle - Belief State Search (Simulation)")
        frame_top = tk.Frame(root, pady=5)
        frame_top.pack()
        
        btn_clear = tk.Button(frame_top, text="Clear", width=10, command=self.clear_board)
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        btn_solve = tk.Button(frame_top, text="Solve Belief State", width=20, command=self.prepare_solutions)
        btn_solve.pack(side=tk.LEFT, padx=5)
        
        btn_prev = tk.Button(frame_top, text="Previous", width=10, command=self.prev_solution)
        btn_prev.pack(side=tk.LEFT, padx=5)
        
        btn_next = tk.Button(frame_top, text="Next", width=10, command=self.next_solution)
        btn_next.pack(side=tk.LEFT, padx=5)

        self.lbl_status = tk.Label(frame_top, text="Nhấn 'Solve' để bắt đầu", font=("Arial", 10, "bold"))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(root, width=N * CELL_SIZE, height=N * CELL_SIZE)
        self.canvas.pack()

        self.queens = set()
        self.solutions = []
        self.current_index = -1
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(N):
            for c in range(N):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "white" if (r + c) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        for r, c in self.queens:
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + CELL_SIZE // 2
            fill_color = "black" if (r + c) % 2 == 0 else "white"
            self.canvas.create_text(x, y, text="♛", font=("Segoe UI Symbol", 32), fill=fill_color)
        self.root.update_idletasks()

    def clear_board(self):
        self.queens.clear()
        self.solutions = []
        self.current_index = -1
        self.draw_board()
        self.lbl_status.config(text="Nhấn 'Solve' để bắt đầu")

    def update_status(self):
        if self.solutions:
            self.lbl_status.config(text=f"Solution {self.current_index + 1}/{len(self.solutions)}")
        else:
            self.lbl_status.config(text="Đang giải...")

    def prepare_solutions(self):
        self.clear_board()
        self.update_status()
        self.solutions = self.solve_belief_state_search()
        
        self.current_index = 0 if self.solutions else -1
        if self.solutions:
            self.show_solution_at(self.current_index)
        else:
            self.lbl_status.config(text="Không tìm được nghiệm nào!")

    def show_solution_at(self, idx):
        sol = self.solutions[idx]
        self.queens = {(r, col) for r, col in enumerate(sol)}
        self.draw_board()
        self.update_status()

    def next_solution(self):
        if not self.solutions: return
        self.current_index = (self.current_index + 1) % len(self.solutions)
        self.show_solution_at(self.current_index)

    def prev_solution(self):
        if not self.solutions: return
        self.current_index = (self.current_index - 1) % len(self.solutions)
        self.show_solution_at(self.current_index)

    # --- Thuật toán Belief State Search ---
    
    def is_safe(self, state, row, col):
        for r, c in enumerate(state):
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def solve_belief_state_search(self):
        solutions = []
        q = deque()
        
        initial_belief_state = [[]]
        q.append(initial_belief_state)

        while q:
            current_belief_state = q.popleft()
            
            state = current_belief_state[0]
            row = len(state)

            if row == N:
                solutions.append(state)
                continue

            for col in range(N):

                if self.is_safe(state, row, col):
                    new_state = state + [col]
                    new_belief_state = [new_state]
                    q.append(new_belief_state)
        
        return solutions

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BeliefStateSearchUI(root)
    root.mainloop()