import random

# a= [''for _ in range(100)]
#
# def store(count,process):
#     i=0
#     while i < count:
#         temp = random.randint(0, 99)
#         if a[temp]:
#             continue
#         else:
#             i += 1
#             a[temp] = True
#             process.blocknum.append(int(temp))
#     process.blocknum.sort()
#
# def page(process,timeslice):
#     count = 0  # 记录缺页数
#     list=process.page
#     a_list = []
#     for i in process.block:
#         a_list.append(i)
#     k=0
#     for i in list:
#         if k==timeslice:
#             break
#         if i not in a_list:
#             if len(a_list) < 3:          # 主存还有空闲
#                 a_list.append(i)         # a.list.append(i)将元素i添加到a_list尾部
#                 process.pagetable[process.page1.index(i)]=process.blocknum[process.count]
#                 print('栈情况：',a_list,"缺页了")
#                 print('页号:',process.page1)
#                 print('块号：',process.pagetable)
#                 process.block = a_list
#                 process.count+=1
#             else:
#                 count += 1
#                 temp=process.pagetable[process.page1.index(process.block[0])]
#                 process.pagetable[process.page1.index(i)]=temp
#                 process.pagetable[process.page1.index(process.block[0])]=''
#                 a_list[:2] = a_list[1:]  # 将前两个元素替换为后两个元素，列表首元素出列表的功能
#                 a_list[2:] = [i]         # 将i元素放移动后的到列表最后
#                 print('栈情况：',a_list, "缺页了")
#                 print('页号:', process.page1)
#                 print('块号：', process.pagetable)
#                 process.block = a_list
#         else:
#             a_list[a_list.index(i):] = a_list[a_list.index(i) + 1:]  # 将i开始和元素后面的元素替换为i元素后面的元素
#             a_list[len(a_list):] = [i]                               # 将i元素插入到移动后的列表后面
#             print('栈情况：',a_list)
#             print('页号:', process.page1)
#             print('块号：', process.pagetable)
#             process.block = a_list
#         k+=1
#     process.block=a_list
#     for i in range(0,timeslice):
#         process.page.pop(0)
#     #print('当前进程的页表情况',process.page)
#     #print("缺页数为：",count)


class  Process:
    def __init__(self,name,arrive_time,serve_time):
        self.name=name                              #进程名
        self.arrive_time=arrive_time                #到达时间
        self.serve_time=serve_time                  #需要服务的时间
        self.left_serve_time=serve_time             #剩余需要服务的时间
        self.finish_time=0                          #完成时间
        self.cycling_time=0                         #周转时间
        self.w_cycling_time=0                       #带权周转时间
        self.timeslice =0                           #被抢占的进程时间片
        self.seize=False                            #判断进程在第二或者第三队列时是否被抢占
        #self.page = []                              # 页面序号列
        self.block = []                             # 栈
        self.blocknum = []                          # 对应内存物理号
        #self.pagetable=[''for _ in range(10)]          # 页表
        #self.page1=[0,1,2,3,4,5,6,7,8,9]
        self.count=0

class Queue:
    def __init__(self,level,process_list):
        self.level=level
        self.process_list=process_list
        self.q=0

    def size(self):
        return len(self.process_list)

    def get(self,index):
        return self.process_list[index]

    def add(self,process):
        self.process_list.append(process)

    def delete(self,index):
        self.process_list.remove(self.process_list[index])

