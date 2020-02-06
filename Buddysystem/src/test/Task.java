package test;


/**

 * Created by sh on 2019/12/15.

 */

public class Task {
    public int [] using_mem={0,0};
    public int need_mem_size=0;
    public int task_ID=0;
    public int arrive_time=0;
    public int running_time=0;

    public int[]   release_mem()
    {
        int [] rt=this.using_mem;
        this.using_mem=null;
        return rt;
    }

    public void get_mem(int [] get)
    {
        this.using_mem=get;
    }

    public Task(int ID,int need,int arrive,int run)
    {
        this.task_ID=ID;
        this.need_mem_size=need;
        this.arrive_time=arrive;
        this.running_time=run;
    }
}
