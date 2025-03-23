sudo rm -rf /etc/pacman.d/gnupgp
sudo pacman-key --init
sudo pacman -Sy --needed archlinux-keyring
