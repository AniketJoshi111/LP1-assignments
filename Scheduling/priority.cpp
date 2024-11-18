#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Task {
public:
    string name;
    int arrival_time, burst_time, waiting_time, completion_time, turnaround_time, priority;

    Task() : name(" "), arrival_time(0), burst_time(0), waiting_time(0),
             completion_time(0), turnaround_time(0), priority(0) {}

    Task(string name, int arrival_time, int burst_time, int priority)
        : name(name), arrival_time(arrival_time), burst_time(burst_time),
          waiting_time(0), completion_time(0), turnaround_time(0), priority(priority) {}
};

Task* HighestPriority(vector<Task*> &readyQueue) {
    int highestPriorityIndex = 0;
    for (int i = 1; i < readyQueue.size(); i++) {
        if (readyQueue[i]->priority > readyQueue[highestPriorityIndex]->priority) {
            highestPriorityIndex = i;
        }
    }
    return readyQueue[highestPriorityIndex];
}

void PriorityAlgo(vector<Task> &tasks) {
    int totalWaitingTime = 0;
    int totalTurnaroundTime = 0;
    int totalCompletionTime = 0;
    vector<Task*> readyQueue;
    vector<Task*> alreadyAddedTasks;
    int completedTasks = 0;
    int currentTime = 0;

    while (completedTasks != tasks.size()) {
        for (auto &task : tasks) {
            if (task.arrival_time <= currentTime && find(alreadyAddedTasks.begin(), alreadyAddedTasks.end(), &task) == alreadyAddedTasks.end()) {
                readyQueue.push_back(&task);
                alreadyAddedTasks.push_back(&task);
            }
        }

        if (readyQueue.empty()) {
            currentTime++;
            continue;
        }

        Task* highestPriorityTask = HighestPriority(readyQueue);

        highestPriorityTask->waiting_time = currentTime - highestPriorityTask->arrival_time;
        highestPriorityTask->completion_time = currentTime + highestPriorityTask->burst_time;
        highestPriorityTask->turnaround_time = highestPriorityTask->completion_time - highestPriorityTask->arrival_time;

        totalWaitingTime += highestPriorityTask->waiting_time;
        totalCompletionTime += highestPriorityTask->completion_time;
        totalTurnaroundTime += highestPriorityTask->turnaround_time;

        currentTime = highestPriorityTask->completion_time;
        completedTasks++;
        readyQueue.erase(remove(readyQueue.begin(), readyQueue.end(), highestPriorityTask), readyQueue.end());

        cout << "Name: " << highestPriorityTask->name
             << " Arrival Time: " << highestPriorityTask->arrival_time
             << " Burst Time: " << highestPriorityTask->burst_time
             << " Priority: " << highestPriorityTask->priority
             << " Waiting Time: " << highestPriorityTask->waiting_time
             << " Completion Time: " << highestPriorityTask->completion_time
             << " Turnaround Time: " << highestPriorityTask->turnaround_time << endl;
    }

    cout << "Average waiting time: " << static_cast<float>(totalWaitingTime) / tasks.size() << endl;
    cout << "Average turnaround time: " << static_cast<float>(totalTurnaroundTime) / tasks.size() << endl;
    cout << "Average completion time: " << static_cast<float>(totalCompletionTime) / tasks.size() << endl;
}

int main() {
    vector<Task> tasks;
    tasks.push_back(Task("p1", 0, 5, 1));
    tasks.push_back(Task("p2", 3, 5, 3));
    tasks.push_back(Task("p3", 5, 5, 2));

    PriorityAlgo(tasks);

    return 0;
}
