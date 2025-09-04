import tkinter as tk

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

        self.lbl_status = tk.Label(frame_top, text="Click để đặt/gỡ quân hậu ♛", font=("Arial", 10, "bold"))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(root, width=N*CELL_SIZE, height=N*CELL_SIZE)
        self.canvas.pack()

        self.queens = set()  
        self.draw_board()

  
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        """Vẽ bàn cờ 8x8 trắng đen"""
        self.canvas.delete("all")
        for r in range(N):
            for c in range(N):
                x1, y1 = c*CELL_SIZE, r*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "white" if (r+c) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

  
        for (r, c) in self.queens:
            x = c*CELL_SIZE + CELL_SIZE//2
            y = r*CELL_SIZE + CELL_SIZE//2
            fill_color = "black" if (r+c) % 2 == 0 else "white"  #
            self.canvas.create_text(x, y, text="♛", font=("Segoe UI Symbol", 32), fill=fill_color)

    def on_click(self, event):
        """Xử lý khi click chuột lên ô"""
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
        """Xóa toàn bộ quân hậu"""
        self.queens.clear()
        self.draw_board()
        self.update_status()

    def update_status(self):
        q = len(self.queens)
        self.lbl_status.config(text=f"Queens: {q}/8")

if __name__ == "__main__":
    root = tk.Tk()
    app = EightQueensUI(root)
    root.mainloop()
