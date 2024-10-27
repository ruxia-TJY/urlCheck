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
console = Console()

def test_connect(url,timeout):
    code = 0
    with console.status("") as s:
        s.update(f"{url}")
        req = request.Request(url)
        now = time.strftime("%H:%M:%S",time.localtime())
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
    return code
def parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(info.desc),
                                     # epilog="github.com/ruxia-TJY"
                                     )
    parser_url_source = parser.add_mutually_exclusive_group()
    parser_url_source.add_argument("--url", type=str,nargs="+", help="check from string")
    parser_url_source.add_argument("--file",type=str,nargs=1, help="check from File")

    parser.add_argument("--timeout",type=int,nargs=1,
                        default=3,metavar="default=3",help="set timeout")
    parser.add_argument("-v","-V","--version",action="version",version=info.verStr)
    args = parser.parse_args()
    return args

class count:
    '''
        自增器
    '''
    def __init__(self):
        self.result = {"Total":0}

    def add(self,code):
        if code == 0:
            self.result['Error'] = self.result.get('Error',0) + 1
        elif code == 200:
            self.result['Success'] = self.result.get('Success',0) + 1
        else:
            self.result[str(code)] = self.result.get(str(code),0) + 1
        self.result['Total'] += 1

    def __repr__(self):
        result_lst = [f"{key}:{value}" for key ,value in self.result.items()]
        r = ' '.join(result_lst)
        return r

def main():
    args = parser()
    c = count()
    if args.url:
        for i in args.url:
            code = test_connect(i,timeout=args.timeout)
            c.add(code)
        print(c)
    elif args.file:
        # TODO File Mode
        pass


if __name__ == '__main__':
    main()