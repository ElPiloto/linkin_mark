"""Generates a mapping from markdown files to linked markdown files.

Example usage:

  import linkin_mark as lm
  links = lm.get_links('/path/to/dir/of/md/files/')
  >>> {
          PosixPath('/path/to/dir/of/md/files/index.md'): 
              [PosixPath('/path/to/dir/of/md/files/linkedto1.md'),
               PosixPath('/path/to/dir/of/md/files/subdir/linkedto2.md')],
          PosixPath('/path/to/dir/of/md/files/linkedto1.md'): [],
          PosixPath('/path/to/dir/of/md/files/subdir/linkedto2.md'): 
              [PosixPath('/path/to/dir/of/md/files/index.md'),
               PosixPath('/path/to/dir/of/md/files/linkedto1.md')],
       }

  links = lm.get_relativized_links('/path/to/dir/of/md/files/')
  >>> {
          PosixPath('index.md'): 
              [PosixPath('linkedto1.md'),
               PosixPath('subdir/linkedto2.md')],
          PosixPath('linkedto1.md'): [],
          PosixPath('subdir/linkedto2.md'): 
              [PosixPath('index.md'),
               PosixPath('linkedto1.md')],
       }
  links = lm.get_relativized_links('/path/to/dir/of/md/files/',
                                   excluded_files=['index.md'])
  >>> {
          PosixPath('linkedto1.md'): [],
          PosixPath('subdir/linkedto2.md'): [PosixPath('linkedto1.md')],
       }

"""
from typing import Any, Callable, TypeVar
import os
import pathlib

import graphviz
import marko
from marko import inline
from marko import element

_DEFAULT_DIR = '/Users/lpiloto/code/web/luispiloto/content/pizzle-wiki/markdown/'

T = TypeVar('T')
StrOrPath = str | pathlib.Path


def get_links(
    root_dir: str,
    excluded_files: list[str] | None = None,
) -> dict[pathlib.Path, list[pathlib.Path]]:
  """Finds links between markdown files."""
  if excluded_files is None:
    excluded_files = []

  md_files = list_markdown_files(root_dir)

  links_per_file = {}
  for md in md_files:
    links = find_links(parse_markdown(md))
    links = [resolve_link(l, md) for l in links]
    rel_path = str(md.relative_to(root_dir))
    if rel_path not in excluded_files:
      links_per_file[md] = links
  return links_per_file


def get_relativized_links(
    root_dir: str,
    excluded_files: list[str] | None = None,
) -> dict[Any, list[pathlib.Path]]:
  """Finds links between markdown files and makes relative to root dir."""
  links = get_links(root_dir, excluded_files)
  return relativize_links(links, root_dir)


def list_markdown_files(root_dir: str) -> list[pathlib.Path]:
  """Finds all markdown files in rootdown directory."""
  root = pathlib.Path(root_dir)
  return list(root.rglob('*.md'))


def parse_markdown(md_file: pathlib.Path | str) -> marko.block.Document:
  """Parses markdown to marko Document."""
  with open(md_file, 'r') as f:
    file_contents = f.read()
  return marko.parse(file_contents)


def is_internal_link(dest: str) -> bool:
  """Checks this is not a web link or anchor tag link."""
  dest = dest.lower()
  is_external = 'http' in dest or 'www' in dest
  is_tag = '#' in dest
  return not (is_external or is_tag)


def find_links(
    el: element.Element | str,
) -> list[str]:
  """Recursively searches element for any links and returns link targets."""
  links = []
  if isinstance(el, inline.Link):
    link = el.dest
    if is_internal_link(link):
      links.append(link)
  if isinstance(el, marko.block.BlockElement) and hasattr(el, 'children'):
    for c in el.children:
      links += find_links(c)
  return links


def resolve_link(link: str, linked_from: pathlib.Path) -> pathlib.Path:
  """Resolve links which are specified relative to linking files."""
  link_dir = str(linked_from.parent)
  normed_path = os.path.normpath(os.path.join(link_dir, link))
  return pathlib.Path(normed_path)


def apply_to_links(
  fn: Callable[[T], T],
  links: dict[T, list[T]],
  ) -> dict[T, list[T]]:
  """Applies function to links in keys and values."""
  applied = {}
  for k, v in links.items():
    applied[fn(k)] = [fn(x) for x in v]
  return applied


def relativize_links(
    links: dict[StrOrPath, list[StrOrPath]],
    root_dir: StrOrPath
) -> dict[pathlib.Path, list[pathlib.Path]]:
  """Converts source and target links to paths relative to root_dir."""
  def _relativize(l: StrOrPath) -> pathlib.Path:
    return l.relative_to(root_dir)
  return apply_to_links(_relativize, links)
