import os
import sys

def main():
    
    print("Reading GitHub Actions Variables and Secrets")
 

    # 读取 Variable
    my_var = os.getenv("MY_VAR", "default_value")
    print(f"MY_VAR = {my_var}")

    # 读取 Secret
    api_key = os.getenv("API_KEY")
    if api_key:
        print(f"API_KEY = {api_key}")  
    else:
        print("API_KEY not set")
        
    print("\n finished.")

if __name__ == "__main__":
    main()
