# Import the Turtle Graphics module
import turtle
import random

# Define program constants
WIDTH = 800
HEIGHT = 500
FOOD_SIZE = 20  # Pixels
EATING_DIST = 20

scores = []

offsets = {"up": (0, 20), "down": (0, -20), "right": (20, 0), "left": (-20, 0)}

def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("right"), "Right")
    screen.onkey(lambda: set_snake_direction("left"), "Left")

def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":  # preventing going backwards to itself
            snake_direction = "up"
    elif direction == "down":
        if snake_direction != "up":
            snake_direction = "down"
    elif direction == "right":
        if snake_direction != "left":
            snake_direction = "right"
    elif direction == "left":
        if snake_direction != "right":
            snake_direction = "left"

def game_loop():
    stamp.clearstamps()  # Removes existing snake

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check snake-snake & snake-wall collisions
    if new_head in snake or new_head[1] > HEIGHT/2 or new_head[1] < -HEIGHT/2 \
            or new_head[0] > WIDTH/2 or new_head[0] < -WIDTH/2:
        reset()
    else:
        # Add new head to the snake body
        snake.append(new_head)

        # Check snake-food collision
        if not food_collision():
            snake.pop(0)  # Removing last segment as the snake moves
            
        # Draw the snake
        for segment in snake:
            stamp.goto(segment[0], segment[1])
            stamp.stamp()

        # Making record
        scores.append(score)
        record = max(scores)
        
        # Refreshing the screen
        screen.title(f"Snake. Score: {score}. Record: {record}")
        screen.update()

        # Rinse and repeat
        turtle.ontimer(game_loop, delay)

def food_collision():
    global food_position, score, delay
    if get_distance(snake[-1], food_position) < EATING_DIST:
        score += 1
        delay = delay - 10  # Increasing speed as score rises
        food_position = get_random_food_position()  # Creating new food position if previous was eaten
        food.goto(food_position)
        return True
    return False

def get_random_food_position():  # except snake position
    x = random.randint(-WIDTH/2 + FOOD_SIZE, WIDTH/2 - FOOD_SIZE)
    y = random.randint(-HEIGHT/2 + FOOD_SIZE, HEIGHT/2 - FOOD_SIZE)
    return(x, y)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1)**2 + (x2 - x1)**2 )**(0.5)  # Pythagoras' theorem
    return distance

def reset():
    global score, delay, snake, snake_direction, food_position
    score = 0
    delay = 200  # Milliseconds
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
    snake_direction = "up"
    food_position = get_random_food_position()
    food.goto(food_position)
    game_loop()

# Game window
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)  # Set the dimensions of the Turtle Graphics window.
screen.bgcolor("black")
screen.tracer(0)  # Disables automatic animation

# Event handler (arrow key commands)
screen.listen()
bind_direction_keys()

# Snake
stamp = turtle.Turtle()
stamp.shape("circle")
stamp.penup()
stamp.color("green")  # Color of our future snake

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("orange")
food.shapesize(FOOD_SIZE / 20)
food.penup()

# Set all in motion
reset()

# Finish
turtle.done()
