﻿import os
import sys
import zipfile
import getpass
import subprocess
import shutil
import textwrap
import pathlib
import socket
import re
import collections

#Проверка зависимостей
missing = []
try:
    import yaml
except ImportError:
    missing.append("pyyaml")
try:
    import paramiko
except ImportError:
    missing.append("paramiko")
try:
    from tqdm import tqdm
except ImportError:
    missing.append("tqdm")

if missing:
    print("[ОШИБКА] Не найдены библиотеки: " + ", ".join(missing))
    print("Установите зависимости командой:\n\npip install -r requirements.txt\n")
    sys.exit(1)

#Вспомогательные функции
def validate_ascii(s):
    try:
        s.encode("utf-8")
        return all(ord(c) < 128 for c in s)
    except UnicodeEncodeError:
        return False

def load_servers(filepath):
    with open(filepath, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if "servers" not in data:
        print("В файле нет ключа 'servers'")
        sys.exit(1)
    return data['servers']

def exec_sudo_cmd(client, cmd, password):
    stdin, stdout, stderr = client.exec_command(f"sudo -S -p '' {cmd}", get_pty=True)
    stdin.write(password + '\n')
    stdin.flush()
    return stdout.channel.recv_exit_status()

#Генерация CSR
def generate_csr_on_app1(cluster, username, password):
    for name, app in cluster.items():
        if name != "app1":
            continue

        print("\n" + "-" * 60)
        hostname = app['hostname']
        ip = app['ip']
        port = 22

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=ip, port=port, username=username, password=password, timeout=10)
        except Exception as e:
            print(f"[ОШИБКА] Не удалось подключиться к APP1 ({hostname}) → {e}")
            continue

        def run_sudo_command(cmd):
            stdin, stdout, stderr = client.exec_command(f"sudo -S -p '' {cmd}", get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
            return stdout.channel.recv_exit_status()

        stdin, stdout, stderr = client.exec_command("hostname")
        shortname = stdout.read().decode().strip()

        print(f"[i] Генерация CSR для: {shortname}")

        run_sudo_command("sudo mkdir -p /root/keys")
        run_sudo_command("[ -f /root/keys/openssl_srv.cnf ] || echo '[ req ]\\nprompt = no\\ndistinguished_name = dn\\n[ dn ]\\nCN = example.com' | sudo tee /root/keys/openssl_srv.cnf > /dev/null")
        run_sudo_command("[ -f /root/keys/private.key ] || sudo openssl genrsa -out /root/keys/private.key 2048")

        commands = [
            f"sudo openssl req -new -config /root/keys/openssl_srv.cnf -key /root/keys/private.key -out /root/keys/s{shortname}.ru.csr",
            f"sudo zip /root/keys/dns_{shortname}.zip /root/keys/s{shortname}.ru.csr /root/keys/openssl_srv.cnf",
            f"sudo cp /root/keys/dns_{shortname}.zip /tmp/dns_{shortname}.zip",
            f"sudo chmod 644 /tmp/dns_{shortname}.zip"
        ]

        for cmd in commands:
            result = run_sudo_command(cmd)
            if result == 0:
                print(f"[+] Выполнено: {cmd}")
            else:
                print(f"[!] Ошибка при выполнении: {cmd}")
                print(f"[!] Прерывание генерации для сервера {shortname}.")
                client.close()
                break
        else:
            local_ca_dir = pathlib.Path("CA")
            local_ca_dir.mkdir(exist_ok=True)

            sftp = client.open_sftp()
            remote_path = f"/tmp/dns_{shortname}.zip"
            local_path = str(local_ca_dir / f"dns_{shortname}.zip")
            try:
                sftp.get(remote_path, local_path)
                print(f"[✓] Архив скачан в: {local_path}")
            except Exception as e:
                print(f"[ОШИБКА] Не удалось скачать архив: {e}")
            finally:
                sftp.close()
                client.close()

#SSH логин и кластер
def check_ssh_login(ip, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, port=port, username=username, password=password, timeout=10)
        client.close()
        return True
    except Exception:
        return False

def get_hostname(ip, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, port=port, username=username, password=password, timeout=10)
    stdin, stdout, stderr = client.exec_command("hostname -f")
    output = stdout.read().decode(errors="ignore").strip()
    client.close()
    return output

def find_all_app(app1_name, username, password, port=22, max_apps=5):
    cluster = {}
    unreachable_nodes = []

    def connect_and_get_ip(hostname):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, port=port, username=username, password=password, timeout=5)
        stdin, stdout, stderr = client.exec_command("hostname -I")
        ip = stdout.read().decode().strip().split()[0]
        client.close()
        return ip

    base = app1_name.replace('app1', 'app{}') if 'app1' in app1_name else None

    for i in range(1, max_apps + 1):
        role = f'app{i}'
        if i == 1:
            hostname_try = app1_name
        elif base:
            hostname_try = base.format(i)
        else:
            break

        try:
            ip = connect_and_get_ip(hostname_try)
            cluster[role] = {'hostname': hostname_try, 'ip': ip}
        except socket.gaierror:
            break
        except paramiko.AuthenticationException:
            unreachable_nodes.append((role, hostname_try, "Authentication failed."))
        except Exception as e:
            unreachable_nodes.append((role, hostname_try, str(e)))

    return cluster, unreachable_nodes

