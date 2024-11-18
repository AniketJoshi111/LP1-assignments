#include <iostream>
#include <queue>
#include <unordered_set>
#include <vector>
using namespace std;

void printFrames(int page, const queue<int>& frame, int hits, int pageFaults) {
    cout << "Page " << page << ": ";
    cout << "Frames: ";
    // Create a copy of the queue to iterate and print its elements
    queue<int> copy = frame;
    while (!copy.empty()) {
        cout << copy.front() << " ";
        copy.pop();
    }
    cout << "Hits: " << hits << ", Page Faults: " << pageFaults << endl;
}

void fifoPageReplacement(const vector<int>& pages, int capacity) {
    queue<int> frame;
    unordered_set<int> frameSet;
    int pageFault = 0;
    int hits = 0;
    for(int page:pages)
    {
        if(frameSet.find(page)==frameSet.end())
        {
            pageFault ++;
            if(frame.size()==capacity)
            {
                int frontpage = frame.front();
                frame.pop();
                frameSet.erase(frontpage);
            }
            frame.push(page);
            frameSet.insert(page);
        }
        else{
        hits++;
        }
        printFrames(page,frame,hits,pageFault);
    }
}

int main() {
    vector<int> pages = { 1, 2, 3, 4, 1, 5, 6, 2, 7, 8, 7 };
    int capacity = 3;
    fifoPageReplacement(pages, capacity);
    return 0;
}
