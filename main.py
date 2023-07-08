import paramiko
from colorama import init, Fore, Style

def configure_vlan(hostname, username, password, vlan_id, vlan_interface, vlan_description):
    # Membuat objek SSHClient
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Melakukan koneksi SSH ke perangkat MikroTik
        ssh_client.connect(hostname, username=username, password=password)

        # Membuka channel SSH
        ssh_channel = ssh_client.invoke_shell()

        # Mengirim perintah untuk masuk ke mode konfigurasi
        ssh_channel.send("configure\r")

        # Menunggu respons dari perangkat
        while not ssh_channel.recv_ready():
            pass

        # Membaca respons dari perangkat
        output = ssh_channel.recv(1024).decode()

        # Mengirim perintah untuk membuat VLAN
        ssh_channel.send(f"/interface vlan add name=vlan{vlan_id} interface={vlan_interface} vlan-id={vlan_id} comment={vlan_description}\r")

        # Menunggu respons dari perangkat
        while not ssh_channel.recv_ready():
            pass

        # Membaca respons dari perangkat
        output = ssh_channel.recv(1024).decode()

        # Mengirim perintah untuk keluar dari mode konfigurasi
        ssh_channel.send("exit\r")

        # Menutup koneksi SSH
        ssh_client.close()

        print(Fore.GREEN + "Konfigurasi VLAN berhasil!" + Style.RESET_ALL)
    except paramiko.AuthenticationException:
        print(Fore.RED + "Gagal melakukan autentikasi. Periksa kembali username dan password." + Style.RESET_ALL)
    except paramiko.SSHException:
        print(Fore.RED + "Gagal melakukan koneksi SSH." + Style.RESET_ALL)
    except paramiko.socket.error as e:
        print(Fore.RED + f"Terjadi kesalahan: {e}" + Style.RESET_ALL)

def backup_configuration(hostname, username, password, backup_filename):
    # Membuat objek SSHClient
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Melakukan koneksi SSH ke perangkat MikroTik
        ssh_client.connect(hostname, username=username, password=password)

        # Membuka channel SSH
        ssh_channel = ssh_client.invoke_shell()

        # Mengirim perintah untuk mengekspor konfigurasi
        ssh_channel.send(f"/export file={backup_filename}\r")

        # Menunggu respons dari perangkat
        while not ssh_channel.recv_ready():
            pass

        # Membaca respons dari perangkat
        output = ssh_channel.recv(1024).decode()

        # Menutup koneksi SSH
        ssh_client.close()

        print(Fore.GREEN + f"Backup konfigurasi berhasil disimpan ke file: {backup_filename}" + Style.RESET_ALL)
    except paramiko.AuthenticationException:
        print(Fore.RED + "Gagal melakukan autentikasi. Periksa kembali username dan password." + Style.RESET_ALL)
    except paramiko.SSHException:
        print(Fore.RED + "Gagal melakukan koneksi SSH." + Style.RESET_ALL)
    except paramiko.socket.error as e:
        print(Fore.RED + f"Terjadi kesalahan: {e}" + Style.RESET_ALL)

# Memanggil fungsi untuk mengkonfigurasi VLAN
configure_vlan("alamat_ip_mikrotik", "username", "password", 10, "ether1", "VLAN 10")

# Memanggil fungsi untuk membuat backup konfigurasi
backup_configuration("alamat_ip_mikrotik", "username", "password", "backup_config.rsc")
      
