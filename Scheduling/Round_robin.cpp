#include <iostream>
#include <queue>
#include <vector>
#include <algorithm>
using namespace std;

class Task {
public:
    string name;
    int arrival_time, burst_time, waiting_time, completion_time, turnaround_time;

    Task(string name, int arrival_time, int burst_time)
        : name(name), arrival_time(arrival_time), burst_time(burst_time),
          waiting_time(0), completion_time(0), turnaround_time(0) {}
};

bool compareArrivalTime(const Task &a, const Task &b) {
    return a.arrival_time < b.arrival_time;
}

void RRAlgo(vector<Task> &tasks, int quantum) {
    // Sort tasks by arrival time
    sort(tasks.begin(), tasks.end(), compareArrivalTime);

    int totalWaitingTime = 0;
    int totalTurnAroundTime = 0;
    int totalCompletionTime = 0;

    queue<Task*> readyQueue;
    int currentTime = 0;

    for (auto &task : tasks) {
        if (task.arrival_time == 0) {
            readyQueue.push(&task);
        }
    }

    while (!readyQueue.empty()) {
        Task *currentTask = readyQueue.front();
        readyQueue.pop();

        if (currentTask->burst_time > quantum) {
            currentTask->burst_time -= quantum;
            currentTime += quantum;
        } else {
            currentTask->waiting_time = currentTime - currentTask->arrival_time;
            currentTime += currentTask->burst_time;
            currentTask->burst_time = 0;
            currentTask->completion_time = currentTime;
            currentTask->turnaround_time = currentTask->completion_time - currentTask->arrival_time;
            totalWaitingTime += currentTask->waiting_time;
            totalCompletionTime += currentTask->completion_time;
            totalTurnAroundTime += currentTask->turnaround_time;
        }

        for (auto &task : tasks) {
            if (task.arrival_time <= currentTime && task.arrival_time > (currentTime - quantum) && task.burst_time > 0) {
                readyQueue.push(&task);
            }
        }

        if (currentTask->burst_time > 0) {
            readyQueue.push(currentTask);
        }
    }

    // Print the results
    cout << "Task Name\tArrival Time\tBurst Time\tWaiting Time\tCompletion Time\tTurnaround Time\n";
    for (const auto &task : tasks) {
        cout << task.name << "\t\t" << task.arrival_time << "\t\t" << task.burst_time << "\t\t"
             << task.waiting_time << "\t\t" << task.completion_time << "\t\t" << task.turnaround_time << "\n";
    }

    cout << "Average Waiting Time: " << static_cast<float>(totalWaitingTime) / tasks.size() << "\n";
    cout << "Average Turnaround Time: " << static_cast<float>(totalTurnAroundTime) / tasks.size() << "\n";
    cout << "Average Completion Time: " << static_cast<float>(totalCompletionTime) / tasks.size() << "\n";
}

int main() {
    vector<Task> tasks;
    tasks.emplace_back("T1", 0, 5);
    tasks.emplace_back("T2", 1, 3);
    tasks.emplace_back("T3", 2, 8);
    tasks.emplace_back("T4", 3, 6);
    tasks.emplace_back("T5", 4, 4);

    int quantum = 2;
    RRAlgo(tasks, quantum);

    return 0;
}
