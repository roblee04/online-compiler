# measure the time of all operations under some simulated network load

# we will be directly invoking 
#   /api/compile
#   /api/execute


import requests
import time
import threading
from pathlib import Path

WEBAPP_IP = "http://18.144.156.160:5000/"

def comp_request(data):
    
    url = WEBAPP_IP + 'api/compile'
    start = time.time()
    response = requests.post(url, json=data)
    end = time.time()
    # print(response.json())
    t = end - start
    return t

def exec_request(data):

    url = WEBAPP_IP + 'api/run'
    start = time.time()
    response = requests.post(url, json=data)
    end = time.time()
    # print(response.json())
    t = end - start
    return t



def test(code, cmp):
    # 10 compile
    cmp_tot = 0
    cmp_max = 0
    # print("COMPILE with " + cmp)
    for i in range(10):
        data = {
            'code': code + " // " + str(i) + " " + cmp,
            'compiler': cmp
        }
        t = comp_request(data)
        cmp_tot += t
        cmp_max = max(cmp_max, t)
        # print(t)
    avg = cmp_tot / 10
    # print("\n AVG: " + str(avg) + "\t MAX: " + str(cmp_max) + "\n")

    # 10 exec
    exe_tot = 0
    exe_max = 0
    # print("EXECUTE")
    for i in range(2):
        data = {
            'code': code + " // " + str(i) + " " + cmp,
            'compiler': cmp
        }
        t2 = exec_request(data)
        exe_tot += t2
        exe_max = max(exe_max, t2)
        # print(t2)
    avg2 = exe_tot / 10
    # print("\n AVG: " + str(avg2) + "\t MAX: " + str(exe_max) + "\n")

    print("COMPILE with " + cmp)
    print("\n AVG: " + str(avg) + "\t MAX: " + str(cmp_max) + "\n")
    print("EXECUTE")
    print("\n AVG: " + str(avg2) + "\t MAX: " + str(exe_max) + "\n")





def main():
    gcc = ["gcc 5.4.0", "gcc 7.5.0", "gcc 9.4.0"]
    gpp = ["g++ 5.4.0", "g++ 7.5.0", "g++ 9.4.0"]
    clang = ["clang 3.8.0", "clang 6.0.0", "clang 10.0.0"]
    clangpp = ["clang++ 3.8.0", "clang++ 6.0.0", "clang++ 10.0.0"]
    tcc = ["latest"]

    c_cmp = gcc + clang
    cpp_cmp = gpp + clangpp

    filler = ""
    code = Path('../test.c').read_text() 
    code_cpp = Path('../test.cpp').read_text() 
    # cmp = 'gcc 5.4.0'

    no_threads = 1

    for cmp in c_cmp:
        threads = []
        for i in range(no_threads):
            code += " // " + str(time.time()) + str(i)
            threads.append(threading.Thread(target=test, args=(code, cmp)))
            threads[-1].start()
        for thread in threads:
            thread.join()

    for cmp in cpp_cmp:
        threads = []
        for i in range(no_threads):
            code_cpp += " // " + str(time.time()) + str(i)
            threads.append(threading.Thread(target=test, args=(code_cpp, cmp)))
            threads[-1].start()
        for thread in threads:
            thread.join()


if __name__ == '__main__':
    main()