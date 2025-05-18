class Solution {
public:
    int distributeCoins(TreeNode* root) {
        return dfs(root)[1];
    }
    
    array<int, 3> dfs(TreeNode* node) {
        if (!node) return {0, 0, 0};
        auto left = dfs(node->left);
        auto right = dfs(node->right);
        return {left[1] + right[1] + node->val - 1, abs(left[1] - right[1]) + left[2] + right[2] + abs(left[0] + right[0] - 1), left[0] + right[0] + 1};
    }
};