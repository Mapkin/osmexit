import math

def validate_tags(tags, schema):
    for k, v in schema.items():
        if v == '*':
            if k in tags:
                continue
            else:
                return False
        elif v is None:
            if k not in tags:
                continue
            else:
                return False
        else:
            if tags.get(k) == v:
                continue
            else:
                return False

    return True


def delta_angle(reference_az, way):
    # Take the z-component of the cross product between way1 and way2 vectors.
    # If positive, then v1 is to the right of v2. If negative, v1 is to the
    # left of v2. If 0, they are the same vector.
    angle = azimuth(way) - reference_az

    if angle > math.pi:
        angle -= 2.0 * math.pi
    if angle < -math.pi:
        angle += 2.0 * math.pi

    return angle


def azimuth(c):
    dx = c[1][0] - c[0][0]
    dy = c[1][1] - c[0][1]

    angle = math.atan2(dy, dx)

    return angle
