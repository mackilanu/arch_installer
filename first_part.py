import os

os.system('loadlkeys sv-latin1')

skip_part = input('Skip partitioning? (y/N): ')

if skip_part.lower() != 'y':
    os.system('fdisk -l')
    disk = input('Pick a disk to install on: ')

    ans = input('This disk will be wiped, please backup your data before proceeding. Continue? (Y/n)')
    if ans == 'n':
        exit()

    ans_swap = input('Do you want a swap partition? (y/N): ')

    os.system('wipefs -a -p ' + disk)
    os.system(f'parted {disk} --script mklabel gpt')
    os.system(f'parted {disk} --script mkpart primary fat32 0% 513MiB')
    ans_swap_size = ""
    if ans_swap.lower() == 'y':
        ans_swap_size = input("How big of a swap partition do you want? (in mb)")
        os.system(f'parted {disk} --script mkpart primary linux-swap 513MiB {ans_swap_size}MiB')
    os.system(f'parted {disk} --script set 1 esp on')
    os.system(f'parted {disk} --script mkpart primary ext4 {int(ans_swap_size) + 513}MiB 100%')

    if 'nvme' in disk:
        disk = disk + 'p'

    ext4_part_num = ""
    if ans_swap.lower() == 'y':
        ext4_part_num = '3'
    else:
        ext4_part_num = '2'

    os.system(f'mkfs.fat -F 32 {disk}1')
    os.system(f'mkfs.ext4 {disk}{ext4_part_num}')
    if ans_swap.lower() == 'y':
        os.system(f"mkswap {disk}2")
        os.system(f"swapon {disk}2")

    os.system(f'mount {disk}{ext4_part_num} /mnt')
    os.system(f'mkdir /mnt/EFI')
    os.system(f'mount {disk}1 /mnt/EFI')

os.system('pacstrap /mnt base linux linux-firmware base-devel vim git python grub efibootmgr reflector curl')
os.system('genfstab -U /mnt >> /mnt/etc/fstab')
os.system('curl -L 172.104.240.145/second.html > /mnt/installer')
os.system('arch-chroot /mnt && python installer')
