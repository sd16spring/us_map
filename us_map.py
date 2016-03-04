"""Exports a dict `states` that maps state codes to lists of polygons.

Author: Oliver Steele <oliver.steele@olin.edu>
License: MIT

Requirements:

    pip install BeautifulSoup
    pip install svg.path
"""

from BeautifulSoup import BeautifulSoup
from collections import OrderedDict
from svg.path import parse_path

__all__ = ['states', 'counties']

SEGMENT_CTL_PT_PROPS = ['start', 'control', 'control1', 'control2', 'end']
"""An ordered list of names of `svg.path` properties that hold control points."""


def get_segment_control_points(segment):
    """Given an `svg.path` segment, return its list of control points.
    Each control point is a pair of floats `(x, y)`.

    This does the minimum to support the paths in the map files.
    In particular, it simply returns the endpoints of arc segments."""

    cpts = [getattr(segment, prop) for prop in SEGMENT_CTL_PT_PROPS if hasattr(segment, prop)]
    return [(pt.real, pt.imag) for pt in cpts]


def path_to_points(path):
    """Given an `svg.path` Path, return a list of its control points.
    Each control point is a pair of floats `(x, y)`."""

    return [pt
            for segment in path
            for pt in get_segment_control_points(segment)]


def svg_path_to_polygons(path_data):
    """Return a list of polygons that collectively approximate the SVG path whose string is `path_data`."""

    # `svg.path` treats the Move command as though it were Line.
    # Split the path data, in order to collect one Path per contour.
    path_strings = [s for s in path_data.split('m') if s]
    path_prefix = 'm'

    polygons = []
    for path_string in path_strings:
        if path_string[0] not in 'M':
            path_string = path_prefix + path_string
        path = parse_path(path_string)
        polygons.append(path_to_points(path))
        end_pt = path[-1].end
        end_pt = path[0].start
        path_prefix = 'M %f,%f m' % (end_pt.real, end_pt.imag)

    return polygons


def _load_states(svg_filename='Blank_US_Map.svg'):
    """Initialize the `states` module variable."""

    states = {}

    with open(svg_filename, 'r') as svg:
        soup = BeautifulSoup(svg.read(), selfClosingTags=['defs'])

    for p in soup.findAll('path'):
        state_name = p.get('id', None)
        path_data = p.get('d', None)
        if state_name and path_data:
            states[state_name] = svg_path_to_polygons(path_data)

    return OrderedDict(sorted(states.items()))


def _load_counties(svg_filename='USA_Counties_with_FIPS_and_names.svg'):
    """Initialize the `counties` module variable."""

    counties_by_fips, counties_by_name = {}, {}

    with open(svg_filename, 'r') as svg:
        soup = BeautifulSoup(svg.read(), selfClosingTags=['defs'])

    for p in soup.findAll('path'):
        name = p.get('inkscape:label', None)
        fips = p.get('id', None)
        path_data = p.get('d', None)
        if name and ', ' in name:
            polygons = svg_path_to_polygons(path_data)
            assert len(polygons) == 1
            counties_by_fips[int(fips)] = polygons[0]
            counties_by_name[name] = polygons[0]

    return counties_by_fips, counties_by_name

states = _load_states()
"""A `dict` of state abbreviations (e.g. `"MA"`) to lists of polygons. Each polygon is a list of points.
Each point is a tuple of floats `(x, y)`."""

counties_by_fips, counties_by_name = _load_counties()

if __name__ == '__main__':
    print 'MA', len(states['MA'])
    print 'Norfolk County', len(counties_by_name['Norfolk, MA'])
    print 'FIPS 25021', len(counties_by_fips[25021])
