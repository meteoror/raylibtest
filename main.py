import random
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

    window_width = 800 # cm
    window_height = 600 # cm

    walls_coefficient_of_restitution = 0.95
    floor_coefficient_of_restitution = 0.8
    coefficient_of_friction = 0.8
    gravity = 981 # cm/s^2

    field_force = 1000 # N
    class Ball:
        def __init__(self, x, y, v_x, v_y, a_x, a_y, mass, radius, color):
            self.x = x
            self.y = y
            self.v_x = v_x
            self.v_y = v_y
            self.a_x = a_x
            self.a_y = a_y
            self.f_x = 0
            self.f_y = 0
            self.sliding = False
            self.mass = mass
            self.radius = radius
            self.color = color

    '''
    Balls = [
        Ball(100, 300, 0, 0, 0, gravity, 0.5, 10, pr.Color(255, 0, 0, 255)),
        Ball(300, 300, 0, 0, 0, gravity, 1, 20, pr.Color(0, 255, 0, 255)),
        Ball(500, 300, 0, 0, 0, gravity, 2, 40, pr.Color(0, 0, 255, 255))
    ]
    '''
    Balls = [
        Ball(
            random.randint(0, window_width//2),  
            random.randint(0, window_height//2),  
            0, 0, 0, gravity, 
            random.uniform(0.1, 1.5), 
            20,
            pr.Color(
                random.randint(0, 255),    
                random.randint(0, 255),    
                random.randint(0, 255),    
                255                        
            )
        )
        for _ in range(20)
    ]
    
    
    pr.init_window(window_width, window_height, "BLL-pt")
    pr.set_target_fps(45)

    while not pr.window_should_close():
        dt = pr.get_frame_time()

        for ball in Balls:
            ball.sliding = ball.y >= window_height - ball.radius

        for ball in Balls:
            ball.f_x = 0
            ball.f_y = ball.mass * gravity

        if pr.is_key_down(pr.KEY_A) or pr.is_key_down(pr.KEY_LEFT):
            for ball in Balls:
                ball.f_x -= field_force
        if pr.is_key_down(pr.KEY_D) or pr.is_key_down(pr.KEY_RIGHT):
            for ball in Balls:
                ball.f_x += field_force
        if pr.is_key_down(pr.KEY_W) or pr.is_key_down(pr.KEY_UP):
            for ball in Balls:
                ball.f_y -= field_force
        if pr.is_key_down(pr.KEY_S) or pr.is_key_down(pr.KEY_DOWN):
            for ball in Balls:
                ball.f_y += field_force

        for ball in Balls:
            ball.a_x = ball.f_x / ball.mass
            ball.a_y = ball.f_y / ball.mass

        for ball in Balls:
            ball.x, ball.y, ball.v_x, ball.v_y = updatePosition(ball.x, ball.y, ball.v_x, ball.v_y, ball.a_x, ball.a_y, dt)
            ball.x, ball.y, ball.v_x, ball.v_y = checkCollision(ball.x, ball.y, ball.v_x, ball.v_y, ball.radius, window_width, window_height, floor_coefficient_of_restitution, walls_coefficient_of_restitution)
            ball.v_x = applyFriction(ball.v_x, coefficient_of_friction, ball.mass, gravity, dt) if ball.sliding else ball.v_x

        pr.begin_drawing()
        pr.clear_background(pr.Color(135, 206, 235, 255))

        for ball in Balls:
            pr.draw_circle(int(ball.x), int(ball.y), ball.radius, ball.color)

        '''
        for i, ball in enumerate(Balls):
            y_offset = i * 50  # enough space for 2 lines per ball
            pr.draw_text(f"Ball {i} fx: {ball.f_x} Newtons", 10, 10 + y_offset, 20, ball.color)
            pr.draw_text(f"Ball {i} fy: {ball.f_y} Newtons", 10, 30 + y_offset, 20, ball.color)
        '''
        
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()