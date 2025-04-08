import subprocess
import re
import sys

def get_buildkit_version():
    try:
        result = subprocess.run(["buildkitd", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip()
        match = re.search(r'v?(\d+)\.(\d+)\.(\d+)', output)
        if match:
            version = tuple(map(int, match.groups()))
            print(f"[*] BuildKit 버전 감지됨: {version}")
            return version
        else:
            print("[x] 버전 정보를 찾을 수 없음")
            return None
    except FileNotFoundError:
        print("[x] buildkitd 명령어를 찾을 수 없습니다. 설치 여부를 확인하세요.")
        return None

def is_vulnerable(version_tuple):
    if version_tuple is None:
        return False
    # 취약한 버전: 0.12.5 미만
    return version_tuple < (0, 12, 5)

if __name__ == "__main__":
    version = get_buildkit_version()
    if is_vulnerable(version):
        print("[!] 취약한 BuildKit 버전이 감지되었습니다. 실험을 진행합니다.\n")
        # 여기서 레이스 컨디션 탐지 로직을 불러오거나 실행
        import cve_2024_23651_detector  # detector.py에 race condition 실험 코드 작성해두기
    else:
        print("[*] 안전한 BuildKit 버전입니다. 실험을 중단합니다.")

