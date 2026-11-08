#!/usr/bin/env bash
# Đối chứng ĐỘC LẬP bằng openssl (không dùng code CertGuard).
# Mục đích: chứng minh với giảng viên rằng lỗi nằm thật trên máy chủ,
# và CertGuard phát hiện đúng — kết quả hai bên phải trùng nhau.
#
# Chạy: bash verify_servers.sh

ROOT=certs/ca/root.pem
declare -A PORTS=( [good]=8443 [expiring]=8444 [expired]=8445 [selfsigned]=8446 \
                   [wronghost]=8447 [incomplete]=8448 [weak]=8449 )

for name in good expiring expired selfsigned wronghost incomplete weak; do
  port=${PORTS[$name]}
  host="$name.certguard.webservers"
  echo "================ $host (cổng $port) ================"
  out=$(echo | openssl s_client -connect 127.0.0.1:$port -servername "$host" \
        -verify_hostname "$host" -CAfile "$ROOT" -showcerts 2>&1)
  echo "$out" | grep -E "Verify return code" | tail -1
  echo "$out" | openssl x509 -noout -subject -issuer -enddate 2>/dev/null
  echo "$out" | grep -c "BEGIN CERTIFICATE" | xargs echo "Số chứng thư máy chủ gửi:"
  echo "$out" | openssl x509 -noout -text 2>/dev/null | grep "Public-Key"
  for proto in tls1 tls1_1; do
    if echo | openssl s_client -connect 127.0.0.1:$port -$proto -cipher 'DEFAULT:@SECLEVEL=0' >/dev/null 2>&1; then
      echo "CẢNH BÁO: chấp nhận $proto"
    fi
  done
  curl -sk -o /dev/null -D - "https://127.0.0.1:$port" | grep -i strict-transport \
    || echo "Không có HSTS"
  echo
done
