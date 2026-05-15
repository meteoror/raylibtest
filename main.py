import random
import pyray as pr
import lib

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

            self.x, self.y, self.v_x, self.v_y = lib.updatePosition(self.x, self.y, self.v_x, self.v_y, a_x, a_y, dt)
            self.x, self.y, self.v_x, self.v_y = lib.checkCollision(self.x, self.y, self.v_x, self.v_y, self.radius, window_width, window_height, floor_cor, walls_cor)
            self.v_x = lib.applyFriction(self.v_x, friction, self.mass, gravity, dt) if self.sliding else self.v_x

        def draw(self):
            pr.draw_circle(int(self.x), int(self.y), self.radius, self.color)

    class Rectangle:
        def __init__(self, x, y, width, height, color):
            self.x, self.y = x, y
            self.width, self.height = width, height
            self.color = color

        def draw(self):
            pr.draw_rectangle(int(self.x), int(self.y), int(self.width), int(self.height), self.color)

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
        for _ in range(3)
    ]
    
    Rectangles = [Rectangle(100, 400, 200, 20, pr.Color(139, 69, 19, 255))]

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

        for rect in Rectangles:
            if pr.is_key_down(pr.KEY_UP): rect.y -= 10
            if pr.is_key_down(pr.KEY_DOWN): rect.y += 10
            if pr.is_key_down(pr.KEY_LEFT): rect.x -= 10
            if pr.is_key_down(pr.KEY_RIGHT): rect.x += 10

        pr.begin_drawing()
        pr.clear_background(pr.Color(135, 206, 235, 255))

        for ball in Balls:
            ball.update(dt, input_fx, input_fy, window_width, window_height, gravity, floor_coefficient_of_restitution, walls_coefficient_of_restitution, coefficient_of_friction)
            
            # Check collision with each rectangle
            for rect in Rectangles:
                result = lib.checkBallRectangleCollision(ball.x, ball.y, ball.radius, rect.x, rect.y, rect.width, rect.height)
                
                if result:
                    n_x, n_y, overlap = result
                    ball.x, ball.y, ball.v_x, ball.v_y = lib.applyNormals(ball.x, ball.y, overlap, ball.v_x, ball.v_y, n_x, n_y, floor_coefficient_of_restitution)

            ball.draw()

        for rect in Rectangles:
            rect.draw()

        pr.draw_text(f"Time Scale: {time_scale:.2f}x", 600, 550, 20, pr.Color(0, 0, 0, 255))

        '''
        for i, ball in enumerate(Balls):
            y_offset = i * 50  # enough space for 2 lines per ball
            pr.draw_text(f"Ball {i} fx: {int(ball.f_x)} Newtons", 10, 10 + y_offset, 20, ball.color)
            pr.draw_text(f"Ball {i} fy: {int(ball.f_y)} Newtons", 10, 30 + y_offset, 20, ball.color)

            pr.draw_text(f"Ball {i} ax: {int(ball.f_x / ball.mass)} cm/s^2", 300, 10 + y_offset, 20, ball.color)
            pr.draw_text(f"Ball {i} ay: {int(ball.f_y / ball.mass)} cm/s^2", 300, 30 + y_offset, 20, ball.color)

            pr.draw_text(f"Ball {i} vx: {int(ball.v_x)} cm/s", 550, 10 + y_offset, 20, ball.color)
            pr.draw_text(f"Ball {i} vy: {int(ball.v_y)} cm/s", 550, 30 + y_offset, 20, ball.color)
        '''

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()