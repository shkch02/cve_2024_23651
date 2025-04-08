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
            print(f"[*] BuildKit ���� ������: {version}")
            return version
        else:
            print("[x] ���� ������ ã�� �� ����")
            return None
    except FileNotFoundError:
        print("[x] buildkitd ��ɾ ã�� �� �����ϴ�. ��ġ ���θ� Ȯ���ϼ���.")
        return None

def is_vulnerable(version_tuple):
    if version_tuple is None:
        return False
    # ����� ����: 0.12.5 �̸�
    return version_tuple < (0, 12, 5)

if __name__ == "__main__":
    version = get_buildkit_version()
    if is_vulnerable(version):
        print("[!] ����� BuildKit ������ �����Ǿ����ϴ�. ������ �����մϴ�.\n")
        # ���⼭ ���̽� ����� Ž�� ������ �ҷ����ų� ����
        import cve_2024_23651_detector  # detector.py�� race condition ���� �ڵ� �ۼ��صα�
    else:
        print("[*] ������ BuildKit �����Դϴ�. ������ �ߴ��մϴ�.")

