#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#define INT_MAX  10000
using namespace std;

class LRU {
public:
    static void LRUPageReplacementAlgo(vector<int>& pages, int capacity) {
        int hits = 0;
        int pageFaults = 0;
        vector<int> frame;
        // Iterate through the pages
        for (int i = 0; i < pages.size(); i++) {
            if (find(frame.begin(), frame.end(), pages[i]) != frame.end()) {
                // Page hit: The page is already in the frame
                hits++;
            } else {
                if (frame.size() < capacity) {
                    // Frame has space: Add the page to the frame
                    frame.push_back(pages[i]);
                    pageFaults++;
                } else {
                    // Frame is full: Replace the LRU page with the current page
                    int frameIndexToBeReplaced = FrameIndexToBeReplaced(pages, frame, i);
                    frame[frameIndexToBeReplaced] = pages[i];
                    pageFaults++;
                }
            }
            // Print the current state of the frame, hits, and page faults
            PrintFrame(frame, hits, pageFaults);
        }
    }

    static void PrintFrame(vector<int>& frame, int hits, int pageFaults) {
        cout << "Hits: " << hits << endl;
        cout << "Page Faults: " << pageFaults << endl;
        cout << "Frame: ";
        for (int num : frame) {
            cout << num << " ";
        }
        cout << endl;
    }

    static int FrameIndexToBeReplaced(vector<int>& pages, vector<int>& frame, int index) {
        // Map to store the index of the LRU page in the pages array
        unordered_map<int, int> map;

        // Initialize the map with -1
        for (int num : frame) {
            map[num] = -1;
        }

        // Update the map with the index of the page in the pages array which is Least Recently Used
        for (int i = index - 1; i >= 0; i--) {
            if (map.find(pages[i]) != map.end() && map[pages[i]] == -1) {
                map[pages[i]] = i;
            }
        }

        // Find the LRU page and its index in the frame
        int LRUIndex = INT_MAX;
        int valueToBeReplaced = -1;

        for (auto& entry : map) {
            if (entry.second < LRUIndex) {
                LRUIndex = entry.second;
                valueToBeReplaced = entry.first;
            }
        }

        // Return the index of the LRU page in the frame
        return find(frame.begin(), frame.end(), valueToBeReplaced) - frame.begin();
    }
};

int main() {
    // Test the LRU page replacement algorithm
    vector<int> pages = { 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4 };
    int capacity = 3;
    LRU::LRUPageReplacementAlgo(pages, capacity);
    return 0;
}
