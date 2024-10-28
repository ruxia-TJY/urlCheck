'''
    check url valid
'''

import textwrap
from urllib import request,error
import argparse
from rich.console import Console
import time

class info:
    name = "urlCheck"
    version = "0.0.1"
    verStr = f"{name} {version}"
    author = "Jiayu Tu"
    email = "ruxia.tjy@qq.com"
    protocol = "MIT"
    desc = '''
A Script check url valid, written by JiayuTu.based
on Python.

thanks for use and if you love it,could you please
give me a star in github.I will grateful and bette
r able to develop more useful tools,If you find an
y bug,or have any suggestions, please tell me.
            
Github Repo: github.com/ruxia-TJY/urlCheck
Email: ruxia.tjy@qq.com
            
Thank for use!
'''

class count:
    '''
        自增器
    '''
    def __init__(self):
        self.result = {"Total":0}

    def add(self,code:int) -> None:
        if code == 0:
            self.result['Error'] = self.result.get('Error',0) + 1
        elif code == 1:
            self.result['Error-URL'] = self.result.get('Error-URL',0) + 1
        elif code == 200:
            self.result['Success'] = self.result.get('Success',0) + 1
        else:
            self.result[str(code)] = self.result.get(str(code),0) + 1
        self.result['Total'] += 1

    def __repr__(self):
        result_lst = [f"{key}:{value}" for key ,value in self.result.items()]
        r = ' '.join(result_lst)
        return r


console = Console()

def test_connect(url:str,timeout:int) -> (int,str):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

    code = 0
    with console.status("") as s:
        s.update(f"{url}")
        now = time.strftime("%H:%M:%S", time.localtime())
        try:
            req = request.Request(url,headers=headers)
        except Exception as e:
            console.print(f"[green][bold][{now}]\t[001][/]\t{url}")
            code = 1
            return code
        try:
            responese = request.urlopen(req,timeout=timeout)
            console.print(f"[green][bold][{now}]\t[{responese.status}][/]\t{url}")
            code = 200
        except error.HTTPError as e:
            console.print(f"[yellow][bold][{now}]\t[{e.code}][/]\t{url}")
            code = e.code
        except Exception as e:
            console.print(f"[red][{now}]\t[000]\t{url}")
            code = 0
    return (code,now)

def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(info.desc),
                                     # epilog="github.com/ruxia-TJY"
                                     )
    parser_url_source = parser.add_mutually_exclusive_group()
    parser_url_source.add_argument("--url", type=str,nargs="+",
                                   help="check from string")
    parser_url_source.add_argument("--file",type=str,nargs=1,
                                   help="check from File")

    parser.add_argument("--timeout",type=int,nargs=1,
                        default=3,metavar="default=3",help="set timeout")
    parser.add_argument('--out',type=str,nargs=1,
                        help="output to file")
    parser.add_argument('--out-flag',type=str,nargs=1,
                        default="tcu",dest="outflag",help='output flag')
    parser.add_argument("-v","-V","--version",action="version",
                        version=info.verStr)
    args = parser.parse_args()
    return args

def parser_outflag(flags:str,result:list) -> str:
    t = [row[0] for row in result]
    c = [row[1] for row in result]
    u = [row[2] for row in result]
    flag_all = ['t','c','u']
    result_str = ''
    new_arr = []
    for i,flag in enumerate(flags):
        if flag not in flag_all:
            continue

        if i == 0:
            new_arr = eval(flag)
        elif i == 1:
            new_arr = [list(t) for t in zip(new_arr,eval(flag))]
        elif i == 2:
            new_arr = [row + [eval(flag)[i]] for i,row in enumerate(new_arr)]

    for col in new_arr:
        result = ','.join(col)
        result_str += f'{result}\n'

    return result_str

def main():
    global console
    args = parser()
    c = count()

    url_lst = args.url if args.url is not None else []

    if args.file:
        try:
            with open(args.file[0], 'r') as f:
                url_lst = [i.rstrip() for i in f.readlines()]
        except FileNotFoundError:
            console.print('[red]File not found!')
            return
        except PermissionError:
            console.print('[red]Permission Error!')
            return

    if not len(url_lst):
        console.print('[red]URL list is empty!')
        return

    result = []
    time_start = time.time()
    for url in url_lst:
        code,now = test_connect(url,timeout=args.timeout)
        c.add(code)
        result_i = [now,str(code).zfill(3),url]
        result.append(result_i)

    print('-' * 51)
    console.print(f'[green]{c}')
    console.print(f"[green]Time:{(time.time() - time_start):.4f}s")

    if args.out:
        # default out-flag
        outflag = "tcu"
        if args.outflag:
            outflag = args.outflag[0]

        result_str = parser_outflag(outflag,result)

        try:
            with open(args.out[0],'w',encoding="UTF-8") as f:
                f.write(result_str)
        except Exception as e:
            console.print('[red]output failed')

if __name__ == '__main__':
    main()