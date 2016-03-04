# US States

A Python module for parsing U.S. States from an SVG file, and an example of using this with PyGame.

This is intended to support the SoftDes Spring 2016
[Interactive Programming project](https://sites.google.com/site/sd16spring/home/assignments-and-mini-projects/interactive-visualization).

The attached files consist of a module, `us_map.py`, that defines the shape of each U.S. state;
an SVG file `Blank_US_Map.svg` from which it reads these shapes;
and a short example `pygame_draw_state.py` of using [PyGame](http://www.pygame.org/hifi.html) to draw a single state.


## Requirements

Use `pip` to install these packages:

* BeautifulSoup
* svg.path
* matplotlib


## Examples

Print the polygon that defines the border of Colorado:

    import us_map
    print us_map.states['CO']

`pygame_draw_state.py` is a longer example that draws Colorado in a PyGame window.
This code also demonstrates how to determine if the mouse is inside the state.


## API

`us_map.states` is a dictionary *abbr* -> *shape*, where *state* is a two-letter
[ANSI U.S. abbreviation](https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations#Table).

*shape* is a list of polygons.
Each polygon is a list of tuples (x, y), where x and y are floats.

Many states, such as Colorado, consist of a single polygon.
Several, such as Massachusetts, consist of several.


## License

The Python files are released under the MIT License.

`Blank_US_Map.svg` is from the Wikipedia ([source](https://commons.wikimedia.org/wiki/File:Blank_US_Map.svg)),
and is licensed under the [GNU Free Documentation License](https://en.wikipedia.org/wiki/GNU_Free_Documentation_License).
