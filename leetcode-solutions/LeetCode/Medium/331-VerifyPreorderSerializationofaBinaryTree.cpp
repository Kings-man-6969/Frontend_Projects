bool isValidSerialization(string preorder) {
    int nodes = 1;
    stringstream ss(preorder);
    string token;
    while (getline(ss, token, ',')) {
        --nodes;
        if (nodes < 0) return false;
        if (token != "#") nodes += 2;
    }
    return nodes == 0;
}