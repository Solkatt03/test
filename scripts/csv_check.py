import csv 
from datetime import datetime
import os

def validate_csv(csv_path, expected_headers, column_types, delimiter=',', quotechar='"', escapechar=None, doublequote:bool=True):
    if not os.path.exists(csv_path):
        return False, f"文件不存在: {csv_path}"
    
    if not csv_path.lower().endswith('.csv'):
        return False, f"文件不是csv格式: {os.path.basename(csv_path)}"
    
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        try:
            reader = csv.reader(f, delimiter=delimiter)
            headers = next(reader)
        except Exception as e:
            return False, f"读取csv文件失败: {str(e)}"
        
    
    # 表头验证
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
        for row in reader:
            row_num += 1
            if len(row) < len(headers):
                row += [''] * (len(headers) - len(row))
            elif len(row) > len(headers):
                row = row[:len(headers)]
            for idx, col_name, typ, fmt in checks:
                value = row[idx]
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

    
    # 最终验证结果提示
    if has_error:
        print("\n数据类型验证完成,存在错误。")
        return False, "数据类型验证失败"
    else:
        print("\n所有数据类型验证通过！")
        return True, "验证通过"
    
    # 索引, 列名, 预期类型, 格式
    

if __name__ == "__main__":
    # 预期表头
    table_headers = ["product_id", "customer_id", "order_time"]
    
    # 预期数据类型
    column_types = {
        "product_id": int,
        "customer_id": int,
        "order_time": (datetime, "%Y-%m-%d-%H:%M:%S")
    }
    
  
    success, message = validate_csv(
        csv_path="C:/project/csv/test6_sheet0.csv/Sheet1.csv",
        expected_headers=table_headers,
        column_types=column_types
    )

    if not success:
        print(f"\n验证失败: {message}")
    else:
        print(f"\n验证成功: {message}")
