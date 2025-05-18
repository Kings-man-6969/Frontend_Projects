class Solution {
public:
    int diameterOfBinaryTree(TreeNode* root) {
        int depth = 0;
        helper(root, depth);
        return depth;
    }
    int helper(TreeNode* root, int& depth) {
        if (!root) return 0;
        int left = helper(root->left, depth);
        int right = helper(root->right, depth);
        depth = max(depth, left + right);
        return max(left, right) + 1;
    }
};