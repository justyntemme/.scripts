# docker
## Remove dangling images; skip the confirmation prompt
docker image prune -f
docker container prune
## Remove unused build cache older than seven days
docker builder prune -a -f --filter 'until=168h'

# Go
go clean -modcache
## compiled  build cache
go clean -cache
#homebrew
brew autoremove
brew cleanup --prune=all
# npm
npm cache clean --force
# python
python3 -m pip cache purge
