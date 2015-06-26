osmexit
=======

Determine OSM highway exit information.


Overview
--------

Turn-by-turn navigation apps use highway exit numbers and exit sign
information to notify drivers when and where to turn off of major highways.
OpenStreetMap has  multiple schemes for tagging both the exit number and the
exit sign data at highway exits. There is nothing stopping mappers from using
multiple methods to convey the same information.  It's possible that more than
one tagging scheme is used on the same junction yielding different results.
It's also possible that the exit is tagged in such a way that the underlying
data is ambiguous as to which outgoing way is the actual exit, although a map
might show the proper exit number in the correct location.

osmexit analyzes the tags at motorway junction nodes and their connected ways.
It assigns the exit information to the outgoing ways in a uniform manner,
regardless of which tagging method is used. Furthermore it reports when two
different methods have conflicting results, and also when the tags are
ambiguous and no assignment can be made.  

Conflicting and ambiguous outputs should be cause for further investigation
and cleanup using tools like 
`to-fix <http://osmlab.github.io/to-fix/>`__ 
or 
`maproulette <http://maproulette.org/>`__.

Note that there's the critical assumption that exit information can and should
be determined by looking at the junction node and its immediately attached
ways.


Exit Numbers
------------
Basic Motorway Junction: Node tagged with ``highway=motorway_junction`` and
``ref=*``, the exit number is the node's ``ref`` tag. If one outgoing way is a
``highway=motorway_link``, then that way is assigned the exit number. If there
is more than one motorway link, then the rightmost (leftmost when driving on
the left side of the road) link is assigned the exit number.

Left/Right Junction: Node tagged with ``highway=motorway_junction`` and at
least one of ``ref:left=*`` or ``ref:right=*``. If there are two outgoing
ways, then the leftmost way is assigned exit number ``ref:left`` and the
rightmost way is assigned ``ref:right``. If there are not two outgoing ways
then this is an ambiguous situation.

Junction ref: Node tagged with ``highway=motorway_junction``. Any outgoing way
tagged with ``junction:ref=*`` is assigned that as its exit number.

No Ref: Node tagged with ``highway=motorway_junction`` and ``noref=yes``.
This exit and its outgoing ways have no exit number associated with them.


Destination Information
-----------------------
Basic Destination: Node tagged with ``highway=motorway_junction``. Any
outgoing way tagged with ``destination=*`` is assigned that as its destination
information.

Basic Exit To: Node tagged with ``highway=motorway_junction`` and ``exit_to``.
If one outgoing way is tagged with ``highway=motorway_link``, then that way is
assigned the ``exit_to`` information as its destination. If there is more than
one motorway link, then the rightmost (leftmost when driving on the left side
of the road) link is assigned ``exit_to`` as its destination information.

Left/Right Exit To: Node tagged with ``highway=motorway_junction`` and at
least one of ``exit_to:left=*`` or ``exit_to:right=*``. If there are two
outgoing ways, then the leftmost way is assigned ``exit_to:left`` as its
destination information and the right most is assigned ``exit_to:right`` as
its destination information. If there are not two outgoing ways then this is
an ambiguous situation.


See also
--------
- `OSM Wiki page for motorway_junction <http://wiki.openstreetmap.org/wiki/Tag:highway%3Dmotorway_junction>`__.
- `OSM Wiki page for destination=* <http://wiki.openstreetmap.org/wiki/Key:destination>`__.
- `OSM Wiki page for exit_to=* <https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=openstreetmap%20exit_to>`__.
