package test;


import java.util.ArrayList;

import java.util.HashMap;

import java.util.List;

import java.util.Map;



/**

 * Created by sh on 2019/12/14.

 */

public class Buddy {

    public static int nowtime = 0;

    private static final int memsize = 1024;//内存的页数

    private static Character[] Memory = new Character[memsize];//总的内存空间大小  一个int表示一个页的大小为1KB

    public static List<Task> task_list = new ArrayList<>();

    public static List<Task> running_list = new ArrayList<>();

    /**

     * 存储空闲的页表，每个list对应相应的大小的页表块

     **/

    private static List<int[]> size1024K = new ArrayList<>();
    private static List<int[]> size512K = new ArrayList<>();
    private static List<int[]> size256K = new ArrayList<>();
    private static List<int[]> size128K = new ArrayList<>();
    private static List<int[]> size64K = new ArrayList<>();
    private static List<int[]> size32K = new ArrayList<>();
    private static List<int[]> size16K = new ArrayList<>();
    private static List<int[]> size8K = new ArrayList<>();
    private static Map<Integer, List> Mem = new HashMap<>();//存储所有空闲页的列表

    public static void init_mem() {
        for (int i = 0; i < Memory.length; i++) {
            Memory[i] = '_';
        }
        int[] t = {0, memsize - 1};
        size1024K.add(t);
        Mem.put(1024, size1024K);
        Mem.put(512, size512K);
        Mem.put(256, size256K);
        Mem.put(128, size128K);
        Mem.put(64, size64K);
        Mem.put(32, size32K);
        Mem.put(16, size16K);
        Mem.put(8, size8K);
    }

    static void refresh_memory(int begin, int end, int op)//刷新内存
    {
        if (op == 1)
            for (int i = begin; i <= end; i++) {
                Memory[i] = '@';
            }
        if (op == 0) {
            for (int i = begin; i <= end; i++) {
                Memory[i] = '_';
            }
        }
    }



    static int[] get_from_List(int size)//从大小为size的空闲快列表中得到一个块
    {
        int[] rt = new int[2];
        List<int[]> sizex = Mem.get(size);//取出size大小的空闲块队列
        if (sizex.size() > 0)  //如果不为空
        {
            rt = sizex.get(0);   //取出一个块
            sizex.remove(0);   //从队列中删除这个块
            Mem.put(size, sizex);  //将队里放回mem中
        }
        return rt;
    }


    static boolean break_list(int size)//分割页面
    {
        if (size > 1024)//大于1024的页面不存在无法分割
            return false;
        List<int[]> sizex = Mem.get(size);//得到当前size大小的空页列表
        boolean rt = true;
        if (sizex.size() == 0)//如果列表为空
        {
            rt = false;
            rt = break_list(size * 2);//将更大一级的页分解
        }
        if (rt) {   //如果更大一级的页框分割成功，分割本页框，使其成为两个一样大的小
            sizex = Mem.get(size);
            int[] t = sizex.get(0);  //取出一个size大小的页
            sizex.remove(0);//从当前列表中删除
            Mem.put(size, sizex);//放回mem
            int[] t1 = new int[2];
            t1[0] = t[0];
            t1[1] = t1[0] + ((size / 2) - 1);//分割成两个大小一样的小页
            t[0] = t1[1] + 1;
            List<int[]> tem = Mem.get(size / 2);//得到size/2大小的页的列表
            tem.add(t);//将分割好的两个页插入进去
            tem.add(t1);
            Mem.put(size / 2, tem);//将新的列表放入所有的空闲内存中
            return true;
        } else {    //如果更大的叶匡分割失败，表示没有更大的空闲页了，返回值为false
            return false;
        }
    }

    public static boolean request_mem(Task task)//请求调页
    {
        boolean rt;
        int size = task.need_mem_size;
        System.out.println("\n\n当前时间:" + nowtime + "     进程:" + task.task_ID + " 开始请求内存，所需内存大小==" + size + "KB");
        if (size > 1024)//没有大于1024的页可以分配
            return false;
        int t = (int) Math.ceil(Math.log(size) / Math.log(2));// 计算t=log2（size）进一法  // 如果请求为size大小，则需要分配的页的大小为2^t
        if (size <= 8)   //最小页面为8KB  即t最小为3
            t = 3;
        List<int[]> tem = Mem.get((int) Math.pow(2, t));//取出当前2^t大小的空闲页面列表
        if (tem.size() == 0) {  //如果列表为空，需要进行页分割
            rt = break_list((int) Math.pow(2, t) * 2);    //分割得到2^t大小的页
            if (!rt)   //如果分割失败，返回false表示请求失败
                return false;
        }
        int[] get = get_from_List((int) Math.pow(2, t));//取出一个页面
        System.out.println("当前时间:" + nowtime + "     分配得到内存空间从" + get[0] + "==>" + get[1] + " 的 " + (get[1] - get[0] + 1) + "KB内存");
        refresh_memory(get[0], get[1], 1);//刷新内存值  1表示占用
        task.get_mem(get);
        return true;
    }

