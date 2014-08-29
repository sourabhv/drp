Drop_Boxer
==========

Drop_Boxer is a command line tool for Dropbox to ease upload, download of files and get public URLs.

Requirements
------------

- Python (Duh!)
- [Dropbox Python SDK](https://www.dropbox.com/developers/core/sdks/python)

Possible Commands
-----------------

- `drop_boxer up source_file [dest_path]`: Upload *source_file* to App's root/*dest_path*
- `drop_boxer ls [path]`: List all files/folders in root/given *path*
- `drop_boxer tree [path]`: Show the file tree structure of root/given *path*
- `drop_boxer down source_file_path [dest_path]`: Download the *source_file_path* into current directory or *dest_path*
- `dropboxer share source_file_path`: Copy the public URL of *source_file_path* in clipboard
