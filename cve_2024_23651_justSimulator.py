import os
import threading
import time
import hashlib
import datetime

# 바인드 마운트된 호스트 파일 경로
HOST_TARGET_PATH = "/hostroot/etc/passwd"

# BuildKit 캐시 공유 디렉터리 (컨테이너 생성 시 volume으로 연결되어야 함)
CACHE_MOUNT_PATH = "/mnt/cache"

# 로그 경로
LOG_PATH = "/logs/detected.txt"

# 민감 파일 접근 시도
def try_access_host_file():
    timestamp = datetime.datetime.now().isoformat()
    try:
        with open(HOST_TARGET_PATH, 'r') as f:
            content = f.read()
            checksum = hashlib.sha256(content.encode()).hexdigest()
            msg = f"[{timestamp}] [!] 호스트 파일 접근 성공 - SHA256: {checksum}"
    except Exception as e:
        msg = f"[{timestamp}] [x] 호스트 파일 접근 실패 - 이유: {e}"
    print(msg)
    with open(LOG_PATH, "a") as log:
        log.write(msg + "\n")

# BuildKit 캐시 디렉터리에 대량 쓰기 시도 (Race Condition 유발)
def race_writer(thread_id):
    for i in range(50):
        try:
            with open(f"{CACHE_MOUNT_PATH}/temp_{thread_id}_{i}.txt", 'w') as f:
                f.write(f"Thread {thread_id}, iteration {i}\n")
            time.sleep(0.01)
        except Exception as e:
            print(f"[x] 쓰기 에러 in Thread {thread_id}: {e}")

# Race Condition 시뮬레이션 시작
def start_race_condition_simulation():
    print("[*] Race Condition 시뮬레이션 시작")
    threads = []

    for i in range(10):  # 캐시 디렉터리 접근 쓰레드
        t = threading.Thread(target=race_writer, args=(i,))
        threads.append(t)
        t.start()

    for i in range(3):  # 민감 파일 접근 시도 쓰레드
        t = threading.Thread(target=try_access_host_file)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("[*] 시뮬레이션 완료")

if __name__ == "__main__":
    start_race_condition_simulation()
