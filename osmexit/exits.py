from osmexit import common
from osmexit.result import (
    Result, JointResult, UNKNOWN, SUCCESS, AMBIGUOUS, CONFLICT,
)


def assign_exits(node, way_in, ways_out):
    algos = {
        'noref': noref,
        'basic': basic_junction,
        'left_right': left_right_junction,
        'junction_ref': junction_ref,
    }

    results = {}
    for k, v in algos.items():
        alg_results = v(node, way_in, ways_out)
        if alg_results:
            results[k] = alg_results

    if not results:
        return None
    return JointResult(results)


def noref(node, way_in, ways_out):
    """
    A motorway junction where the node has
        highway=motorway_junction
        noref=yes
    
    This indicates that there are no assignments to be made.

    """
    node_schema = {
        'highway': 'motorway_junction',
        'noref': 'yes',
    }
    if not common.validate_tags(node['properties'], node_schema):
        return None

    # No assignments when noref is yes
    return Result(SUCCESS, ())


def basic_junction(node, way_in, ways_out):
    """
    A simple motorway junction where the node has
        highway=motorway_junction
        ref=*
    and there is only one motorway_link

    It returns Ambiguous if there is more than one motorway_link

    """
    node_schema = {
        'highway': 'motorway_junction',
        'ref': '*',
    }
    if not common.validate_tags(node['properties'], node_schema):
        return None

    links = [w for w in ways_out if w['properties'].get('highway') == 'motorway_link']
    if len(links) == 0:
        return Result(UNKNOWN, msg='no motorway links')
    elif len(links) == 1:
        return Result(SUCCESS, solution=[(links[0], node['properties']['ref'])])
    else:
        return Result(AMBIGUOUS, msg='ref specified but not just one link out')


def left_right_junction(node, way_in, ways_out):
    """
    A motorway junction that splits into two links. The node has
        highway=motorway_junction
    and one or both of
        ref:left=*
        ref:right=*

    It returns Ambiguous if there are 3 connector roads, otherwise, left and
    right are assigned based on their geometries.

    """
    left_schema = {
        'highway': 'motorway_junction',
        'ref:left': '*',
    }
    is_left_exit = common.validate_tags(node['properties'], left_schema)

    right_schema = {
        'highway': 'motorway_junction',
        'ref:right': '*',
    }
    is_right_exit = common.validate_tags(node['properties'], right_schema)

    if not (is_left_exit or is_right_exit):
        return None

    if len(ways_out) != 2:
        msg = 'ref:left or ref:right specified but not 2 ways out'
        return Result(AMBIGUOUS, msg=msg)

    azimuth_in = common.azimuth(way_in['geometry']['coordinates'][-2:])
    def az_sort(way):
        coords = way['geometry']['coordinates'][:2]
        return common.delta_angle(azimuth_in, coords)
    ways_out = sorted(ways_out, key=az_sort)

    assignments = []
    if is_left_exit:
        assignments.append((ways_out[0], node['properties']['ref:left']))
    if is_right_exit:
        assignments.append((ways_out[1], node['properties']['ref:right']))

    return Result(SUCCESS, solution=assignments)


def junction_ref(node, way_in, ways_out):
    """
    The simplest way to define the exit ref

    A motorway juction that splits into any number of connections. The node
    has
        highway=motorway_junction
    The connecting roads have
        junction:ref

    There is no ambiguity for this method.

    """
    node_schema = {
        'highway': 'motorway_junction',
    }
    if not common.validate_tags(node['properties'], node_schema):
        return None

    assignments = []
    for w in ways_out:
        ref = w['properties'].get('junction:ref')
        if ref:
            assignments.append((w, ref))

    if not assignments:
        return None
    return Result(SUCCESS, solution=assignments)
