# Dry run for files (finds all .rar, .r00, .nfo, .sfv, etc.)

find . -type f ! -name "\*.avi"

# Dry run for the 'Sample' directories

find . -type d -name "Sample"

# Unrar all files in directories recursively

find . -type f -name "\*.rar" -execdir unrar e {} \;
