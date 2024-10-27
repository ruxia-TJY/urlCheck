import random
import os

success_url = [
    'https://www.baidu.com',
    'https://www.google.com',
    'https://cn.bing.com'
]

error_url = [
    'https://dw',
    'dwdd',
    'https://dwwwwwwwwwwwwwwwww.com'
]

def main():
    exe = 'python urlCheck.py'

    url = ' '.join(success_url)
    cmd = f'{exe} --url {url}'
    
    os.system(cmd)

if __name__ == '__main__':
    main()