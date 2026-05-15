import pyray as pr

def updatePosition(p_x, p_y, v_x, v_y, a_x, a_y, dt):
    v_x += a_x * dt
    v_y += a_y * dt
    p_x += v_x * dt
    p_y += v_y * dt
    return p_x, p_y, v_x, v_y

def applyFriction(v_x, coefficient_of_friction, mass, gravity, dt):
    friction_force = coefficient_of_friction * mass * gravity
    friction_acceleration = friction_force / mass
    friction_deceleration = friction_acceleration * dt

    if abs(v_x) <= friction_deceleration:
        return 0
    elif v_x > 0:
        return v_x - friction_deceleration
    else:
        return v_x + friction_deceleration

def checkCollision(p_x, p_y, v_x, v_y, radius, w_width, w_height, floor_cor, walls_cor):
    if p_y > w_height - radius:
        p_y = w_height - radius
        v_y = -v_y * floor_cor
    if p_y < radius:
        p_y = radius
        v_y = -v_y * walls_cor

    if p_x < radius:
        p_x = radius
        v_x = -v_x * walls_cor
    if p_x > w_width - radius:
        p_x = w_width - radius
        v_x = -v_x * walls_cor
        
    return p_x, p_y, v_x, v_y

def main():

    window_width = 800
    window_height = 600

    walls_coefficient_of_restitution = 0.95
    floor_coefficient_of_restitution = 0.8
    mass = 1 # kg
    coefficient_of_friction = 0.8
    gravity = 400 # pixels per second per second
    class Ball:
        def __init__(self, x, y, v_x, v_y, a_x, a_y, radius, color):
            self.x = x
            self.y = y
            self.v_x = v_x
            self.v_y = v_y
            self.a_x = a_x
            self.a_y = a_y
            self.radius = radius
            self.color = color

    BALL_RADIUS = 25
    ball_color = pr.Color(255, 255, 255, 255)

    ball = Ball(400, 300, 0, 0, 0, gravity, BALL_RADIUS, ball_color)

    '''
    p_x = ball.x
    p_y = ball.y
    v_x = ball.v_x
    v_y = ball.v_y
    a_x = ball.a_x
    a_y = ball.a_y
    '''
    
    pr.init_window(window_width, window_height, "raylib-py simple test")
    pr.set_target_fps(60)

    while not pr.window_should_close():
        dt = pr.get_frame_time()

        on_floor = ball.y >= window_height - BALL_RADIUS

        f_x = 0
        f_y = mass * gravity

        if pr.is_key_down(pr.KEY_A) or pr.is_key_down(pr.KEY_LEFT):
            f_x -= 500
        if pr.is_key_down(pr.KEY_D) or pr.is_key_down(pr.KEY_RIGHT):
            f_x += 500
        if pr.is_key_down(pr.KEY_W) or pr.is_key_down(pr.KEY_UP):
            f_y -= 500
        if pr.is_key_down(pr.KEY_S) or pr.is_key_down(pr.KEY_DOWN):
            f_y += 500

        ball.a_x = f_x / mass
        ball.a_y = f_y / mass

        ball.x, ball.y, ball.v_x, ball.v_y = updatePosition(ball.x, ball.y, ball.v_x, ball.v_y, ball.a_x, ball.a_y, dt)
        ball.x, ball.y, ball.v_x, ball.v_y = checkCollision(ball.x, ball.y, ball.v_x, ball.v_y, BALL_RADIUS, window_width, window_height, floor_coefficient_of_restitution, walls_coefficient_of_restitution)
        ball.v_x = applyFriction(ball.v_x, coefficient_of_friction, mass, gravity, dt) if on_floor else ball.v_x

        pr.begin_drawing()
        pr.clear_background(pr.Color(135, 206, 235, 255))

        pr.draw_circle(int(ball.x), int(ball.y), BALL_RADIUS, ball_color)

        pr.draw_text(str(f_x), 10, 10, 20, pr.Color(0, 0, 0, 255))
        pr.draw_text(str(f_y), 10, 40, 20, pr.Color(0, 0, 0, 255))

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()