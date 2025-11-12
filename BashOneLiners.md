# Dry run for files (finds all .rar, .r00, .nfo, .sfv, etc.)

find . -type f ! -name "\*.avi"

# Dry run for the 'Sample' directories

find . -type d -name "Sample"

# Delete all non AVI files (replace with whatever extension the video is in)

# WARNING MUST run in directory with TV show or will delete all videos

find . -type f ! -name "\*.avi" -delete

# Unrar all files in directories recursively

find . -type f -name "\*.rar" -execdir unrar e {} \;
