int shortestSubarray(vector<int>& nums, int k) {
    int n = nums.size();
    vector<int> prefixSum(n + 1, 0);
    for (int i = 0; i < n; i++) {
        prefixSum[i + 1] = prefixSum[i] + nums[i];
    }
    int result = n + 1;
    for (int i = 0; i <= n; i++) {
        int j = lowerBound(prefixSum.begin() + i, prefixSum.end(), prefixSum[i] + k);
        if (j != prefixSum.end()) {
            result = min(result, (int) (j - prefixSum.begin() - i));
        }
    }
    return result <= n ? result : -1;
}

int lowerBound(vector<int>::iterator begin, vector<int>::iterator end, int target) {
    int size = distance(begin, end);
    int l = 0, r = size;
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (begin[mid] < target) {
            l = mid + 1;
        } else {
            r = mid;
        }
    }
    return begin + l;
}