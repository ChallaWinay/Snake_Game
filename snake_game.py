import streamlit as st
import time
import random

# Game constants
GRID_SIZE = 20
CELL_SIZE = 20
GAME_SPEED = 0.2

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def init_game():
    if 'snake' not in st.session_state:
        st.session_state.snake = [(5, 5), (4, 5), (3, 5)]
    if 'food' not in st.session_state:
        st.session_state.food = generate_food()
    if 'direction' not in st.session_state:
        st.session_state.direction = RIGHT
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

def generate_food():
    while True:
        food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if food not in st.session_state.snake:
            return food

def move_snake():
    if st.session_state.game_over:
        return

    head_x, head_y = st.session_state.snake[0]
    dir_x, dir_y = st.session_state.direction
    new_head = (head_x + dir_x, head_y + dir_y)

    # Check collision with walls
    if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
        st.session_state.game_over = True
        return

    # Check collision with self
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head)

    # Check if food eaten
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = generate_food()
    else:
        st.session_state.snake.pop()

def change_direction(new_dir):
    # Prevent 180 degree turns
    if (new_dir[0] * -1, new_dir[1] * -1) != st.session_state.direction:
        st.session_state.direction = new_dir

def render_game():
    # Create a grid representation
    grid_html = '<div style="display: grid; grid-template-columns: repeat({}, 20px); gap: 1px; background-color: #333; width: fit-content; margin: auto;">'.format(GRID_SIZE)
    
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = "#000" # Empty
            if (x, y) in st.session_state.snake:
                color = "#0F0" # Snake
                if (x, y) == st.session_state.snake[0]:
                    color = "#00FF00" # Head (brighter)
            elif (x, y) == st.session_state.food:
                color = "#F00" # Food
            
            grid_html += f'<div style="width: 20px; height: 20px; background-color: {color};"></div>'
    
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Streamlit Snake Game", page_icon="🐍")
    
    st.title("🐍 Snake Game")
    
    init_game()
    
    # Controls
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⬆️"):
            change_direction(UP)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️"):
            change_direction(LEFT)
    with col3:
        if st.button("➡️"):
            change_direction(RIGHT)
            
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⬇️"):
            change_direction(DOWN)

    # Game Loop (Manual refresh for now to keep it simple, or auto-rerun)
    # Streamlit doesn't natively support a game loop well without 'st.empty' and 'time.sleep' blocking interaction.
    # For a shareable simple version, we can use a "Step" button or try to auto-refresh.
    # Let's add a "Auto Play" checkbox or just run the loop.
    
    if not st.session_state.game_over:
        move_snake()
        render_game()
        st.write(f"Score: {st.session_state.score}")
        
        # Add a small delay and rerun to create a loop effect if we want continuous movement
        # However, this blocks button inputs in standard Streamlit. 
        # A better approach for standard Streamlit is to rely on user interaction or use a very short sleep with rerun,
        # but that makes controls laggy.
        # For this MVP, let's stick to the button clicks driving the game or a slow auto-refresh.
        
        time.sleep(GAME_SPEED)
        st.rerun()
        
    else:
        st.error(f"Game Over! Final Score: {st.session_state.score}")
        if st.button("Restart"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
