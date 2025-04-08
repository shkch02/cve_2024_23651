FROM python:3.10-slim

LABEL maintainer="YourName"
LABEL description="BuildKit CVE-2024-23651 탐지 및 실험 컨테이너"

# 작업 디렉토리
WORKDIR /app

# 로그 디렉토리 생성
RUN mkdir /logs

# 탐지 스크립트 복사
COPY cve_2024_23651_detecter.py .
COPY cve_2024_23651.py .

# CMD에서 버전 확인 → 취약 시 실험 코드 실행
CMD ["python", "cve_2024_23651.py"]
