import tkinter as tk
import time
import random
import math

N = 8
CELL_SIZE = 60

INITIAL_TEMPERATURE = 50.0 

COOLING_RATE = 0.995

class SimulatedAnnealingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Queens Puzzle - Tuned Simulated Annealing")

        frame_top = tk.Frame(root, pady=5)
        frame_top.pack()
        
        btn_clear = tk.Button(frame_top, text="Clear Board", width=15, command=self.clear_board)
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        btn_solve = tk.Button(frame_top, text="Solve Simulated Annealing", width=25, command=self.solve_simulated_annealing)
        btn_solve.pack(side=tk.LEFT, padx=5)
        
        self.lbl_status = tk.Label(frame_top, text="Click để đặt tối đa 8 quân hậu", font=("Arial", 10, "bold"))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(root, width=N * CELL_SIZE, height=N * CELL_SIZE)
        self.canvas.pack()

        self.state = []
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(N):
            for c in range(N):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "white" if (r + c) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        for r, c in self.state:
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + CELL_SIZE // 2
            fill_color = "black" if (r + c) % 2 == 0 else "white"
            self.canvas.create_text(x, y, text="♛", font=("Segoe UI Symbol", 32), fill=fill_color)
        self.root.update_idletasks()
        
    def on_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        pos = (row, col)

        if pos in self.state:
            self.state.remove(pos)
        elif len(self.state) < 8:
            self.state.append(pos)
        else:
            self.root.bell()

        self.draw_board()
        self.update_status()

    def clear_board(self):
        self.state = []
        self.draw_board()
        self.update_status()

    def update_status(self):
        cost = self.calculate_cost(self.state)
        self.lbl_status.config(text=f"Đã đặt: {len(self.state)}/8 quân hậu | Chi phí hiện tại: {cost}")

    
    def calculate_cost(self, state):
        cost = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                r1, c1 = state[i]
                r2, c2 = state[j]
                if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    cost += 1
        return cost

    def solve_simulated_annealing(self):
        if len(self.state) != 8:
            self.lbl_status.config(text="Lỗi: Vui lòng đặt đủ 8 quân hậu trước khi giải!")
            return

        current_state = list(self.state)
        temperature = INITIAL_TEMPERATURE
        
        while temperature > 0.1:
            current_cost = self.calculate_cost(current_state)
            self.state = current_state
            self.draw_board()
            self.lbl_status.config(text=f"Đang tìm... Chi phí: {current_cost} | Nhiệt độ: {temperature:.2f}")
            time.sleep(0.01)

            if current_cost == 0:
                self.lbl_status.config(text=f"Đã tìm thấy lời giải! Chi phí: 0")
                return

            neighbor_state = list(current_state)
            queen_to_move_idx = random.randint(0, len(neighbor_state) - 1)
            while True:
                new_pos = (random.randint(0, N - 1), random.randint(0, N - 1))
                if new_pos not in neighbor_state:
                    neighbor_state[queen_to_move_idx] = new_pos
                    break
            
            neighbor_cost = self.calculate_cost(neighbor_state)
            delta_cost = neighbor_cost - current_cost

            if delta_cost < 0 or random.random() < math.exp(-delta_cost / temperature):
                current_state = neighbor_state
            
            temperature *= COOLING_RATE
            
        final_cost = self.calculate_cost(current_state)
        self.lbl_status.config(text=f"Quá trình kết thúc. Chi phí cuối: {final_cost}")

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SimulatedAnnealingUI(root)
    root.mainloop()