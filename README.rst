osmexit
======

Determine OSM highway exit information.

Huh?
----

OpenStreetMap has several different tagging schemes for exit information at
highway exits.  There are multiple independent schemes for indicating both the
exit number and the highway sign (destination) information. There is nothing
stopping mappers from using multiple methods to convey the same information.
It is also possible that the exit is tagged in such a way that the map will
display the exit number in the correct location, but the underlying data is
ambiguous as to which outgoing way is the actual exit ramp.

osmexit analyzes the tags at motorway junction nodes and their connected ways.
It assigns the exit information to the outgoing ways in a uniform manner,
regardless of which tagging method is used. Furthermore it reports when two
different methods have conflicting results, and also when the tags are
ambiguous and no assignment can be made.

Conflicting and ambiguous outputs should be cause for further investigation and
cleanup.


See also
--------

- Paste Script's `paster create <http://pythonpaste.org/script/#paster-create>`__ is
  one that I've used for a long time.
- `cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`__ is
  a Cookiecutter template for a Python package. Cookiecutter supports many languages,
  includes Travis configuration and much more.

