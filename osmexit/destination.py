from osmexit import common
from osmexit.result import (
    Result, JointResult, UNKNOWN, SUCCESS, AMBIGUOUS, CONFLICT,
)


def assign_destination(node, way_in, ways_out):
    algos = {
        'basic': basic_exit_to,
        'left_right': left_right_exit_to,
        'destination_way': destination_way,
    }

    results = {}
    for k, v in algos.items():
        alg_results = v(node, way_in, ways_out)
        if alg_results:
            results[k] = alg_results

    if not results:
        return None
    return JointResult(results)


def basic_exit_to(node, way_in, ways_out):
    """
    A simple motorway junction where the node has
        highway=motorway_junction
        exit_to=*
    and there is only one motorway_link

    It returns Ambiguous if there is more than one motorway_link

    """
    node_schema = {
        'highway': 'motorway_junction',
        'exit_to': '*',
    }
    if not common.validate_tags(node['properties'], node_schema):
        return None

    links = [w for w in ways_out if w['properties']['highway'] == 'motorway_link' ]
    if len(links) == 0:
        return Result(UNKNOWN, msg='no motorway links')
    elif len(links) == 1:
        return Result(SUCCESS, solution=(links[0], node['properties']['exit_to']))
    else:
        return Result(AMBIGUOUS, msg='ref specified but not just one link out')


def left_right_exit_to(node, way_in, ways_out):
    """
    A motorway junction that splits into two links. The node has
        highway=motorway_junction
    and one or both of
        exit_to:left=*
        exit_to:right=*

    It returns Ambiguous if there are 3 connector roads, otherwise, left and
    right are assigned based on their geometries.

    """
    left_schema = {
        'highway': 'motorway_junction',
        'exit_to:left': '*',
    }
    is_left_exit = common.validate_tags(node['properties'], left_schema)

    right_schema = {
        'highway': 'motorway_junction',
        'exit_to:right': '*',
    }
    is_right_exit = common.validate_tags(node['properties'], right_schema)

    if not (is_left_exit or is_right_exit):
        return None

    if len(ways_out) != 2:
        msg = 'exit_to:left or exit_to:right specified but not 2 ways out'
        return Result(AMBIGUOUS, msg=msg)

    azimuth_in = common.azimuth(way_in['geometry']['coordinates'][-2:])
    def az_sort(way):
        coords = way['geometry']['coordinates'][:2]
        return common.delta_angle(azimuth_in, coords)
    ways_out = sorted(ways_out, key=az_sort)

    assignments = []
    if is_left_exit:
        assignments.append((ways_out[0], node['properties']['exit_to:left']))
    if is_right_exit:
        assignments.append((ways_out[1], node['properties']['exit_to:right']))

    return Result(SUCCESS, solution=assignments)


def destination_way(node, way_in, ways_out):
    """
    The simplest way to define the exit ref

    A motorway juction that splits into any number of connections. The node
    has
        highway=motorway_junction
    The connecting roads have
        destination=*

    There is no ambiguity for this method.

    """
    node_schema = {
        'highway': 'motorway_junction',
    }
    if not common.validate_tags(node['properties'], node_schema):
        return None

    assignments = []
    for w in ways_out:
        ref = w['properties'].get('destination')
        if ref:
            assignments.append((w, ref))

    if not assignments:
        return None
    return Result(SUCCESS, solution=assignments)
