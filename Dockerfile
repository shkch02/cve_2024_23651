FROM python:3.10-slim

LABEL maintainer="yourname"
LABEL description="BuildKit CVE-2024-23651 Race Condition 탐지 컨테이너"

WORKDIR /app

# 로그 디렉토리 생성
RUN mkdir /logs

# Python 탐지 코드 복사
COPY cve_2024_23651_justSimulator.py .

# 실행
CMD ["python", "cve_2024_23651_exploit_simulator.py"]