    public static boolean release_mem(Task task)//释放内存  task是要释放自己占用内存的进程
    {
        int[] rlease_mem = task.release_mem();//将要释放的内存的地址
        int begin = rlease_mem[0];//地址开始
        int end = rlease_mem[1];//地址结束
        int size = end - begin + 1;//该快页面的大小
        System.out.println("\n\n\n当前时间:" + nowtime + "     ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||进程：" + task.task_ID + "释放地址" + rlease_mem[0] + "==>" + rlease_mem[1] + "的内存" + "大小为：" + size + "KB");
        refresh_memory(rlease_mem[0], rlease_mem[1], 0);
        int[] mem_after_combine = combine_mem(size, begin, end);
        size = mem_after_combine[1] - mem_after_combine[0] + 1;
        List<int[]> tem = Mem.get(size);
        tem.add(mem_after_combine);
        Mem.put(size, tem);
        return true;
    }





    public static int[] combine_mem(int size, int begin, int end)//块合并
    {
        int[] rt = {begin, end};//返回合并后的块的起始地址和结束地址
        while (true) {
            int[] neighbor = get_neighbour(size, begin, end);//查找是否有大小相同的相邻的块
            if (neighbor == null)//如果没有的话就直接返回rt
                return rt;
            else {
                if (neighbor[0] > rt[1])//如果相邻的块在当前块的后面
                    rt[1] = neighbor[1];//修改合并后块的结束地址
                else
                    rt[0] = neighbor[0];//如果相邻的块在前面，则修改合并后块的起始地址
                begin = rt[0];//更新起始地址
                end = rt[1];//更新结束地址
                size = end - begin + 1;//更新当前块大小
            }
        }
    }


    public static int[] get_neighbour(int size, int begin, int end)//得到输入块的相邻块的地址
    {
        List<int[]> tem = Mem.get(size);//取出大小为size的空闲块 的列表
        for (int i = 0; i < tem.size(); i++)//遍历所有size大小的空闲快
        {
            int[] t = tem.get(i);
            if (t[0] == end + 1 || t[1] == begin - 1) {  //如果有一个空闲快的起始地址是当前块的结束地址+1   或者     一个空闲快的结束地址是当前块的起始地址—1  说明这个两个块是相邻的
                tem.remove(i);  //从size大小的列表中删除该相邻块
                Mem.put(size, tem);//放回内存
                return t;//返回这个相邻的块
            }
        }
        return null;//如果没有当前块的相邻块，返回空指针
    }


    static void init_task() {
        for (int i = 0; i < 20; i++) {
            //              进程号        需要的页面数                    进程到达时间     进程预计执行时间
            Task t = new Task(i, (int) (Math.random() * 400) % 200 + 1, i, (int) (Math.random() * 20) % 10 + 1);
            task_list.add(t);
        }
    }

    static void show_memory() {
        for (int i = 0; i < Memory.length; i += 8) {
            System.out.print(Memory[i]);
        }
        System.out.println("");
    }

    public static void main(String arg[]) {
        System.out.println("默认内存大小为1024KB,最小的内存页面为8KB\n总共有20个进程不同时间到达，申请随机大小(1~200KB)的内存页面,随机占用1~10秒时间\n每次成功申请和释放内存后会打印内存的占用情况\n‘@’表示内存8KB内存被占用‘_’表示8KB内存空闲");
        init_task();
        init_mem();
        while (true) {
            for (int i = 0; i < task_list.size(); i++) {
                Task tem = task_list.get(i);//进程队列里取出一个进程
                if (request_mem(tem)) {
                    tem.arrive_time = nowtime;  //纪录该进程开始得到内存的时间
                    task_list.remove(i);  //成功获得内存的进程从等待队列中删除，加入到正在运行的队列中
                    running_list.add(tem);
                    System.out.println("当前时间:" + nowtime + "     request memory success" + "    进程需要运行时间：" + tem.running_time);
                    show_memory();
                    break;   //同一个时刻只能有一个进程获得内存，如果已经有一个进程成功分配内存，则终止循环
                } else     //如果请求内存失败，则从输出请求失败信息，并进入下一个循环，取出进程队列中的下个进程
                    System.out.println("当前时间:" + nowtime + "     request memory failed");
            }
            for (int i = 0; i < running_list.size(); i++) {   //扫描正在运行的进程列表
                Task tem = running_list.get(i);
                if (tem.running_time <= nowtime - tem.arrive_time) {  //如果有一个进程所需的内存的时间结束
                    release_mem(tem);    //释放内存
                    System.out.println("当前时间:" + nowtime + "     release memory success");
                    show_memory();   //打印出当前的内存状况
                    running_list.remove(i);  //从运行队列中删掉该进程
                    i = 0;   //重新从队列头部扫描
                }
            }
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            nowtime++;
            System.out.println("\n\n~~~~~~~~~~~~~~~~~~~~~" + "当前时间:" + nowtime);
            if (running_list.size() == 0 && task_list.size() == 0)
                break;
        }
    }

}






