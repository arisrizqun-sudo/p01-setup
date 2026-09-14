import random
import tkinter as tk


WIDTH = 480
HEIGHT = 640
GROUND_HEIGHT = 80
PIPE_WIDTH = 72
PIPE_GAP = 175
BIRD_SIZE = 28
FRAME_MS = 20


class FlappyGame:
	def __init__(self, root):
		self.root = root
		self.root.title("Flappy Bird Sederhana")
		self.root.resizable(False, False)

		self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
		self.canvas.pack()
		self.canvas.bind("<Button-1>", self.flap)
		self.root.bind("<space>", self.flap)
		self.root.bind("<Return>", self.restart)

		self.best_score = 0
		self.running = False
		self.restart()

	def restart(self, _event=None):
		self.canvas.delete("all")
		self.bird_x = 110
		self.bird_y = HEIGHT // 2 - BIRD_SIZE // 2
		self.velocity = 0
		self.score = 0
		self.pipes = []
		self.running = True
		self.spawn_pipe(WIDTH + 40)
		self.spawn_pipe(WIDTH + 300)
		self.draw_background()
		self.update()

	def draw_background(self):
		self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#72c6e8", outline="")
		self.canvas.create_oval(35, 70, 145, 125, fill="#d8f3fa", outline="")
		self.canvas.create_oval(95, 48, 215, 125, fill="#d8f3fa", outline="")
		self.canvas.create_oval(335, 105, 455, 165, fill="#d8f3fa", outline="")
		self.canvas.create_rectangle(
			0, HEIGHT - GROUND_HEIGHT, WIDTH, HEIGHT, fill="#ded07b", outline=""
		)
		self.canvas.create_rectangle(
			0, HEIGHT - GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT + 12,
			fill="#79b84c", outline=""
		)

	def spawn_pipe(self, x):
		gap_top = random.randint(100, HEIGHT - GROUND_HEIGHT - PIPE_GAP - 40)
		self.pipes.append({"x": x, "gap_top": gap_top, "passed": False})

	def flap(self, _event=None):
		if self.running:
			self.velocity = -8.5

	def update(self):
		if not self.running:
			return

		self.velocity += 0.42
		self.bird_y += self.velocity
		for pipe in self.pipes:
			pipe["x"] -= 3.5
			if not pipe["passed"] and pipe["x"] + PIPE_WIDTH < self.bird_x:
				pipe["passed"] = True
				self.score += 1

		if self.pipes[-1]["x"] < WIDTH - 220:
			self.spawn_pipe(WIDTH + 30)
		self.pipes = [pipe for pipe in self.pipes if pipe["x"] > -PIPE_WIDTH]

		if self.collides():
			self.game_over()
			return

		self.draw()
		self.root.after(FRAME_MS, self.update)

	def collides(self):
		bird_left = self.bird_x
		bird_right = self.bird_x + BIRD_SIZE
		bird_top = self.bird_y
		bird_bottom = self.bird_y + BIRD_SIZE
		if bird_top <= 0 or bird_bottom >= HEIGHT - GROUND_HEIGHT:
			return True

		for pipe in self.pipes:
			pipe_left = pipe["x"]
			pipe_right = pipe["x"] + PIPE_WIDTH
			overlaps_x = bird_right > pipe_left and bird_left < pipe_right
			outside_gap = bird_top < pipe["gap_top"] or bird_bottom > pipe["gap_top"] + PIPE_GAP
			if overlaps_x and outside_gap:
				return True
		return False

	def draw(self):
		self.canvas.delete("game")
		for pipe in self.pipes:
			x = pipe["x"]
			gap_top = pipe["gap_top"]
			self.canvas.create_rectangle(x, 0, x + PIPE_WIDTH, gap_top, fill="#3ca34b", outline="#267333", tags="game")
			self.canvas.create_rectangle(
				x - 5, gap_top - 18, x + PIPE_WIDTH + 5, gap_top,
				fill="#48b957", outline="#267333", tags="game"
			)
			bottom_y = gap_top + PIPE_GAP
			self.canvas.create_rectangle(x, bottom_y, x + PIPE_WIDTH, HEIGHT - GROUND_HEIGHT, fill="#3ca34b", outline="#267333", tags="game")
			self.canvas.create_rectangle(
				x - 5, bottom_y, x + PIPE_WIDTH + 5, bottom_y + 18,
				fill="#48b957", outline="#267333", tags="game"
			)

		self.canvas.create_oval(
			self.bird_x, self.bird_y, self.bird_x + BIRD_SIZE, self.bird_y + BIRD_SIZE,
			fill="#ffd447", outline="#d18d22", width=2, tags="game"
		)
		self.canvas.create_oval(
			self.bird_x + 17, self.bird_y + 6, self.bird_x + 23, self.bird_y + 12,
			fill="white", outline="", tags="game"
		)
		self.canvas.create_oval(
			self.bird_x + 20, self.bird_y + 8, self.bird_x + 23, self.bird_y + 11,
			fill="#222", outline="", tags="game"
		)
		self.canvas.create_polygon(
			self.bird_x + BIRD_SIZE - 2, self.bird_y + 14,
			self.bird_x + BIRD_SIZE + 12, self.bird_y + 19,
			self.bird_x + BIRD_SIZE - 2, self.bird_y + 23,
			fill="#ef8f28", outline="#b86718", tags="game"
		)
		self.canvas.create_text(18, 18, anchor="nw", text=f"Skor: {self.score}", fill="white", font=("Arial", 20, "bold"), tags="game")

	def game_over(self):
		self.running = False
		self.best_score = max(self.best_score, self.score)
		self.canvas.create_rectangle(65, 225, WIDTH - 65, 415, fill="#fffdf2", outline="#355c7d", width=3, tags="game")
		self.canvas.create_text(WIDTH // 2, 265, text="GAME OVER", fill="#d84a3a", font=("Arial", 30, "bold"), tags="game")
		self.canvas.create_text(WIDTH // 2, 315, text=f"Skor: {self.score}   Rekor: {self.best_score}", fill="#263238", font=("Arial", 16), tags="game")
		self.canvas.create_text(WIDTH // 2, 365, text="Tekan ENTER untuk bermain lagi", fill="#355c7d", font=("Arial", 14), tags="game")


if __name__ == "__main__":
	window = tk.Tk()
	FlappyGame(window)
	window.mainloop()
