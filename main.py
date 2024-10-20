from urllib.parse import unquote

from login import login

lg_version = "1.0.0 Release"

language_dict = {
    0: "自动识别语言",
    1: "Pascal",
    2: "C",
    3: "C++98",
    4: "C++11",
    7: "Python3",
    8: "Java 8",
    9: "Node.js LTS",
    11: "C++14",
    12: "C++17",
    13: "Ruby",
    14: "Go",
    15: "Rust",
    16: "PHP",
    17: "C# Mono",
    19: "Haskell",
    21: "Kotlin/JVM",
    22: "Scala",
    23: "Perl",
    25: "PyPy3",
    27: "C++20",
    28: "C++14(GCC 9)",
    30: "OCaml",
    31: "Julia",
    32: "Lua",
    33: "Java 21"
}

def get_language_name(x):
    return language_dict.get(x, "未知语言")


import json
import requests
import time as t
from bs4 import BeautifulSoup
from termcolor import colored

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection": "keep-alive",
    "Host": "www.luogu.com.cn",
    "Origin": "https://www.luogu.com.cn",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
}

encode = "utf-8"
enableO2 = 1
lang = 28
try:
    cookies_user = json.loads(open("cookie.json", "r").read())
except:
    with open("cookie.json", "w") as f:
        cookies_user = {}
        f.write("{}")
homepage = requests.get(url="https://www.luogu.com.cn/", cookies=cookies_user, headers=header)
soup = BeautifulSoup(homepage.text, 'html.parser')
csrf_token = soup.find_all('meta', {'name': 'csrf-token'})
csrf_token = csrf_token[0].get('content')
header["X-CSRF-TOKEN"] = csrf_token

def SubmitProblem(problem, filename):
    with open(filename, "r", encoding=encode) as f:
        code = f.read()
    datas = {
        "enableO2": enableO2,
        "lang": lang,
        "code": code
    }
    header["Referer"] = "https://www.luogu.com.cn/problem/"+problem
    header["Content-Type"] = "application/json"
    response = requests.post(
        url = "https://www.luogu.com.cn/fe/api/problem/submit/" + problem,
        data = json.dumps(datas),
        json=datas,
        headers = header,
        cookies=cookies_user
    )

    rid = str(response.json()["rid"])

    t.sleep(5)

    GetRecord(rid, False)


def GetRecord(record_id, isopenym):
    print("Record:", record_id)
    print()
    url = f'https://www.luogu.com.cn/record/{record_id}'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }
    r = requests.get(url, headers=header, timeout=5, cookies=cookies_user)
    soup = BeautifulSoup(r.text, 'html.parser')
    res = soup.script.get_text()
    res = unquote(res.split('\"')[1])
    response = json.loads(res)
    resdata = response["currentData"]["record"]
    currentTime = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime(resdata["submitTime"]))
    print("提交时间:", currentTime)
    print("提交用户:", "#" + str(resdata["user"]["uid"]), resdata["user"]["name"])
    print("题目:", resdata["problem"]["pid"], resdata["problem"]["title"])
    print("是否正确:", resdata["status"]==12)
    print("源码长度:", resdata["sourceCodeLength"])
    if isopenym:
        try:
            print("\n源代码:\n" + resdata["sourceCode"])
        except:
            print("\n源代码：您无权查看源代码")
    detail = resdata["detail"]
    comp = detail["compileResult"]
    print("\n编译成功:", comp["success"])
    if not comp["success"]:
        print("编译信息:\n", comp["message"])
    result = detail["judgeResult"]
    print("分数:", str(resdata["score"]) + "/100")
    print("是否开启O2优化:", resdata["enableO2"])
    print("耗时:", str(resdata["time"])+"ms")
    print("内存:", str(resdata["memory"])+"KB")
    print()
    print("共", len(result["subtasks"]), "个子任务\n")
    for i in range(len(result["subtasks"])):
        print("Subtask #" + str(i))
        for si in range(len(result["subtasks"][i]["testCases"])):
            if isinstance(result["subtasks"][i]["testCases"], dict):
                s = result["subtasks"][i]["testCases"][str(si)]
            else:
                s = result["subtasks"][i]["testCases"][si]
            statusAsSub = "Unaccepted"
            if s["status"] == 12:
                statusAsSub = "Accepted"
            print("第", s["id"]+1, "个测试点:", statusAsSub, ", 得分", s["score"], ",", s["description"].strip("\n"), ", 时间:", str(s["time"]) + "ms /", "内存:", str(s["memory"]) + "KB")


