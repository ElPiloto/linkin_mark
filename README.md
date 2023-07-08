# linkin_mark

Creates a list of links in markdown files.  This can be used for downstream
purposes such as visualization.

# Usage

### Absolute Paths
```
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
```

### Relative Paths
```
  links = lm.get_relative_links('/path/to/dir/of/md/files/')
  >>> {
          PosixPath('index.md'): 
              [PosixPath('linkedto1.md'),
               PosixPath('subdir/linkedto2.md')],
          PosixPath('linkedto1.md'): [],
          PosixPath('subdir/linkedto2.md'): 
              [PosixPath('index.md'),
               PosixPath('linkedto1.md')],
       }
```


### Exclude markdown files
```
  links = lm.get_relative_links('/path/to/dir/of/md/files/', excluded_files=['index.md'])
  >>> {
          PosixPath('linkedto1.md'): [],
          PosixPath('subdir/linkedto2.md'): [PosixPath('linkedto1.md')],
      }
```

### Visualization using networkx and matplotlib
```
import matplotlib.pyplot as plt
import networkx as nx
links = lm.get_relative_links('/path/to/dir/of/md/files/')
g = nx.from_dict_of_lists(links, nx.DiGraph)  # alternatively: nx.DiGraph(links)
nx.draw_networkx(g, arrows=True)
plt.show()

```
![Example Graph](https://github.com/ElPiloto/linkin_mark/assets/629190/cdcb9254-4c09-4a1a-86d3-0deeec152129)



