class Solution {
public:
    vector<vector<int>> kSmallestPairs(vector<int>& nums1, vector<int>& nums2, int k) {
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> min_heap;
        vector<vector<int>> res;
        int i = 0, j = 0;
        for (int count = 0; count < k && i < nums1.size() && j < nums2.size(); count++) {
            int sum = nums1[i] + nums2[j];
            min_heap.push({sum, i, j});
            while (!min_heap.empty() && min_heap.top()[0] >= sum) {
                res.push_back({nums1[min_heap.top()[1]], nums2[min_heap.top()[2]]});
                min_heap.pop();
            }
            if (j + 1 < nums2.size() && nums2[j + 1] < nums1[i]) {
                j++;
            } else {
                i++;
            }
        }
        return res;
    }
};