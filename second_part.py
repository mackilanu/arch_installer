import os

os.system('ln -sf /usr/share/zoneinfo/Europe/Stockholm /etc/localtime')
os.system('hwclock --systohc')
os.system('rm /etc/locale.gen')

os.system("curl -L 172.104.240.145/locale.html > /etc/locale.gen")
os.system('locale-gen')

hostname = input('Enter your desired hostname: ')

os.system(f"printf '{hostname}' > /etc/hostname")

hosts = """127.0.0.1 localhost
::1 localhost
127.0.1.1 {0}.localdomain {0}""".format(hostname)

reflector = """--save /etc/pacman.d/mirrorlist
--protocol https
--country Sweden,Norway
--latest 5
--sort age
"""

os.system(f"printf \"{reflector}\" > /etc/xdg/reflector/reflector.conf")

os.system(f"printf \"{hosts}\" > /etc/hosts")
os.system("curl -L 172.104.240.145/sudoers.html > /etc/sudoers")

username = input('Enter desired username: ')
os.system(f'useradd -mG wheel {username}')

print('Enter password below')
os.system(f'passwd {username}')

print('Enter root below')
os.system('passwd')

de = input('Please enter desired DE(gnome/kde): ')

if de == 'gnome':
    os.system('pacman -S gnome gdm')
    os.system('systemctl enable gdm')
if de == 'kde':
    os.system('pacman -S plasma kde-applications sddm')
    os.system('systemctl enable sddm')

cpu = input('Do you have an amd or intel CPU? (amd/intel): ')

os.system(f"pacman -S {cpu}-ucode")

aur_helper = input('Do you want to install an AUR helper(paru)? (Y/n): ')
if aur_helper.lower() != 'n':
    os.system(f"su {username}")
    os.system('git clone https://aur.archlinux.org/paru.git')
    os.system('cd paru && makepkg -si')
    os.system('su')

os.system('grub-install --target=x86_64-efi --efi-directory=/EFI --bootloader-id=GRUB')

os.system('grub-mkconfig -o /boot/grub/grub.cfg')

os.system('systemctl enable NetworkManager reflector')

print('The installation script has finished! Enjoy your new system :)')
