import tkinter as tk
import copy
from itertools import product

N = 8
CELL_SIZE = 60

class AndOrSearchUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Queens Puzzle - AND-OR Search (CSP)")

        frame_top = tk.Frame(root, pady=5)
        frame_top.pack()
        
        btn_clear = tk.Button(frame_top, text="Clear", width=10, command=self.clear_board)
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        btn_solve = tk.Button(frame_top, text="Solve AND-OR", width=15, command=self.prepare_solutions)
        btn_solve.pack(side=tk.LEFT, padx=5)
        
        btn_prev = tk.Button(frame_top, text="Previous", width=10, command=self.prev_solution)
        btn_prev.pack(side=tk.LEFT, padx=5)
        
        btn_next = tk.Button(frame_top, text="Next", width=10, command=self.next_solution)
        btn_next.pack(side=tk.LEFT, padx=5)

        self.lbl_status = tk.Label(frame_top, text="Nhấn 'Solve AND-OR' để bắt đầu", font=("Arial", 10, "bold"))
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
        self.lbl_status.config(text="Nhấn 'Solve AND-OR' để bắt đầu")

    def update_status(self):
        if self.solutions:
            self.lbl_status.config(text=f"Solution {self.current_index + 1}/{len(self.solutions)}")
        else:
            self.lbl_status.config(text="Đang giải...")

    def prepare_solutions(self):
        self.clear_board()
        self.update_status()
        
        self.solutions = self.nqueens_and_or_solver()
        
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

    # --- Thuật toán AND-OR Search ---
    
    def an_toan(self, state, row, col):
        for r, c in enumerate(state):
            if c == col or abs(row - r) == abs(col - c):
                return False
        return True

    def consistent(self, assign, var, val):
        state = [assign[r] for r in sorted(assign)]
        return self.an_toan(state, var, val)

    def build_constraint_graph(self, unassigned, domains):
        graph = {v: set() for v in unassigned}
        for i in range(len(unassigned)):
            for j in range(i + 1, len(unassigned)):
                a, b = unassigned[i], unassigned[j]
                edge = False
                for ca in domains[a]:
                    for cb in domains[b]:
                        if ca == cb or abs(a - b) == abs(ca - cb):
                            edge = True
                            break
                    if edge: break
                if edge:
                    graph[a].add(b)
                    graph[b].add(a)
        return graph

    def connected_components(self, graph):
        seen = set()
        comps = []
        for v in graph:
            if v in seen: continue
            comp = []
            stack = [v]
            seen.add(v)
            while stack:
                x = stack.pop()
                comp.append(x)
                for nb in graph[x]:
                    if nb not in seen:
                        seen.add(nb)
                        stack.append(nb)
            comps.append(comp)
        return comps

    def OrSearch(self, unassigned, domains, assign, find_all=True):
        if not unassigned:
            return [dict(assign)]
        var = min(unassigned, key=lambda v: len(domains[v]))
        solutions = []
        for val in sorted(list(domains[var])):
            if not self.consistent(assign, var, val):
                continue
            assign2 = dict(assign)
            assign2[var] = val
            domains2 = copy.deepcopy(domains)
            domains2[var] = {val}
            failure = False
            for v in unassigned:
                if v == var: continue
                remove = set()
                for cv in domains2[v]:
                    if cv == val or abs(v - var) == abs(cv - val):
                        remove.add(cv)
                if remove:
                    domains2[v] -= remove
                    if not domains2[v]:
                        failure = True
                        break
            if failure:
                continue
            remaining = [v for v in unassigned if v != var]
            if not remaining:
                solutions.append(dict(assign2))
                if not find_all: return solutions
                continue
            
            graph = self.build_constraint_graph(remaining, domains2)
            components = self.connected_components(graph)
            comp_solutions_list = []
            comp_failed = False
            for comp in components:
                comp_sols = self.OrSearch(comp, domains2, assign2) 
                if not comp_sols:
                    comp_failed = True
                    break
                comp_solutions_list.append(comp_sols)
            if comp_failed:
                continue
            for prod in product(*comp_solutions_list):
                merged = dict(assign2)
                for d in prod:
                    merged.update(d)
                solutions.append(merged)
                if not find_all and solutions:
                    return solutions
        return solutions

    def nqueens_and_or_solver(self, N=8, find_all=True):
        variables = list(range(N))
        domains_init = {v: set(range(N)) for v in variables}
        all_solutions = self.OrSearch(variables, domains_init, {}, find_all)
        return [[sol[r] for r in range(N)] for sol in all_solutions]

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AndOrSearchUI(root)
    root.mainloop()