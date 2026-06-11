import os
import sys
import random
import math

def main():
    print("Running number.py in GitHub Actions")

    print(f"Python version: {sys.version}")
 
    
    # 随机数
    random_numbers = [random.randint(1, 100) for _ in range(10)]
    print(f"\nGenerated random numbers: {random_numbers}")
    
    # 计算
    total = sum(random_numbers)
    average = total / len(random_numbers)
    max_val = max(random_numbers)
    min_val = min(random_numbers)
    
    print(f"Sum: {total}")
    print(f"Average: {average:.2f}")
    print(f"Maximum: {max_val}")
    print(f"Minimum: {min_val}")
    
    # 平方根
    num = random_numbers[0]
    if num >= 0:
        print(f"\nSquare root of {num}: {math.sqrt(num):.2f}")
    
    # 读取环境变量
    custom_var = os.getenv("CUSTOM_NUMBER", "42")
    print(f"\nCustom environment variable CUSTOM_NUMBER: {custom_var}")
    
    print("\nScript executed successfully!")

if __name__ == "__main__":
    main()
