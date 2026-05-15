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

def checkBallRectangleCollision(ball_x, ball_y, ball_radius, rect_x, rect_y, rect_width, rect_height):
    # find the closest point on the rectangle to the ball center
    closest_x = max(rect_x, min(ball_x, rect_x + rect_width))
    closest_y = max(rect_y, min(ball_y, rect_y + rect_height))

    # distance from ball center to that closest point
    dx = ball_x - closest_x
    dy = ball_y - closest_y
    dist = (dx**2 + dy**2) ** 0.5

    if dist >= ball_radius or dist == 0:
        return None  # duh

    # normal points from rectangle surface toward ball center
    nx = dx / dist
    ny = dy / dist

    # how far to push the ball out so it no longer overlaps
    overlap = ball_radius - dist

    return nx, ny, overlap

def applyNormals(ball_x, ball_y, overlap, v_x, v_y, n_x, n_y, cor):
    ball_x += n_x * overlap
    ball_y += n_y * overlap
    dot = v_x * n_x + v_y * n_y
    v_x -= 2 * dot * n_x
    v_y -= 2 * dot * n_y
    v_x *= cor
    v_y *= cor
    return ball_x, ball_y, v_x, v_y
