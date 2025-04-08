# Dockerfile
FROM python:3.10-slim

LABEL maintainer="YourName"
LABEL description="BuildKit CVE-2024-23651 Race Condition 탐지 컨테이너"

WORKDIR /app

# 로그 디렉토리 생성
RUN mkdir /logs

# 탐지 스크립트 복사
COPY cve_2024_23651_detecter.py .

# 실행 명령어
CMD ["python", "cve_2024_23651_detecter.py"]
