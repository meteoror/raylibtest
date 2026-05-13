import pyray as pr

# todo: make the floor thing a state so i can organize code better

def main():

    window_width = 800
    window_height = 600

    walls_coefficient_of_restitution = 0.95
    floor_coefficient_of_restitution = 0.8
    mass = 1 # kg
    coefficient_of_friction = 0.8
    gravity = 400 # pixels per second per second

    ball_radius = 25
    ball_color = pr.Color(255, 255, 255, 255)

    p_x = 400
    p_y = 300
    v_x = 0
    v_y = 0
    a_x = 0
    a_y = gravity  # pixels per second per second

    pr.init_window(window_width, window_height, "raylib-py simple test")
    pr.set_target_fps(60)

    while not pr.window_should_close():
        dt = pr.get_frame_time()

        on_floor = p_y >= window_height - ball_radius
        f_x = 0
        f_y = mass * gravity

        if pr.is_key_down(pr.KEY_A) or pr.is_key_down(pr.KEY_LEFT):
            f_x -= 500
        if pr.is_key_down(pr.KEY_D) or pr.is_key_down(pr.KEY_RIGHT):
            f_x += 500
        if pr.is_key_down(pr.KEY_W) or pr.is_key_down(pr.KEY_UP):
            f_y -= 500

        if on_floor and v_x != 0:
            friction_force = coefficient_of_friction * mass * gravity
            f_x += -friction_force if v_x > 0 else friction_force

        a_x = f_x / mass
        a_y = f_y / mass

        v_x += a_x * dt
        v_y += a_y * dt
        p_x += v_x * dt
        p_y += v_y * dt

        if p_y > window_height - ball_radius:
            p_y = window_height - ball_radius
            v_y = -v_y * floor_coefficient_of_restitution
        if p_y < ball_radius:
            p_y = ball_radius
            v_y = -v_y * walls_coefficient_of_restitution
        if p_x < ball_radius:
            p_x = ball_radius
            v_x = -v_x * walls_coefficient_of_restitution
        if p_x > window_width - ball_radius:
            p_x = window_width - ball_radius
            v_x = -v_x * walls_coefficient_of_restitution

        if on_floor and v_x != 0:
            friction_decel = coefficient_of_friction * gravity * dt
            if abs(v_x) <= friction_decel:
                v_x = 0
            elif v_x > 0:
                v_x -= friction_decel
            else:
                v_x += friction_decel

        pr.begin_drawing()
        pr.clear_background(pr.Color(135, 206, 235, 255))

        pr.draw_circle(int(p_x), int(p_y), ball_radius, ball_color)

        pr.draw_text(str(f_x), 10, 10, 20, pr.Color(0, 0, 0, 255))
        pr.draw_text(str(f_y), 10, 40, 20, pr.Color(0, 0, 0, 255))

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
