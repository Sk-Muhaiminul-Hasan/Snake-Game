from tkinter import *
import random

# Initial game settings
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Default difficulty (will be changed by selection)
SPEED = 0  # Will be set based on difficulty


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        # Using integer division (//) to ensure we get an integer
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    
    # Add play again button
    play_again_button = Button(window, text="Play Again", command=show_start_screen, font=('consolas', 20))
    play_again_button_window = canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 100, 
                                                   window=play_again_button)


def start_game(difficulty):
    global SPEED, score, direction, snake, food, canvas, label
    
    # Set speed based on difficulty
    if difficulty == "easy":
        SPEED = 150  # Slow
    elif difficulty == "medium":
        SPEED = 100  # Medium
    elif difficulty == "hard":
        SPEED = 50   # Fast - original speed
    
    # Clear the canvas
    canvas.delete(ALL)
    
    # Reset game state
    score = 0
    direction = 'down'
    
    # Create new score label
    if 'label' in globals():
        label.destroy()
    
    label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
    label.pack()
    
    # Create new canvas
    canvas.config(bg=BACKGROUND_COLOR)
    canvas.pack()
    
    # Initialize game objects
    snake = Snake()
    food = Food()
    
    # Start game loop
    next_turn(snake, food)


def show_start_screen():
    global canvas, label
    
    # Clear existing widgets
    if 'label' in globals():
        label.destroy()
    canvas.delete(ALL)
    
    # Set background
    canvas.config(bg="#333333")
    
    # Create title
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/4, 
                      text="SNAKE GAME", 
                      font=('consolas', 70), 
                      fill="#00FF00")
    
    # Create difficulty buttons
    difficulty_text = canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 - 50,
                                       text="Select Difficulty:", 
                                       font=('consolas', 30),
                                       fill="white")
    
    # Button dimensions and positioning
    button_width = 200
    button_height = 50
    button_y_start = GAME_HEIGHT/2 + 20
    button_spacing = 70
    
    # Easy button
    easy_button = Button(window, text="Easy", 
                       command=lambda: start_game("easy"),
                       font=('consolas', 20),
                       bg="#00AA00",
                       fg="white",
                       width=10)
    easy_button_window = canvas.create_window(GAME_WIDTH/2, button_y_start, 
                                           window=easy_button)
    
    # Medium button
    medium_button = Button(window, text="Medium", 
                         command=lambda: start_game("medium"),
                         font=('consolas', 20),
                         bg="#AAAA00",
                         fg="white",
                         width=10)
    medium_button_window = canvas.create_window(GAME_WIDTH/2, button_y_start + button_spacing, 
                                             window=medium_button)
    
    # Hard button
    hard_button = Button(window, text="Hard", 
                       command=lambda: start_game("hard"),
                       font=('consolas', 20),
                       bg="#AA0000",
                       fg="white",
                       width=10)
    hard_button_window = canvas.create_window(GAME_WIDTH/2, button_y_start + 2*button_spacing, 
                                           window=hard_button)


# Initialize the main window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Initialize canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set up keyboard controls
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Show the start screen
show_start_screen()

# Start the main loop
window.mainloop()