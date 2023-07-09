from typing import TypeVar
import graphviz
import os
import pathlib


T = TypeVar('T')


PALETTES = {
  'shmoop': [
    '#001219',
    '#005f73',
    '#0a9396',
    '#94d2bd',
    '#e9d8a6',
    '#ee9b00',
    '#ca6702',
    '#bb3e03',
    '#ae2012',
    '#9b2226'
  ],
  'shmoop2': [
    "#34d1ff",
    "#349dff",
    "#346aff",
    "#3437ff",
    "#6334ff",
    "#c934ff",
    "#ff349d",
    "#ff3437"
  ],
  'pastel': [
    "#cdb4db",
    "#ffc8dd",
    "#ffafcc",
    "#bde0fe",
    "#a2d2ff"
  ],
}


DEFAULT_COLOR_PALETTE = PALETTES['pastel']
DEFAULT_BG_COLOR = '#838584'


def get_node_colors(
    links: list[str],
    colors: list[str] = DEFAULT_COLOR_PALETTE,
) -> dict[str, str]:
  """Maps parent directories to colors."""
  dirs = set([os.path.dirname(l) for l in links])
  dirs_to_colors = {
      d: colors[i % len(colors)] for i, d in enumerate(dirs)
  }
  links_to_colors = {
      l: dirs_to_colors[os.path.dirname(l)] for l in links
  }
  return links_to_colors


def graph_with_colors_by_dir(
    links_per_file: dict[pathlib.Path, list[pathlib.Path]],
    root_dir: str | pathlib.Path,
    colors: list[str] = DEFAULT_COLOR_PALETTE,
    bg_color: str = DEFAULT_BG_COLOR,
    edge_color: str = '#000000',
    layout_engine: str = 'sfdp',
) -> None:
  """Draws a graph where nodes are colored based on their parent directory."""
  dot = graphviz.Digraph(
      'links',
      engine=layout_engine,
      graph_attr={'bgcolor': bg_color}
  )
  links_to_colors = get_node_colors([str(l) for l in links_per_file.keys()])
  node_names = []
  for file in links_per_file.keys():
    # fname = str(file.relative_to(root_dir))
    node_names.append(str(file))
    attributes = {}
    attributes['fillcolor'] = links_to_colors[str(file)]
    attributes['style'] = 'filled'
    dot.node(str(file), **attributes)

  for file, links in links_per_file.items():
    for l in links:
      if str(l) in node_names:
        dot.edge(str(file), str(l))

  dot.view()


