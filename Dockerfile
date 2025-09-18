# Dockerfile
FROM python:3.11-slim

# 시스템 기본 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# (선택) 빌드가 필요한 휠 대비
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 의존성 먼저 설치 → 레이어 캐시 극대화
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스 복사
COPY app /app/app

EXPOSE 8000

# 기본 실행 커맨드 (개발/운영 공용)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
