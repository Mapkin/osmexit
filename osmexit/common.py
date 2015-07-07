import math


def iter_intersection_info(g):
    for n in g.nodes_iter():
        if g.node[n].get('highway') != 'motorway_junction':
            continue
        try:
            info = build_intersection(g, n)
        except:
            continue
        yield info


def build_intersection(g, n):
    node_coords = g.node[n]['coordinates']
    node = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': node_coords,
        },
        'properties': g.node[n]
    }

    way_in_node = g.predecessors(n)
    if len(way_in_node) > 1:
        raise ValueError('Node {} has more than one way in'.format(node_coords))
    way_in_node = way_in_node[0]
    
    way_in = feature_for_edge(g, way_in_node, n)
    ways_out = [feature_for_edge(g, n, n_out) for n_out in g.successors(n)]

    return node, way_in, ways_out


def feature_for_edge(g, n1, n2):
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'LineString',
            'coordinates': [g.node[n1]['coordinates'], g.node[n2]['coordinates']],
        },
    }
    props = g[n1][n2]['tags'].copy()
    props['length'] = g[n1][n2]['length']
    feature['properties'] = props

    return feature



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
