# Nhập các dòng từ người dùng
print("Nhập văn bản (Nhập 'done' để kết thúc):")
lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line)
#chuyển in hoa
print("\nCác dòng đã nhập sau khi chuyển thành in hoa:")
for line in lines:
    print(line.upper())