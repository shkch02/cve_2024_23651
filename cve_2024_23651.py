# -*- coding: utf-8 -*-
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
            print(f"[*] BuildKit version detected: {version}")
            return version
        else:
            print("[x] can't detected version info")
            return None
    except FileNotFoundError:
        print("[x] can't find buildkitd command. check the install")
        return None

def is_vulnerable(version_tuple):
    if version_tuple is None:
        return False
    # weakness version < 0.12.5
    return version_tuple < (0, 12, 5)

if __name__ == "__main__":
    version = get_buildkit_version()
    if is_vulnerable(version):
        print("[!] detected weakness buildkit version, operate the test.\n")
        # race condition test
        import cve_2024_23651_detector  
    else:
        print("[*] safe BuildKit version.")

