import os
import threading
import time
import hashlib

HOST_TARGET_PATH = "/hostroot/etc/passwd"  # ��� �����̳ʿ� ȣ��Ʈ�� ���ε� ����Ʈ �ص� ��
CACHE_MOUNT_PATH = "/mnt/cache"  # ���� ĳ�� ����Ʈ ���

def try_access_host_file():
    try:
        with open(HOST_TARGET_PATH, 'r') as f:
            content = f.read()
            checksum = hashlib.sha256(content.encode()).hexdigest()
            print(f"[!] ȣ��Ʈ ���� ���� ���� - SHA256: {checksum}")
            with open("/logs/detected.txt", "w") as log:
                log.write(f"[DETECTED] Host file accessed: {checksum}\n")
    except Exception as e:
        print(f"[x] ���� ����: {e}")

def race_writer(thread_id):
    for i in range(50):
        try:
            with open(f"{CACHE_MOUNT_PATH}/temp_{thread_id}.txt", 'w') as f:
                f.write(f"Thread {thread_id}, iteration {i}\n")
            time.sleep(0.01)
        except Exception as e:
            print(f"[x] ���� ���� in Thread {thread_id}: {e}")

def start_race_condition_simulation():
    threads = []
    for i in range(10):  # 10���� ������� ���ÿ� ĳ�ø���Ʈ ����
        t = threading.Thread(target=race_writer, args=(i,))
        threads.append(t)
        t.start()

    # ���� ���� �õ��� ���ķ� ����
    for i in range(3):
        t = threading.Thread(target=try_access_host_file)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    print("[*] Race Condition �ùķ��̼� ����")
    start_race_condition_simulation()
    print("[*] �Ϸ�")
