#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;
class Process{
public:
    int pid;
    int at;
    int bt;
    int ct;
    int rt;
    Process(int id,int arrivalTime,int burstTime)
         :pid(id) , at(arrivalTime),bt(burstTime),ct(0),rt(burstTime) {}
    
};

bool arrivalcomp(const Process &a , const Process &b){
    return a.at < b.at;
}
int main()
{
    int n;
    cout << "Enter number of processes :";
    cin >> n ;
    vector<Process> processes(n);
    for(int i=0;i<n;i++)
    {
        int arrivalTime,burstTime;
        cout << "Enter arrival and bursttime" << " ";
        cin >> arrivalTime >> burstTime ;
        processes.emplace_back(i+1,arrivalTime,burstTime);
    }

    sort(processes.begin(),processes.end(),arrivalcomp);

    int current_time = 0;
    int completed = 0;
    int waiting_time = 0;
    int turnaround_time = 0;

    while(completed!=n)
    {
        int  minIndex = -1;
        int minBursttime = INT_MAX;

        for(int i=0;i<n;i++)
        {
            if(processes[i].at <= current_time && processes[i].rt > 0)
            {
                if(processes[i].rt < minBursttime)
                {
                    minBursttime = processes[i].rt;
                    minIndex = i;
                }
            }
        }

        if(minIndex ==-1)
        {
            current_time++;
        }
        else{
            current_time++;
            processes[minIndex].rt--;

            if(processes[minIndex].rt == 0)
            {
                completed++;
                processes[minIndex].ct = current_time;
                int tat = processes[minIndex].ct - processes[minIndex].at;
                int wt = tat - processes[minIndex].bt; 

                turnaround_time += tat;
                waiting_time += wt;
            }
        }

        cout << "\tPID\tAT\tBT\tCT\tTAT\tWT\n";
        for(const auto& p:processes)
        {
            cout << p.pid << "\t\t" << p.at << "\t\t" << p.bt << "\t\t" << p.ct << "\t\t" << p.tat << "\t\t" << p.wt << "\t\t";

        }

        cout << "Average waiting time:" << (float)waiting_time/n << endl;
        cout << "Average Turnaround time :" << (float)turnaround_time/n << e

    }

    return 0;
}