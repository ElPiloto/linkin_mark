"""Test for linkin_mark.lib."""
import importlib.resources
import os
import pathlib
import unittest

import linkin_mark as lm


class TestLinks(unittest.TestCase):
  def setUp(self) -> None:
    self.data_path = str(importlib.resources.files('test').joinpath('test_data'))
    return super().setUp()

  def test_get_links(self):
    links = lm.get_links(self.data_path)
    index_md = pathlib.Path(os.path.join(self.data_path, 'index.md'))
    one_md = pathlib.Path(os.path.join(self.data_path, 'linkedto1.md'))
    two_md = pathlib.Path(
        os.path.join(self.data_path, 'subdir', 'linkedto2.md')
    )
    expected_links = {
        index_md: [one_md, two_md],
        one_md: [],
        two_md: [one_md],
    }
    self.assertSetEqual(
        set(expected_links.keys()),
        set(links.keys()),
        'Did not find expected markdown files',
    )
    self.assertDictEqual(
        expected_links,
        links,
        'Did not find links in markdown files'
    )

  def test_get_relative_links(self):
    links = lm.get_relative_links(self.data_path)
    index_md = pathlib.Path('index.md')
    one_md = pathlib.Path('linkedto1.md')
    two_md = pathlib.Path(os.path.join('subdir', 'linkedto2.md'))
    expected_links = {
        index_md: [one_md, two_md],
        one_md: [],
        two_md: [one_md],
    }
    self.assertSetEqual(
        set(expected_links.keys()),
        set(links.keys()),
        'Did not find expected markdown files',
    )
    self.assertDictEqual(
        expected_links,
        links,
        'Did not find links in markdown files'
    )

  def test_get_links_excluded(self):
    """Makes sure excluded files are actually excluded."""
    links = lm.get_links(self.data_path, excluded_files=['index.md'])
    one_md = pathlib.Path(os.path.join(self.data_path, 'linkedto1.md'))
    two_md = pathlib.Path(
        os.path.join(self.data_path, 'subdir', 'linkedto2.md')
    )
    expected_links = {
        one_md: [],
        two_md: [one_md],
    }
    self.assertSetEqual(
        set(expected_links.keys()),
        set(links.keys()),
        'Did not find expected markdown files',
    )
    self.assertDictEqual(
        expected_links,
        links,
        'Did not find links in markdown files'
    )
