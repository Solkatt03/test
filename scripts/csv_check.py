import csv
from datetime import datetime
import os
import sys
import argparse
import glob

def validate_csv(csv_path, expected_headers, column_types, delimiter=',', quotechar='"', escapechar=None, doublequote:bool=True):
    if not os.path.exists(csv_path):
        return False, f"文件不存在: {csv_path}"

    if not csv_path.lower().endswith('.csv'):
        return False, f"文件不是csv格式: {os.path.basename(csv_path)}"

    try:
        with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar, escapechar=escapechar, doublequote=doublequote)
            headers = next(reader)
    except Exception as e:
        return False, f"读取csv文件失败: {str(e)}"

    # 表头验证
    headers = [h.strip() for h in headers]
    print(f"\n文件: {csv_path}")
    print("表头：", headers)
    if headers == expected_headers:
        print("表头一致")
    else:
        print("表头不一致")
        print("预期：", expected_headers)
        print("实际：", headers)
        return False, "表头验证失败"

    # 列名到索引的映射
    col_index = {name: idx for idx, name in enumerate(headers)}

    checks = []
    for col_name, typ in column_types.items():
        if col_name not in col_index:
            print(f"预期列 '{col_name}' 不存在于实际表头中，跳过检查")
            continue
        idx = col_index[col_name]
        if isinstance(typ, tuple) and len(typ) == 2 and typ[0] is datetime:
            checks.append((idx, col_name, typ[0], typ[1]))
        else:
            checks.append((idx, col_name, typ, None))

    if not checks:
        print("没有列需要检查")
        return True, "验证通过（无列需要检查）"

    print("\n开始数据类型验证...")
    has_error = False
    row_num = 1
    try:
        with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar, escapechar=escapechar, doublequote=doublequote)
            next(reader)  # skip header
            for row in reader:
                row_num += 1
                if len(row) < len(headers):
                    row += [''] * (len(headers) - len(row))
                elif len(row) > len(headers):
                    row = row[:len(headers)]
                for idx, col_name, typ, fmt in checks:
                    value = row[idx].strip()
                    if value == '':   # 空值跳过检查
                        continue
                    try:
                        if typ is int:
                            int(value)
                        elif typ is float:
                            float(value)
                        elif typ is str:
                            pass
                        elif typ is datetime:
                            if fmt:
                                datetime.strptime(value, fmt)
                            else:
                                datetime.fromisoformat(value)
                        else:
                            print(f" 行 {row_num}, 列 '{col_name}': 不支持的类型 {typ}")
                            has_error = True
                    except Exception as e:
                        print(f" 行 {row_num}, 列 '{col_name}', 值 '{value}' 类型错误: {e}")
                        has_error = True
    except Exception as e:
        return False, f"读取数据行失败: {e}"

    # 最终验证结果提示
    if has_error:
        print("\n数据类型验证完成,存在错误。")
        return False, "数据类型验证失败"
    else:
        print("\n所有数据类型验证通过！")
        return True, "验证通过"


def find_csvs(paths):
    files = []
    if not paths:
        files = glob.glob("**/*.csv", recursive=True)
    else:
        for p in paths:
            if os.path.isdir(p):
                files.extend(glob.glob(os.path.join(p, "**/*.csv"), recursive=True))
            elif os.path.isfile(p) and p.lower().endswith('.csv'):
                files.append(p)
            else:
                # try glob pattern
                files.extend(glob.glob(p, recursive=True))
    # unique and sorted
    return sorted(set(files))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate CSV files in repo")
    parser.add_argument("paths", nargs="*", help="CSV files, directories, or glob patterns to check. Omit to scan all .csv in repo.")
    parser.add_argument("--headers", nargs="+", help="Expected headers in order (space separated).", required=False)
    parser.add_argument("--show-sample", action="store_true", help="Print sample of checked files.")
    args = parser.parse_args()

    # 从文件或仓库配置读取
    expected_headers = args.headers if args.headers else ["product_id", "customer_id", "order_time"]
    column_types = {
        "product_id": int,
        "customer_id": int,
        "order_time": (datetime, "%Y-%m-%d-%H:%M:%S")
    }

    csv_files = find_csvs(args.paths)
    if not csv_files:
        print("未找到任何 CSV 文件可校验。")
        sys.exit(0)

    any_failed = False
    for f in csv_files:
        success, message = validate_csv(f, expected_headers=expected_headers, column_types=column_types)
        if not success:
            print(f"验证失败: {f} -> {message}")
            any_failed = True
        else:
            if args.show_sample:
                print(f"验证成功: {f} -> {message}")

    if any_failed:
        print("\n存在不通过的 CSV 文件。")
        sys.exit(1)
    else:
        print("\n所有 CSV 文件校验通过。")
        sys.exit(0)
