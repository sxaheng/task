import numpy as np

def safe(available, need, allocation):
    """
    安全检测算法：检查系统是否处于安全状态。
    :param available: 可用资源向量
    :param need: 最大需求矩阵
    :param allocation: 分配矩阵
    :return: 如果系统安全，返回 (True, 安全序列)；否则返回 (False, [])。
    """
    processes = allocation.shape[0]
    work = available.copy() 
    finish = np.zeros(processes, dtype=bool) 
    safearray = [] 

    while True:
        found = False 
        for i in range(processes):
            if not finish[i] and np.all(need[i] - allocation[i] <= work):
                work += allocation[i] 
                finish[i] = True 
                safearray.append(i)  
                found = True 
        if not found:
            break

    if np.all(finish):
        return True, safearray
    else:
        return False, []

def bankers(available, need, allocation, request, process_id):
    """
    银行家算法：处理进程的资源请求
    :param available: 可用资源向量
    :param need: 最大需求矩阵
    :param allocation: 分配矩阵
    :param request: 进程的请求
    :param process_id: 请求资源的进程ID
    :return: 如果请求可以，返回 (True, 安全序列)；否则返回 (False, 错误信息)。
    """
    resources = available.shape[0]  
    need = need - allocation  
    if not np.all(request <= need[process_id]):
        return False, "超过了其最大需求"
    if not np.all(request <= available):
        return False, "资源不足"
    available -= request 
    allocation[process_id] += request 
    need[process_id] -= request  
    #在这里调用了安全算法
    safe_state, safearray = safe(available, need, allocation)
    if safe_state:
        return True, safearray  
    else:
        available += request
        allocation[process_id] -= request
        need[process_id] += request
        return False, "系统不安全状态"

# 给一个小例子
if __name__ == "__main__":
    available = np.array([3, 3, 2])
    need = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])
    allocation = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])
    # 进程1
    request = np.array([1, 1, 2])
    process_id = 1  # 进程ID
    # 使用银行家算法
    result, msg = bankers(available, need, allocation, request, process_id)
    if result:
        print("可以分配资源，安全序列是:", msg)
    else:
        print("不能分配资源，因为", msg)