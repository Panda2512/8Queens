import tkinter as tk
import time
import random

N = 8
CELL_SIZE = 60

POPULATION_SIZE = 150 
MAX_GENERATIONS = 1000
MUTATION_RATE = 0.15 
TOURNAMENT_SIZE = 5

MAX_FITNESS = (N * (N - 1)) // 2 

class GeneticAlgorithmUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Queens Puzzle - Free Placement Genetic Algorithm")

        frame_top = tk.Frame(root, pady=5)
        frame_top.pack()
        
        btn_clear = tk.Button(frame_top, text="Clear Board", width=15, command=self.clear_board)
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        btn_solve = tk.Button(frame_top, text="Solve Genetic Algorithm", width=25, command=self.solve_genetic_algorithm)
        btn_solve.pack(side=tk.LEFT, padx=5)
        
        self.lbl_status = tk.Label(frame_top, text="Click để đặt tối đa 8 quân hậu", font=("Arial", 10, "bold"))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(root, width=N * CELL_SIZE, height=N * CELL_SIZE)
        self.canvas.pack()

        self.user_state = []
        self.population = []
        self.best_individual = []
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board([])

    def draw_board(self, individual):
        self.canvas.delete("all")
        for r in range(N):
            for c in range(N):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "white" if (r + c) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        for r, c in individual:
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + CELL_SIZE // 2
            fill_color = "black" if (r + c) % 2 == 0 else "white"
            self.canvas.create_text(x, y, text="♛", font=("Segoe UI Symbol", 32), fill=fill_color)
        self.root.update_idletasks()
        
    def on_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        pos = (row, col)

        if pos in self.user_state:
            self.user_state.remove(pos)
        elif len(self.user_state) < 8:
            self.user_state.append(pos)
        else:
            self.root.bell()

        self.draw_board(self.user_state)
        self.update_status_initial()

    def clear_board(self):
        self.user_state = []
        self.best_individual = []
        self.population = []
        self.draw_board([])
        self.lbl_status.config(text="Click để đặt tối đa 8 quân hậu")

    def update_status_initial(self):
        placed_queens = len(self.user_state)
        fitness = self.calculate_fitness(self.user_state)
        self.lbl_status.config(text=f"Đã đặt: {placed_queens}/8 | Fitness ban đầu: {fitness}/{MAX_FITNESS}")

    def update_status_solving(self, generation, fitness):
        self.lbl_status.config(text=f"Thế hệ: {generation} | Fitness tốt nhất: {fitness}/{MAX_FITNESS}")

    # --- Thuật toán Di truyền ---
    
    def calculate_fitness(self, individual):
        if len(individual) != 8:
            return 0
        clashes = 0
        for i in range(len(individual)):
            for j in range(i + 1, len(individual)):
                r1, c1 = individual[i]
                r2, c2 = individual[j]
                if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    clashes += 1
        return MAX_FITNESS - clashes

    def initialize_population_from_user_state(self):
        self.population = [list(self.user_state)]
        
        while len(self.population) < POPULATION_SIZE:
            mutated_individual = list(self.user_state)
            for _ in range(random.randint(1, 3)): 
                if not mutated_individual: continue
                idx_to_mutate = random.randrange(len(mutated_individual))

                new_pos = (random.randint(0, N-1), random.randint(0, N-1))
                while new_pos in mutated_individual:
                    new_pos = (random.randint(0, N-1), random.randint(0, N-1))
                
                mutated_individual[idx_to_mutate] = new_pos
            self.population.append(mutated_individual)

    def selection(self):
        tournament = random.sample(self.population, TOURNAMENT_SIZE)
        return max(tournament, key=self.calculate_fitness)

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, N - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        child = list(set(child)) 
        while len(child) < N:
            new_pos = (random.randint(0, N-1), random.randint(0, N-1))
            if new_pos not in child:
                child.append(new_pos)
        
        return child[:N]

    def mutate(self, individual):
        if random.random() < MUTATION_RATE:
            idx_to_mutate = random.randrange(len(individual))
            new_pos = (random.randint(0, N-1), random.randint(0, N-1))
            while new_pos in individual:
                new_pos = (random.randint(0, N-1), random.randint(0, N-1))
            individual[idx_to_mutate] = new_pos
        return individual

    def solve_genetic_algorithm(self):
        if len(self.user_state) != 8:
            self.lbl_status.config(text="Lỗi: Vui lòng đặt đủ 8 quân hậu trước khi giải!")
            return

        self.initialize_population_from_user_state()

        for generation in range(1, MAX_GENERATIONS + 1):
            self.population.sort(key=self.calculate_fitness, reverse=True)
            self.best_individual = self.population[0]
            best_fitness = self.calculate_fitness(self.best_individual)
            
            self.draw_board(self.best_individual)
            self.update_status_solving(generation, best_fitness)

            if best_fitness == MAX_FITNESS:
                self.lbl_status.config(text=f"Đã tìm thấy lời giải ở thế hệ {generation}! Fitness: {MAX_FITNESS}")
                return

            new_population = []
            elite_count = int(0.1 * POPULATION_SIZE)
            new_population.extend(self.population[:elite_count])

            while len(new_population) < POPULATION_SIZE:
                parent1 = self.selection()
                parent2 = self.selection()
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)

            self.population = new_population
        
        self.lbl_status.config(text=f"Kết thúc sau {MAX_GENERATIONS} thế hệ. Fitness tốt nhất: {best_fitness}")

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GeneticAlgorithmUI(root)
    root.mainloop() 