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
    class PhysicsBody:
        def __init__(self, x, y, vx, vy, mass):
            self.x, self.y = x, y
            self.v_x, self.v_y = vx, vy
            self.mass = mass
            self.f_x, self.f_y = 0, 0

        def apply_force(self, fx, fy):
            self.f_x += fx
            self.f_y += fy

        def integrate(self, dt):
            a_x = self.f_x / self.mass
            a_y = self.f_y / self.mass
            self.x, self.y, self.v_x, self.v_y = lib.updatePosition(
                self.x, self.y, self.v_x, self.v_y, a_x, a_y, dt
            )
            self.f_x, self.f_y = 0, 0  # reset forces each frame

    class Ball(PhysicsBody):
        def __init__(self, x, y, vx, vy, mass, radius, color):
            super().__init__(x, y, vx, vy, mass)
            self.radius = radius
            self.color = color

        def update(self, dt, window_width, window_height, gravity, floor_cor, walls_cor, friction):
            self.apply_force(0, self.mass * gravity)  # gravity only for balls
            self.integrate(dt)
            self.x, self.y, self.v_x, self.v_y = lib.checkCollision(
                self.x, self.y, self.v_x, self.v_y, self.radius,
                window_width, window_height, floor_cor, walls_cor
            )
            if self.y >= window_height - self.radius:
                self.v_x = lib.applyFriction(self.v_x, friction, self.mass, gravity, dt)

        def draw(self):
            pr.draw_circle(int(self.x), int(self.y), self.radius, self.color)

    class Rectangle(PhysicsBody):
        def __init__(self, x, y, vx, vy, mass, width, height, color):
            super().__init__(x, y, vx, vy, mass)
            self.width, self.height = width, height
            self.color = color

        def update(self, dt):
            self.integrate(dt)  # no gravity, no wall collisions

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
        for _ in range(1)
    ]
    
    Rectangles = [Rectangle(100, 400, 0, 0, 0.05, 200, 20, pr.Color(139, 69, 19, 255))]

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

        pr.begin_drawing()
        pr.clear_background(pr.Color(135, 206, 235, 255))

        for ball in Balls:
            if pr.is_key_down(pr.KEY_A): ball.apply_force(-field_force, 0)
            if pr.is_key_down(pr.KEY_D): ball.apply_force( field_force, 0)
            if pr.is_key_down(pr.KEY_W): ball.apply_force(0, -field_force)
            if pr.is_key_down(pr.KEY_S): ball.apply_force(0,  field_force)
            ball.update(dt, window_width, window_height, gravity, floor_coefficient_of_restitution, walls_coefficient_of_restitution, coefficient_of_friction)
            
            for rect in Rectangles:
                result = lib.checkBallRectangleCollision(ball.x, ball.y, ball.radius, rect.x, rect.y, rect.width, rect.height)
                if result:
                    n_x, n_y, overlap = result
                    ball.x, ball.y, ball.v_x, ball.v_y = lib.applyNormals(ball.x, ball.y, overlap, ball.v_x, ball.v_y, n_x, n_y, floor_coefficient_of_restitution, rect.v_x, rect.v_y)
            
            ball.draw()

        for rect in Rectangles:
            prev_x, prev_y = rect.x, rect.y

            if pr.is_key_down(pr.KEY_UP):    rect.apply_force(0, -field_force)
            if pr.is_key_down(pr.KEY_DOWN):  rect.apply_force(0,  field_force)
            if pr.is_key_down(pr.KEY_LEFT):  rect.apply_force(-field_force, 0)
            if pr.is_key_down(pr.KEY_RIGHT): rect.apply_force( field_force, 0)

            rect.update(dt)
            rect.v_x = rect.x - prev_x
            rect.v_y = rect.y - prev_y

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