#Применение сертификата
def apply_signed_certificate(cluster, username, password):
    for name, app in cluster.items():
        if name != "app1":
            continue

        print("\n" + "-" * 60)
        hostname = app['hostname']
        ip = app['ip']

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=ip, username=username, password=password, timeout=10)
        except Exception as e:
            print(f"[ОШИБКА] Не удалось подключиться к APP1 ({hostname}) → {e}")
            continue

        sftp = client.open_sftp()
        stdin, stdout, stderr = client.exec_command("hostname")
        shortname = stdout.read().decode().strip()

        csr_file = pathlib.Path(f"./cer/s{shortname}.ru.csr")
        if not csr_file.exists():
            print(f"[ОШИБКА] Не найден файл сертификата: {csr_file}")
            client.close()
            continue

        try:
            sftp.put(str(csr_file), f"/root/keys/s{shortname}.ru.csr")
            print(f"[+] Отправлен: s{shortname}.ru.csr")
        except Exception as e:
            print(f"[ОШИБКА] Не удалось загрузить сертификат: {e}")
            client.close()
            continue

        commands = [
            "cd /root/keys",
            "wget -c http://ca.corp.tander.ru/pki/CA.zip",
            "unzip -o ./CA.zip",
            "openssl x509 -inform der -in ./CA/TanderRootCA.crt -out ./TanderRootCA.pem",
            "rm -f /root/keys/bundle.pem",
            f"cat ./s{shortname}.ru.csr >> ./bundle.pem && cat CA/TanderCorpCA.crt >> ./bundle.pem && cat ./TanderRootCA.pem >> ./bundle.pem",
            f"cp ./bundle.pem /etc/nginx/conf.d/ssl/ && cp ./s{shortname}.ru.csr /etc/nginx/conf.d/ssl/cert.pem && cp ./private.key /etc/nginx/conf.d/ssl/",
            "ls -ltr /etc/nginx/conf.d/ssl/",
            "nginx -t"
        ]

        success = True
        for cmd in commands:
            exit_code = exec_sudo_cmd(client, cmd, password)
            if exit_code != 0:
                print(f"[!] Ошибка при выполнении: {cmd}")
                success = False
                break
            else:
                print(f"[+] Выполнено: {cmd}")

        if success:
            print("[✓] Конфигурация nginx проверена. Применяем изменения...")
            reload_code = exec_sudo_cmd(client, "nginx -s reload", password)
            if reload_code == 0:
                print("[✓] Nginx перезапущен успешно.")
                print("[!] Проверьте, что сертификат подхватился через браузер из АРМ РЦ.")
            else:
                print("[ОШИБКА] Не удалось перезапустить nginx.")

        client.close()

        for node_name, node_data in cluster.items():
            if node_name == "app1":
                continue

            print("\n" + f"[→] Копируем сертификаты на {node_name} ({node_data['hostname']})")
            ip2 = node_data['ip']
            try:
                c2 = paramiko.SSHClient()
                c2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                c2.connect(hostname=ip2, username=username, password=password, timeout=10)
                sftp2 = c2.open_sftp()
                sftp2.put(str(csr_file), f"/root/keys/s{shortname}.ru.csr")
                sftp2.put("/etc/nginx/conf.d/ssl/bundle.pem", "/root/keys/bundle.pem")
                sftp2.put("/etc/nginx/conf.d/ssl/private.key", "/root/keys/private.key")
                print("[+] Сертификаты отправлены")

                cmds2 = [
                    "cp /root/keys/bundle.pem /etc/nginx/conf.d/ssl/",
                    f"cp /root/keys/s{shortname}.ru.csr /etc/nginx/conf.d/ssl/cert.pem",
                    "cp /root/keys/private.key /etc/nginx/conf.d/ssl/",
                    "ls -ltr /etc/nginx/conf.d/ssl/",
                    "nginx -t"
                ]

                ok = True
                for c in cmds2:
                    if exec_sudo_cmd(c2, c, password) != 0:
                        print(f"[!] Ошибка: {c}")
                        ok = False
                        break
                if ok:
                    exec_sudo_cmd(c2, "nginx -s reload", password)
                    print(f"[✓] Nginx на {node_name} успешно перезапущен")
                sftp2.close()
                c2.close()
            except Exception as e:
                print(f"[ОШИБКА] Не удалось скопировать на {node_name} → {e}")

