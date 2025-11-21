#!/bin/bash
# Script untuk memeriksa indentasi dan syntax error Python
# Usage: bash .python-lint-check.sh

echo "🔍 Memeriksa indentasi dan syntax error pada file Python..."

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERROR_COUNT=0

# Fungsi untuk memeriksa file Python
check_python_file() {
    local file=$1
    
    # Cek syntax error
    python3 -m py_compile "$file" 2>&1 | while IFS= read -r line; do
        if [[ $line == *"IndentationError"* ]] || [[ $line == *"SyntaxError"* ]]; then
            echo -e "${RED}❌ ERROR:${NC} $file"
            echo -e "${RED}   $line${NC}"
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    done
    
    # Cek indentasi dengan Python
    python3 << EOF
import ast
import sys

try:
    with open("$file", "r", encoding="utf-8") as f:
        code = f.read()
    ast.parse(code)
except IndentationError as e:
    print(f"${RED}❌ IndentationError in $file:${NC}")
    print(f"${RED}   Line {e.lineno}: {e.msg}${NC}")
    sys.exit(1)
except SyntaxError as e:
    print(f"${RED}❌ SyntaxError in $file:${NC}")
    print(f"${RED}   Line {e.lineno}: {e.msg}${NC}")
    sys.exit(1)
EOF
}

# Cari semua file Python (kecuali di venv dan migrations)
find . -type f -name "*.py" \
    ! -path "./venv/*" \
    ! -path "./.venv/*" \
    ! -path "./__pycache__/*" \
    ! -path "./*/migrations/*" \
    | while read -r file; do
    check_python_file "$file"
done

if [ $ERROR_COUNT -eq 0 ]; then
    echo -e "${GREEN}✅ Semua file Python tidak memiliki error indentasi!${NC}"
    exit 0
else
    echo -e "${RED}❌ Ditemukan $ERROR_COUNT error indentasi!${NC}"
    exit 1
fi

