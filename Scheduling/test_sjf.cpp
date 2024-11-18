#include<iostream>
#include<algorithm>
#include<vector>
#include<limits.h>
#include<string>
using namespace std;
class Process{
    public:
    int pid;
    int at;
    int bt;
    int rt;
    int ct;
    Process(int id,int arrival_time,int burst_time)
     : pid(id) , at(arrival_time) , bt(burst_time) , rt(burst_time) ,ct(0) {}

};

bool compareArrivalTime(const Process& a , const Process& b)
{
    return a.at > b.at;
}
int main()
{
    int n;
    cout << "Enter number of processes :";
    cin >> n;
    vector<Process> processes;

    for(int i=0;i<n;i++)
    {
        int arrivaltime, bursttime;
        cout << "Enter Arrival and burst time" << " ";
        cin >> arrivaltime >> bursttime;
        processes.emplace_back(Process(i+1 , arrivaltime,bursttime));
    }
    
    //sort on the basis of arrival time
    sort(processes.begin() , processes.end());
    int currentTime = 0; //this will act as clock
    int completed = 0;   // number of processes completed
    int total_tat = 0;
    int total_wt = 0;

    while(completed!=n)
    {
        int minIndex = -1;
        int minBurstTime = INT_MAX;

        for(int i=0;i<n;i++)
        {
            if(processes[i].at <= currentTime && processes[i].rt > 0)
            {
                if(processes[i].rt < minBurstTime)
                {
                    minIndex = i;
                    minBurstTime = processes[i].rt;
                }
               
            }

        }

        //no ready
        if(minIndex == -1)
        {
            currentTime ++;
        }
        else{
            processes[minIndex].rt--;
            currentTime++;

            //if my rt becomes zero case
            if(processes[i].rt == 0)
            {
                completed++;

                processes[minIndex].ct = currentTime; // currentime will be completeion
                int tat = processes[minIndex].ct - processes[minIndex].at;
                int wt = tat - processes[minIndex].bt;

                total_tat += tat;
                total_wt += wt;    
            } 
        }
    }

    cout << "\tPID\tAT\tBT\tCT\tTAT\tWT\n";

    for(const auto& p:processes)
    {
        int tat = p.ct - p.at;
        int wt = tat - p.bt;
        cout << p.pid << "\t" << p.at << "\t" << p.bt << "\t" << p.ct <<"\t" << tat <<"\t"<<wt<<"\n";
    }
    
    cout << "\n Average TAT:" << (float)total_tat/n << endl;
    cout << "\n Average Waiting Time" << (float)total_wt/n << endl;

 
    return 0;
}