#Меню и main
def menu():
    print("""
Выберите действие:
1. Сгенерировать файл запроса сертификата
2. Применить подписанный сертификат""")
    choise = input()
    return choise.strip()

def main():
    import signal
    from tqdm import tqdm

    def handle_exit(signum, frame):
        print("\n[!] Завершение по Ctrl+C")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)

    servers = load_servers("./servers/servers.yaml")
    print(f"Сервера загружены: {servers}")

    first_ip, first_port = servers[0].strip().split()
    while True:
        username = input("Введите логин для SSH:")
        password = getpass.getpass("Введите пароль для SSH:")

        if not validate_ascii(username) or not validate_ascii(password):
            print("[Ошибка] Логин или пароль содержат недопустимые символы. Допустимы только латинские буквы и цифры.\n")
            continue

        if check_ssh_login(first_ip, int(first_port), username, password):
            break

        print("Неверный логин или пароль. Попробуйте ещё раз.\n")

    unreachable = []
    auth_failed_nodes = []
    all_clusters = []

    print("\n[⏳] Поиск кластеров и хостов...")
    progress = tqdm(servers, desc="Обработка серверов")
    for line in progress:
        ip, port = line.strip().split()
        try:
            hostname = get_hostname(ip, int(port), username, password)
            tqdm.write("\n" + "-" * 60)
            tqdm.write(f"[+] Получено имя: {hostname} от {ip}")
            app1_name = hostname.split('.')[0]
            cluster, cluster_errors = find_all_app(app1_name, username, password, int(port))

            tqdm.write("=== Обнаруженный кластер ===")
            for role, info in cluster.items():
                tqdm.write(f"{role}: {info['hostname']} ({info['ip']})")
            for role, host, reason in cluster_errors:
                tqdm.write(f"[!] {role}: {host} — ошибка подключения: {reason}")
                if reason == "Authentication failed.":
                    auth_failed_nodes.append(f"{role}: {host}")

            all_clusters.append(cluster)
        except Exception as e:
            tqdm.write("\n" + "-" * 60)
            tqdm.write(f"[Ошибка] Не удалось подключиться к {ip}:{port} — {e}")
            unreachable.append(ip)

    if unreachable or auth_failed_nodes:
        print(f"\n[!] Не удалось подключиться к {len(unreachable) + len(auth_failed_nodes)} узлам:")
        for ip in unreachable:
            print(f" - {ip}")
        for node in auth_failed_nodes:
            print(f" - {node}")
    else:
        print("\n[✓] Все серверы доступны.")

    choise = menu()
    if choise == "1":
        for cluster in all_clusters:
            generate_csr_on_app1(cluster, username, password)
    elif choise == "2":
        for cluster in all_clusters:
            apply_signed_certificate(cluster, username, password)
    else:
        print("Неверная цифра")

if __name__ == "__main__":
    main()