# 🔍 SAST Tool - Static Application Security Testing cho Python

Công cụ phân tích mã nguồn tĩnh (SAST) tự động kiểm tra cú pháp AST, mẫu regex độc hại, đánh giá độ tuân thủ chuẩn PEP 8 và xuất báo cáo chuẩn quốc tế **SARIF 2.1.0** (Static Analysis Results Interchange Format) để tích hợp vào CI/CD hoặc xem trực tiếp qua SARIF Viewer trên VS Code.

---

## 📌 Các Tính Năng Chính

1. **Phân tích Cú pháp Trừu tượng (AST Analysis):** Phân tích cây cú pháp của mã nguồn Python để phát hiện việc sử dụng các hàm nguy hiểm như val(), xec(), input() không an toàn.
2. **Kiểm tra Mẫu Biểu thức Chính quy (Regex Vulnerability Matching):** Quét các mẫu mật khẩu cứng (hardcoded password), secret key, token nhạy cảm, sử dụng pickle.loads() không an toàn.
3. **Đánh giá Chuẩn Mã nguồn (Linting & Code Quality):** Tích hợp lake8 kiểm tra các lỗi cú pháp nghiêm trọng và chuẩn PEP 8.
4. **Quy tắc Bảo mật Tùy biến (Security Rule Engine):** Phân loại và gán mức độ nghiêm trọng (High, Medium, Low) dựa trên cấu hình ules/default_rules.json.
5. **Báo cáo chuẩn Quốc tế SARIF v2.1.0:** Tự động tạo file eport.sarif để tương thích hoàn toàn với GitHub Advanced Security và VS Code SARIF Viewer extension.

---

## 📁 Cấu Trúc Thư Mục

`	ext
sast-tool/
├── examples/
│   ├── vulnerable_01.py        # Code mẫu thử nghiệm chứa eval, hardcoded password, pickle
│   └── vulnerable_02.py        # Code mẫu kiểm thử hàm eval với dữ liệu người dùng
├── rules/
│   └── default_rules.json      # Quy tắc phân loại mức độ rủi ro và mô tả lỗ hổng
├── sast_tool/
│   ├── __init__.py
│   ├── ast_analyzer.py         # Module phân tích AST
│   ├── code_quality_checker.py # Module tích hợp flake8
│   ├── vuln_pattern_matcher.py # Module quét regex mẫu lỗ hổng
│   ├── security_rule_engine.py # Động cơ liên kết kết quả với rules
│   ├── sarif_reporter.py       # Module sinh báo cáo SARIF v2.1.0
│   └── main.py                 # CLI entrypoint
├── tests/
│   ├── test_ast_analyzer.py
│   ├── test_code_quality_checker.py
│   ├── test_sarif_reporter.py
│   ├── test_security_rule_engine.py
│   └── test_vuln_pattern_matcher.py
├── report.sarif                # Báo cáo kết quả quét mẫu SARIF
├── requirements.txt            # Thư viện phụ thuộc: flake8, sarif-om, jsonpickle
└── README.md
`

---

## 🚀 Hướng Dẫn Cài Đặt & Sử Dụng

### 1. Cài đặt thư viện phụ thuộc

`ash
cd sast-tool
pip install -r requirements.txt
`

### 2. Chạy bộ kiểm thử tự động (Unit Tests)

`ash
python -m unittest discover tests
`
*Kết quả:* Chạy thành công toàn bộ 6/6 test cases.

### 3. Thực thi quét mã nguồn bằng CLI

Quét file mẫu ulnerable_01.py:
`ash
python -m sast_tool.main examples/vulnerable_01.py
`

Quét file mẫu ulnerable_02.py:
`ash
python -m sast_tool.main examples/vulnerable_02.py
`

### 4. Xem kết quả báo cáo SARIF
File báo cáo eport.sarif sẽ được sinh ra ở thư mục hiện hành. Có thể cài đặt tiện ích mở rộng **SARIF Viewer** trong Visual Studio Code để xem kết quả quét dưới dạng bảng trực quan tương tác.
