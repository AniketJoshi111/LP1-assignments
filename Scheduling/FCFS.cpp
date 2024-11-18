/*In FCFS, the process that arrives first gets executed first.
 This algorithm follows a non-preemptive approach, 
 meaning once a process starts executing, 
 it will continue until it completes, without being interrupted.
 
 Disadvantages:
Poor Average Waiting Time:
 Processes that arrive early with long burst times
  can delay all other processes, leading to the “convoy effect.”
 */

#include <iostream>
#include <string>
#include <vector>
#include<algorithm>

using namespace std;

class Task {
public:
    string name;
    int arrival_time, burst_time, waiting_time, completion_time, turnaround_time;

    Task(string name, int arrival_time, int burst_time) {
        this->name = name;
        this->arrival_time = arrival_time;
        this->burst_time = burst_time;
        waiting_time = 0;
        completion_time = 0;
        turnaround_time = 0;
    }
};

void FCFSSort(vector<Task>& tasks) {
    int n = tasks.size();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (tasks[j].arrival_time > tasks[j + 1].arrival_time) {
                swap(tasks[j], tasks[j + 1]);
            }
        }
    }
}
bool comparator(const Task& a,const Task& b)
{
    return a.arrival_time < b.arrival_time;
}
void FCFS(vector<Task>& tasks) {
    sort(tasks.begin(),tasks.end(),comparator);

    int n = tasks.size();
    int total_waiting_time = 0;
    int total_turnaround_time = 0;
    int total_completion_time = 0;

    for (int i = 0; i < n; i++) {
        if (i == 0) {
            tasks[i].waiting_time = 0;
            tasks[i].completion_time = tasks[i].burst_time;
            tasks[i].turnaround_time = tasks[i].completion_time - tasks[i].arrival_time;
        } else {
            tasks[i].waiting_time = tasks[i - 1].completion_time - tasks[i].arrival_time;
            tasks[i].completion_time = tasks[i - 1].completion_time + tasks[i].burst_time;
            tasks[i].turnaround_time = tasks[i].completion_time - tasks[i].arrival_time;
        }
        total_waiting_time += tasks[i].waiting_time;
        total_turnaround_time += tasks[i].turnaround_time;
        total_completion_time += tasks[i].completion_time;
    }

    cout << "Task\tArrival Time\tBurst Time\tWaiting Time\tCompletion Time\tTurnaround Time\n";
    for (int i = 0; i < n; i++) {
        cout << tasks[i].name << "\t" << tasks[i].arrival_time << "\t\t" << tasks[i].burst_time
             << "\t\t" << tasks[i].waiting_time << "\t\t" << tasks[i].completion_time
             << "\t\t" << tasks[i].turnaround_time << "\n";
    }

    cout << "Average waiting time: " << (double)total_waiting_time / n << endl;
    cout << "Average turnaround time: " << (double)total_turnaround_time / n << endl;
    cout << "Average completion time: " << (double)total_completion_time / n << endl;
}

int main() {
    vector<Task> tasks;
    tasks.push_back(Task("T1", 0, 5));
    tasks.push_back(Task("T2", 1, 3));
    tasks.push_back(Task("T3", 2, 8));
    tasks.push_back(Task("T4", 3, 6));

    FCFS(tasks);

    return 0;
}
