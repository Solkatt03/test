#!/usr/bin/env python3

import os
import sys
import platform

def main():
    print("=" * 50)
    print("Python script executed by GitHub Actions")
    print("=" * 50)

   
    # 自定义环境变量
    my_var = os.getenv("MY_CUSTOM_VAR", "default_value")
    print(f"MY_CUSTOM_VAR = {my_var}")

    # 计算
    numbers = [1, 2, 3, 4, 5]
    total = sum(numbers)
    print(f"Sum of {numbers} = {total}")

    # # 可选：使用 requests 调用 API（需要提前安装 requests）
    # # 如果不需要，可以注释掉。若要启用，请在 requirements.txt 中添加 requests
    # try:
    #     import requests
    #     response = requests.get("https://api.github.com/zen")
    #     if response.status_code == 200:
    #         print(f"GitHub Zen: {response.text}")
    #     else:
    #         print("API call failed")
    # except ImportError:
    #     print("requests 库未安装，跳过 API 调用示例")
    # except Exception as e:
    #     print(f"API 调用出错: {e}")

    print("\n脚本执行完毕！")

if __name__ == "__main__":
    main()
