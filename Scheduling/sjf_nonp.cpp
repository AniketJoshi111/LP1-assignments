#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Process {
public:
    int pid;   // Process ID
    int bt;    // Burst time
    int at;    // Arrival time
    int ct;    // Completion time

    // Constructor
    Process(int id, int arrivalTime, int burstTime)
        : pid(id), at(arrivalTime), bt(burstTime), ct(0) {}
};

// Comparator function for sorting based on arrival time
bool compareArrivalTime(const Process& a, const Process& b) {
    return a.at < b.at;
}

int main() {
    int n;
    cout << "Enter the number of processes: ";
    cin >> n;

    vector<Process> processes;
    for (int i = 0; i < n; ++i) {
        int arrivalTime, burstTime;
        cout << "Enter arrival time and burst time for process " << i + 1 << ": ";
        cin >> arrivalTime >> burstTime;
        processes.emplace_back(i + 1, arrivalTime, burstTime);
    }

    // Sort processes based on arrival time
    sort(processes.begin(), processes.end(), compareArrivalTime);

    int currentTime = 0;
    int completed = 0;
    int totalTAT = 0;
    int totalWT = 0;

    while (completed != n) {
        int minIndex = -1;
        int minBursttime = INT_MAX;
        for(int i=0;i<n;i++)
        {
            if(processes[i].at <= currentTime && processes[i].ct ==0)
            {
                if(processes[i].bt < minBursttime)
                {
                    minBursttime = processes[i].bt;
                    minIndex = i;
                }
            }
        }

        if(minIndex==-1)
        {
            currentTime++;
        }
        else{
           currentTime += processes[minIndex].bt;
           processes[minIndex].ct = currentTime;
           completed++;

            int tat = processes[minIndex].ct - processes[minIndex].at;
            int wt = tat - processes[minIndex].bt;

            total_tat += tat;
            total_wt += wt;  
        }
    }

    // Display results
    cout << "\nPID\tAT\tBT\tCT\tTAT\tWT\n";
    for (const auto& p : processes) {
        int tat = p.ct - p.at;  // Turnaround time
        int wt = tat - p.bt;    // Waiting time
        cout << p.pid << '\t' << p.at << '\t' << p.bt << '\t' << p.ct << '\t' << tat << '\t' << wt << '\n';
    }

    cout << "\nAverage Turnaround Time: " << (float)totalTAT / n << endl;
    cout << "Average Waiting Time: " << (float)totalWT / n << endl;

    return 0;
}
