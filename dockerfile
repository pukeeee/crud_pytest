FROM python:3.12-slim

WORKDIR /crud_pytest

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "tests/"]