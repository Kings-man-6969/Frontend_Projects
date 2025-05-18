class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        vector<int> freq(26, 0);
        for (char c : tasks) {
            freq[c - 'A']++;
        }
        int max_f = *max_element(freq.begin(), freq.end());
        int max_count = count(freq.begin(), freq.end(), max_f);
        return max_f * (n + 1) + max_count - 1;
    }
};