def getd(d):
    if d==0:
        return "暂无评定"
    elif d==1:
        return "入门"
    elif d==2:
        return "普及-"
    elif d==3:
        return "普及/提高−"
    elif d==4:
        return "普及+/提高"
    elif d==5:
        return "提高+/省选−"
    elif d==6:
        return "省选/NOI−"
    elif d==7:
        return "NOI/NOI+/CTSC"


this_problem = ""
submit_file = ""

def punch():
    return requests.get(
        'https://www.luogu.com.cn/index/ajax_punch',
        headers=header,
        cookies=cookies_user
    ).text


while True:
    try:
        command = input(">>> ")
        if command == "help":
            print("Luogu Command (by karsl) - 洛谷命令行", lg_version, "- 通过命令行帮助 OIers 更快、更方便、更轻便地使用洛谷高效刷题\n")
            print("支持的命令：")
            print("\tlogin 登录\n\tsubmit 提交\n\tuse [problem] 选择题目[problem]\n\tsetfile [filename] 将[filename]设置为提交文件\n\tencoding [encode] 使用[encode]文件编码（默认utf-8）\n\t-OpenO2 打开O2优化\n\t-CloseO2 关闭O2优化\n\tsetlang [langNum] 选择语言（默认28）\n\tsearch [keyword] 以[keyword]为关键词搜索题目\n\tinfo [problem] 将题目[problem]以markdown完整输出到md文件中\n\trid [id] 查看[id]的提交记录\n\ti 获取此账号信息\n\trlist [int] 查看第[int]页的提交记录\n\trp++ 打卡\n\texit 退出\n")
            print("支持的语言（setlang时请输入数字）: ")
            for i in range(34):
                if get_language_name(i) != "未知语言":
                    print("\t" + get_language_name(i) + ": " + str(i))
        elif command == "submit":
            if this_problem == "":
                print("未选择题目！")
                continue
            if submit_file == "":
                print("未选择提交文件！")
                continue
            SubmitProblem(this_problem, submit_file)
        elif command[:4] == "use ":
            subcmd = command[4:]
            this_problem = subcmd
        elif command[:8] == "setfile ":
            subcmd = command[8:]
            submit_file = subcmd
        elif command[:9] == "encoding ":
            subcmd = command[9:]
            encode = subcmd
        elif command[0] == "-":
            subcmd = command[1:]
            if subcmd == "OpenO2":
                enableO2 = 1
            elif subcmd == "CloseO2":
                enableO2 = 0
        elif command[:8] == "setlang ":
            subcmd = command[8:]
            lang = int(subcmd)
        elif command[:7] == "search ":
            keyword = command[7:]
            response = requests.get(url="https://www.luogu.com.cn/problem/list?keyword="+keyword+"&type=AT%7CB%7CCF%7CP%7CSP%7CUVA&page=1&_contentOnly=1", headers={"Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"}, cookies=cookies_user)
            res = response.json()
            res = res["currentData"]["problems"]["result"]
            maxlpid = 10
            for sproblem in res:
                maxlpid = max(len(sproblem["pid"]), maxlpid)
            for sproblem in res:
                if sproblem["accepted"]:
                    acs = colored("A ", "green")
                elif sproblem["submitted"]:
                    acs = colored("N ", "red")
                else:
                    acs = "- "
                print(acs + sproblem["pid"].ljust(maxlpid+5) + sproblem["title"] + "   难度：" + getd(sproblem["difficulty"]))
        elif command[:5] == "info ":
            pid = command[5:]
            response = requests.get(url="https://www.luogu.com.cn/problem/"+pid+"?_contentOnly=1", headers={"Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"})
            res = response.json()
            with open(pid+".md", "w", encoding=encode) as f:
                resdata = res["currentData"]["problem"]
                f.write("# " + pid + " " + resdata["title"] + "\n\n")
                f.write("### 难度: " + getd(resdata["difficulty"]) + "\n\n## 限制\n\n### 时间限制: ")
                maxtimelim = 0
                mintimelim = 35565
                for j in resdata["limits"]["time"]:
                    maxtimelim = max(maxtimelim, j)
                    mintimelim = min(mintimelim, j)
                if maxtimelim==mintimelim:
                    f.write(str(mintimelim/1000.0) + "s")
                else:
                    f.write(str(mintimelim/1000.0) + "s ~ " + str(maxtimelim/1000.0) + "s")
                f.write("\n\n### 内存限制: ")
                maxtimelim = 0
                mintimelim = 1024*1024*1024
                for j in resdata["limits"]["memory"]:
                    maxtimelim = max(maxtimelim, j)
                    mintimelim = min(mintimelim, j)
                if maxtimelim==mintimelim:
                    f.write(str(mintimelim/1024.0) + " MB")
                else:
                    f.write(str(mintimelim/1024.0) + " MB ~ " + str(maxtimelim/1024.0) + " MB")
                f.write("\n\n## 题目背景\n\n" + resdata["background"] + "\n\n")
                f.write("## 题目描述\n\n" + resdata["description"] + "\n\n")
                f.write("## 输入格式\n\n" + resdata["inputFormat"] + "\n\n")
                f.write("## 输出格式\n\n" + resdata["outputFormat"] + "\n\n")
                f.write("## 输入输出样例\n\n")
                for sm in resdata["samples"]:
                    f.write("### 输入\n\n```\n" + sm[0] + "\n```\n\n### 输出\n\n```\n" + sm[1] + "\n```\n\n")
                f.write("## 说明/提示\n\n" + resdata["hint"] + "\n\n")
        elif command[:4] == "rid ":
            rid = command[4:]
            GetRecord(rid, True)
        elif command == "i":
            response = requests.get(url="https://www.luogu.com.cn/problem/P1001?_contentOnly=1",
                                    headers={"Content-Type": "application/json",
                                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"}, cookies=cookies_user)
            res = response.json()
            userdata = res["currentUser"]
            print("UID:", userdata["uid"])
            uname = colored(userdata["name"], userdata["color"].lower())
            print("账户名称:", uname)
            print("\n未读私信:", userdata["unreadMessageCount"])
            print("未读公告:", userdata["unreadNoticeCount"])
            print("\n排名:", userdata["ranking"])
            print("等级分:", userdata["eloValue"])
            print("CCF 程序设计能力等级:", userdata["ccfLevel"])
            print("\n关注:", userdata["followingCount"])
            print("粉丝:", userdata["followerCount"])
            print("\n个性签名:", userdata["slogan"])
        elif command[:6] == "rlist ":
            subcmd = command[6:]
            response = requests.get(url="https://www.luogu.com.cn/record/list?page="+subcmd+"&_contentOnly=1",
                                    headers={"Content-Type": "application/json",
                                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"}, cookies=cookies_user)
            res = response.json()
            print(res["currentUser"]["name"], "的记录列表")
            records = res["currentData"]["records"]
            for k in records["result"]:
                currentTime = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime(k["submitTime"]))
                print("R" + str(k["id"]), k["problem"]["pid"], k["problem"]["title"], "提交时间: " + currentTime, "提交语言: " + get_language_name(k["language"]), "开启O2: " + str(k["enableO2"]), "得分: " + str(k["score"]), "时间: " + str(k["time"]) + "ms / 内存: " + str(k["memory"]) + "KB", sep="   ")
            print("共", records["count"], "条")
        elif command == "rp++":
            res = punch()
            status = json.loads(res)
            if status['code'] == 200:
                print(status['more']['html'])
            else:
                print(status['message'])
        elif command == "login":
            login()
        elif command == "exit":
            break
        else:
            print("无此命令")
    except Exception as e:
        print(e)
