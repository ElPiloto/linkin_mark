# linkin_mark

Makes a graph of links in a set of markdown files.


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
```


### Exclude markdown files
```
  links = lm.get_relativized_links('/path/to/dir/of/md/files/',
                                   excluded_files=['index.md'])
  >>> {
          PosixPath('linkedto1.md'): [],
          PosixPath('subdir/linkedto2.md'): [PosixPath('linkedto1.md')],
       }
```
