import graphviz
import os
import pathlib

import marko

_DEFAULT_DIR = '/Users/lpiloto/code/web/luispiloto/content/pizzle-wiki/markdown/'


def list_markdown_files(root_dir: str) -> list[pathlib.Path]:
  root = pathlib.Path(root_dir)
  return list(root.rglob('*.md'))


def parse_markdown(md_file: pathlib.Path):
  with open(md_file.absolute(), 'r') as f:
    file_contents = f.read()
  return marko.parse(file_contents)


def is_valid_link(dest: str) -> bool:
  dest = dest.lower()
  is_external = 'http' in dest or 'www' in dest
  is_tag = '#' in dest
  return not (is_external or is_tag)


def find_links(
    el: marko.block.BlockElement | marko.inline.InlineElement,
) -> list[str]:
  links = []
  if isinstance(el, marko.inline.Link):
    link = el.dest
    if is_valid_link(link):
      links.append(link)
  if hasattr(el, 'children'):
    for c in el.children:
      links += find_links(c)
  return links


def standardize_link(l: str, root_dir, link_file: pathlib.Path):
  if not l.endswith('.md'):
    l += '.md'
  link_dir = str(link_file.parent)
  normed_path = os.path.normpath(os.path.join(link_dir, l))
  return str(pathlib.Path(normed_path).relative_to(root_dir))


def links_to_graph(links_per_file, root_dir: str):
  dot = graphviz.Digraph('links', engine='circo')
  # first let's add all the nodes
  node_names = []
  for file in links_per_file.keys():
    fname = str(file.relative_to(root_dir))
    node_names.append(fname)
    dot.node(fname)
  for file, links in links_per_file.items():
    fname = str(file.relative_to(root_dir))
    for l in links:
      l = standardize_link(l, root_dir, file)
      if l in node_names:
        print(f'Found edge: {fname} ---> {l}')
        dot.edge(fname, l)
      else:
        print(f'{fname},    {l}')

  dot.view()

_EXCLUDED_FILES = ['index.md', 'diary/diary.md']
root_dir = _DEFAULT_DIR
md_files = list_markdown_files(root_dir)
links_per_file = {}
for md in md_files:
  links = find_links(parse_markdown(md))
  rel_path = str(md.relative_to(root_dir))
  if rel_path not in _EXCLUDED_FILES:
    links_per_file[md] = links

links_to_graph(links_per_file, root_dir)
