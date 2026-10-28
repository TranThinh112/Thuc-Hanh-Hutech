# Thư Mục: system_tests

Thư mục tập hợp các kịch bản kiểm thử tích hợp (Integration Tests) và API endpoint testing:
- Chạy với PYTHONPATH trỏ về thư mục gốc đồ án:
  `powershell
  $env:PYTHONPATH = "."
  python system_tests/test_fastapi.py
  python system_tests/test_all_scenarios.py
  `
- Chạy Unit test cốt lõi: `python -m pytest python_app/tests`