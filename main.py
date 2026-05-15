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
        def __init__(self, x, y, vx, vy, mass, radius, color):
            self.x, self.y = x, y
            self.v_x, self.v_y = vx, vy
            self.mass = mass
            self.radius = radius
            self.color = color

        def update(self, dt, f_x, f_y, window_width, window_height, gravity, floor_cor, walls_cor, friction):
            self.f_x = f_x
            self.f_y = f_y + self.mass * gravity

            self.sliding = self.y >= window_height - self.radius

            a_x = self.f_x / self.mass
            a_y = (self.f_y + self.mass * gravity) / self.mass

            self.x, self.y, self.v_x, self.v_y = updatePosition(self.x, self.y, self.v_x, self.v_y, a_x, a_y, dt)
            self.x, self.y, self.v_x, self.v_y = checkCollision(self.x, self.y, self.v_x, self.v_y, self.radius, window_width, window_height, floor_cor, walls_cor)
            self.v_x = applyFriction(self.v_x, friction, self.mass, gravity, dt) if self.sliding else self.v_x

        def draw(self):
            pr.draw_circle(int(self.x), int(self.y), self.radius, self.color)

    '''
    Balls = [
        Ball(100, 300, 0, 0, 0, gravity, 0.5, 10, pr.Color(255, 0, 0, 255)),
        Ball(300, 300, 0, 0, 0, gravity, 1, 20, pr.Color(0, 255, 0, 255)),
        Ball(500, 300, 0, 0, 0, gravity, 2, 40, pr.Color(0, 0, 255, 255))
    ]
    '''
    Balls = [
        Ball(
            random.randint(0, window_width//2) + window_width//4,  
            random.randint(0, window_height//2) + window_height//4,  
            0, 0,
            random.uniform(0.1, 0.5), 
            20,
            pr.Color(
                random.randint(0, 255),    
                random.randint(0, 255),    
                random.randint(0, 255),    
                255                        
            )
        )
        for _ in range(30)
    ]
    
    
    pr.init_window(window_width, window_height, "BLL-pt")
    pr.set_target_fps(45)

    time_scale = 1.0

    while not pr.window_should_close():
        dt = pr.get_frame_time()

        if pr.is_key_pressed(pr.KEY_H):
            time_scale *= 0.5
        if pr.is_key_pressed(pr.KEY_J):
            time_scale *= 2.0

        dt *= time_scale

        # gather input once, outside the ball loop
        input_fx, input_fy = 0, 0
        if pr.is_key_down(pr.KEY_A): input_fx -= field_force
        if pr.is_key_down(pr.KEY_D): input_fx += field_force
        if pr.is_key_down(pr.KEY_W): input_fy -= field_force
        if pr.is_key_down(pr.KEY_S): input_fy += field_force

        pr.begin_drawing()
        pr.clear_background(pr.Color(135, 206, 235, 255))

        for ball in Balls:
            ball.update(dt, input_fx, input_fy, window_width, window_height, gravity, floor_coefficient_of_restitution, walls_coefficient_of_restitution, coefficient_of_friction)
            ball.draw()

        pr.draw_text(f"Time Scale: {time_scale:.2f}x", 10, 10, 20, pr.Color(0, 0, 0, 255))

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