class MulitlevedFeedbackQueue():
    def __init__(self,queue_list,q_first):
        self.queue_list=queue_list
        self.q_first=q_first
        self.time=0

    def scheduling(self):
        q_list=self.queue_list              #当前队列集合
        q_first=self.q_first                #第一个队列的时间片
        flag = 0
        self.judge(self.time)
        i=0
        while i<3:

            if flag==1:
                i=0
            elif flag==2:
                i=1
            elif flag==3:
                i=2
            # 确定每个队列的时间片
            if i==0:
                q_list[i].q=q_first
            else :
                q_list[i].q=q_list[i-1].q*2
            #从第一个队列开始执行时间片
            #先判断是否是最后一个队列，最后一个队列直接执行RR调度算法
            #不是最后一个队列的话，就执行当前队列时间片后判断是否有必要加入到下一个队列的末尾
            if i==2:
                index = 0
                while (True):
                    if 0 == self.queue_list[2].size():
                        print("全部完成")
                        i += 1
                        break
                    currentQueue = self.queue_list[2]
                    '''print(len(self.queue_list[0].process_list))'''
                    if currentQueue.get(index).left_serve_time > q_list[i].q:
                        print("当前时间", self.time)
                        currentQueue.get(index).left_serve_time -= q_list[i].q
                        print('第  %d  队列时间片: %d' % (i,8))
                        print('进程没有执行完毕,需要添加至当前队列末尾：进程名称：%s ' % (currentQueue.get(index).name))
                        #page(currentQueue.get(index), 8)
                        print()
                        # 将当前进程扔到下一个队列的尾部
                        self.queue_list[2].add(currentQueue.get(index))
                        self.queue_list[2].delete(index)
                        self.time += q_list[i].q
                        print("当前时间", self.time)
                    else:
                        print("当前时间", self.time)
                        print('第  %d  队列时间片: %d' % (i, 8))
                        print('进程执行完毕:', currentQueue.get(index).name)
                        #page(currentQueue.get(index),currentQueue.get(index).left_serve_time)
                        #print('调用的物理块', currentQueue.get(index).blocknum)
                        #print(currentQueue.get(index).block)
                        self.time += currentQueue.get(index).left_serve_time
                        self.queue_list[2].left_serve_time = 0
                        self.queue_list[2].delete(index)
                        print("进程结束时间",self.time)
                        print()
            elif i==0:
                index=0
                while(True):
                    if 0==self.queue_list[0].size():
                        print("进入第 1 队列")
                        i+=1
                        flag=2
                        break
                    currentQueue = self.queue_list[0]
                    '''print(len(self.queue_list[0].process_list))'''
                    if currentQueue.get(index).left_serve_time>q_list[i].q:
                        currentQueue.get(index).left_serve_time-=q_list[i].q
                        print('当前时间 %d'%(self.time))
                        print('第  %d  队列时间片: %d'%(i,q_list[i].q))
                        #page(currentQueue.get(index), 2)
                        print('进程没有执行完毕,需要添加至下一队列末尾：进程名称：%s '%(currentQueue.get(index).name))
                        #将当前进程扔到下一个队列的尾部
                        print()
                        self.queue_list[1].add(currentQueue.get(index))
                    else:
                        print("当前时间", self.time)
                        print('第  %d  队列时间片: %d' % (i, q_list[i].q))
                        #page(currentQueue.get(index), 2)
                        print('进程执行完毕:',currentQueue.get(index).name)
                        print()
                        self.queue_list[0].left_serve_time=0
                    self.queue_list[0].delete(0)
                    self.time += q_list[0].q
                    self.judge(self.time)
            elif i==1:
                index=0
                count=0
                while(True):
                    if 0==self.queue_list[1].size():
                        print("进入第 2 队列")
                        i += 1
                        flag = 3
                        break
                    currentQueue = self.queue_list[1]
                    print('当前时间 %d' % (self.time))
                    if self.judge(self.time):
                        flag = 1
                        queue=self.queue_list[1].get(index)
                        queue.seize=True
                        queue.timeslice= q_list[i].q-count
                        self.queue_list[1].delete(index)
                        self.queue_list[1].add(queue)
                        q_list[i].q = q_list[i-1].q*2
                        print("第  %d  秒发生抢占" % (self.time))
                        print('进程插入当前队列末尾：进程名称：%s ' % (queue.name))
                        print('剩余 %d 时间片'%(queue.timeslice))
                        queue1 = self.queue_list[0].get(index)
                        print('进程 %s 加入第 %d 队列'%(queue1.name,i-1))
                        print()
                        break
                    currentQueue.get(index).left_serve_time -= 1
                    if currentQueue.get(index).seize==False:
                        self.time += 1
                        q_list[i].q -= 1
                        print('进程 %s 正在运行'%(currentQueue.get(index).name))
                        #page(currentQueue.get(index), 1)
                        if currentQueue.get(index).left_serve_time > 0 and q_list[i].q == 0:
                            print('第  %d  队列时间片: %d' % (i, 4))
                            print('进程没有执行完毕,需要添加至下一队列末尾：进程名称：%s ' % (currentQueue.get(index).name))
                            print()
                            # 将当前进程扔到下一个队列的尾部
                            self.queue_list[i + 1].add(currentQueue.get(index))
                            self.queue_list[1].delete(index)
                            q_list[i].q = 4
                        elif currentQueue.get(index).left_serve_time == 0 and q_list[i].q >= 0:
                            print('第  %d  队列时间片: %d' % (i, 4))
                            print('进程执行完毕:', currentQueue.get(index).name)
                            print()
                            self.queue_list[1].left_serve_time = 0
                            self.queue_list[1].delete(index)
                            q_list[i].q = 4
                    elif currentQueue.get(index).seize==True and currentQueue.get(index).timeslice>= 0:
                        self.time += 1
                        count += 1
                        print('进程 %s 正在运行' % (currentQueue.get(index).name))
                        #page(currentQueue.get(index), 1)
                        #print(currentQueue.get(index).left_serve_time)
                        currentQueue.get(index).timeslice -= 1
                        if currentQueue.get(index).left_serve_time > 0 and currentQueue.get(index).timeslice== 0:
                            print('第  %d  队列时间片: %d' % (i, 4))
                            print('进程没有执行完毕,需要添加至下一队列末尾：进程名称：%s ' % (currentQueue.get(index).name))
                            print()
                            #print(currentQueue.get(index).left_serve_time)
                            count=0
                            # 将当前进程扔到下一个队列的尾部
                            self.queue_list[i + 1].add(currentQueue.get(index))
                            self.queue_list[1].delete(index)
                            q_list[i].q = 4
                        elif currentQueue.get(index).left_serve_time == 0 and currentQueue.get(index).timeslice>= 0:
                            print('第  %d  队列时间片: %d' % (i, 4))
                            print('进程执行完毕:', currentQueue.get(index).name)
                            print()
                            self.queue_list[1].left_serve_time = 0
                            self.queue_list[1].delete(index)
                            q_list[i].q = 4
    def judge(self,time):
        processA = Process('A', 0, 10)
        processB = Process('B', 3, 10)
        processC = Process('C', 5, 10)
        processD = Process('D', 7, 10)
        processE = Process('E', 13, 10)
        come=0
        if time==processA.arrive_time:
            #store(3,processA)
            #processA.page=[1,3,4,6,2,5,1,2,3,4]
            self.queue_list[0].add(processA)
            come = 1
        elif time==processB.arrive_time:
            #store(3, processB)
            #processB.page = [2, 5, 6, 5, 3, 1, 4, 2, 3, 4]
            self.queue_list[0].add(processB)
            come = 1
        elif time==processC.arrive_time:
            #store(3,processC)
            #processC.page = [3, 5, 2, 5, 3, 4, 1, 2, 5, 4]
            self.queue_list[0].add(processC)
            come = 1
        elif time==processD.arrive_time:
            #store(3,processD)
            #processD.page = [4, 5, 2, 5, 3, 5, 1, 2, 3, 1]
            self.queue_list[0].add(processD)
            come = 1
        elif time==processE.arrive_time:
            #store(3, processE)
            #processE.page = [2, 5,4, 5, 1, 4, 1, 3, 2, 4]
            self.queue_list[0].add(processE)
            come = 1
        return come==1

''' 
测试程序
'''
if __name__=='__main__':

    '''使用多级反馈队列调度算法'''
    print()
    print('#################################################################')
    print('---------------------------多级反馈队列---------------------------')
    print('#################################################################')
    print()
    process_list0,process_list1,process_list2=[],[],[]

    #process_list=[]
    #队列
    queue_list=[]
    queue0=Queue(0,process_list0)
    queue1=Queue(1,process_list1)
    queue2=Queue(2,process_list2)
    queue_list.append(queue0),queue_list.append(queue1),queue_list.append(queue2)
    #使用多级反馈队列调度算法,第一队列时间片为2
    mfq=MulitlevedFeedbackQueue(queue_list,2)
    mfq.scheduling()
    exit()