# SecureKit — Python Secure Coding Skeleton

Ringkasan
- Skeleton project untuk latihan Python lanjutan dan pola secure coding (Minggu 1-2).
- Berisi: utilities aman, HTTP client (sync & async) dengan pola dependency injection, pydantic config, unit tests, dan CI workflow.

Tujuan
- Praktik safe subprocess, temporary env context, validated input decorator.
- Implementasi HTTP client yang aman (TLS verify, timeouts, retries) dengan testable API.
- CI: formatting, linting, typing, unit tests, and security scans.

Quick start
1. Buat virtualenv dan aktifkan:
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\Activate   # Windows

2. Install dependencies:
   pip install -r requirements-dev.txt

3. Jalankan format/lint/test:
   black .
   flake8
   mypy src
   pytest -q

4. Jalankan security scans (opsional):
   bandit -r src
   pip-audit

Struktur penting
- src/securekit: package utama
  - utils.py: safe subprocess, temp_env, decorators
  - http_client.py: sync/async HTTP client with DI
  - config.py: pydantic settings model
- tests/: pytest tests
- .github/workflows/ci.yml: CI workflow
- requirements-dev.txt: dev dependencies

Catatan keamanan & etika
- Jangan memasukkan secrets di repo. Gunakan env vars / secret store.
- Semua contoh network di sini menggunakan dependency injection / mock transport untuk testing — tidak mengakses jaringan nyata saat test berjalan.

Selamat belajar — mulai dari mengulas file `src/securekit/*` dan jalankan `pytest` untuk melihat contoh tests berjalan.
