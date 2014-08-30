Drop_Boxer
==========

Drop_Boxer is a command line tool for Dropbox to ease upload, download of files and get public URLs.

Installation
------------

```
$ wget http://goo.gl/yS0X9B
$ chmod +x main.py
```
Requirements
------------

- Python (Duh!)
- `pip install dropbox`
or [Dropbox Python SDK](https://www.dropbox.com/developers/core/sdks/python)


Command Usage
--------------

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
```

Todos
-----

* Store `access_token` in a local file.
* Add search function
* Extend with parallel uploads and downloads
* Use compression for file transfer (gzip)
* Set multi-threaded transfer for large uploads/downloads

License
-------

Drop_boxer is released under the MIT license.
