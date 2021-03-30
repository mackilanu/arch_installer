import os

os.system('loadlkeys sv-latin1')
os.system('timedatectl set-ntp true')

os.system('fdisk -l')
disk = input('Pick a disk to install on:')

ans = input('This disk will be wiped, please backup your data before proceeding. Continue? (Y/n)')
if ans == 'n':
    exit()

os.system('wipefs -a -p /dev/' + disk)
os.system(f'parted /dev/{disk} --script mklabel gpt')
os.system(f'parted /dev/{disk} --script mkpart primary fat32 0% 513MiB')
os.system(f'parted /dev/{disk} --script set 1 esp on')
os.system(f'parted /dev/{disk} --script mkpart primary ext4 513MiB 100%')

if disk.startswith('nvme'):
    disk = disk + 'p'

os.system(f'mkfs.fat -F 32 /dev/{disk}1')
os.system(f'mkfs.ext4 /dev/{disk}2')

os.system(f'mount /dev/{disk}2 /mnt')
os.system(f'mkdir /mnt/EFI')
os.system('mount /dev/{disk}1 /mnt/EFI')

os.system('pacstrap /mnt base linux linux-firmware base-devel vim git')
os.system('genfstab -U /mnt >> /mnt/etc/fstab')