Drop_Boxer
==========

Drop_Boxer is a command line tool for Dropbox to ease upload, download of files and get public URLs.

Requirements
------------

- Python (Duh!)
 ```
 pip install dropbox
```
or direct download at [Dropbox Python SDK](https://www.dropbox.com/developers/core/sdks/python)


Command Usage
-----------------

```
$ drp                                    # show help
$ drp up file1 file2 -d [path]           # upload files
$ drp down file1 file2 -d [path]         # download files
$ drp ls [path]                          # list files
$ drp cd [path]                          # change current working directory
$ drp tree [path]                        # show file structure
$ drp mkdir folder                       # creae a new directory
$ drp rm file                            # delete file or directory
$ drp share file                         # copy public URL to clipboard
$ drp info file                          # retrieve metadata for file/folder

License
-------

Drop_boxer is released under the MIT license.
