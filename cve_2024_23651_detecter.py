import os
import threading
import time
import hashlib

HOST_TARGET_PATH = "/hostroot/etc/passwd"  # 백신 컨테이너에 호스트를 바인드 마운트 해둘 것
CACHE_MOUNT_PATH = "/mnt/cache"  # 공유 캐시 마운트 경로

def try_access_host_file():
    try:
        with open(HOST_TARGET_PATH, 'r') as f:
            content = f.read()
            checksum = hashlib.sha256(content.encode()).hexdigest()
            print(f"[!] 호스트 파일 접근 성공 - SHA256: {checksum}")
            os.makedirs("/logs", exist_ok=True)
            with open("/logs/detected.txt", "w") as log:
                log.write(f"[DETECTED] Host file accessed: {checksum}\n")
    except Exception as e:
        print(f"[x] 접근 실패: {e}")

def race_writer(thread_id):
    for i in range(50):
        try:
            with open(f"{CACHE_MOUNT_PATH}/temp_{thread_id}.txt", 'w') as f:
                f.write(f"Thread {thread_id}, iteration {i}\n")
            time.sleep(0.01)
        except Exception as e:
            print(f"[x] 쓰기 에러 in Thread {thread_id}: {e}")

def start_race_condition_simulation():
    threads = []
    for i in range(10):  # 10개의 쓰레드로 동시에 캐시마운트 접근
        t = threading.Thread(target=race_writer, args=(i,))
        threads.append(t)
        t.start()

    # 파일 접근 시도도 병렬로 진행
    for i in range(3):
        t = threading.Thread(target=try_access_host_file)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    print("[*] Race Condition 시뮬레이션 시작")
    start_race_condition_simulation()
    print("[*] 완료")
