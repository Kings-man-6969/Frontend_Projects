vector<string> binaryTreePaths(TreeNode* root) {
    vector<string> paths;
    if (!root) return paths;
    if (!root->left && !root->right) {
        paths.push_back(to_string(root->val));
        return paths;
    }
    for (const auto& path : binaryTreePaths(root->left)) {
        paths.push_back(to_string(root->val) + "->" + path);
    }
    for (const auto& path : binaryTreePaths(root->right)) {
        paths.push_back(to_string(root->val) + "->" + path);
    }
    return paths;
}