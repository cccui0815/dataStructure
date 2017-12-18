# 节点区间定义
# [start, end] 代表节点的区间范围
# max 是节点在(start,end)区间上的最大值
# left , right 是当前节点区间划分之后的左右节点区间
class SegmentTreeNode:
    def __init__(self, start, end, x, left=None, right=None):
        self.start = start
        self.end = end
        self.max = x
        self.left = left
        self.right = right
    def __str__ (self):
        return str("[start:end] : [{} {}] ---- max : {} \n left and right: : {} and {}".format(self.start, self.end, self.max, self.left, self.right))


class SegmentTree:
    def __init__(self, A):
        """A is the input list, which we will use this to build the SegmentTree"""
        self.A = A

    def build(self, A):
        return self.buildhelper(0, len(A)-1, A)

    def buildhelper(self, start, end, A):
        if start > end:
            return None
        newRoot = SegmentTreeNode(start, end, A[start])
        if start == end:
            return newRoot
        mid = (start + end) // 2
        newRoot.left = self.buildhelper(start, mid, A)
        newRoot.right = self.buildhelper(mid+1, end, A)
        newRoot.max = max(newRoot.left.max, newRoot.right.max)
        return newRoot

    def queryMax(self, root, start, end):
        if start <= root.start and root.end <= end:
            return root.max
        mid = (root.start + root.end) // 2
        ans = float("-inf")
        if mid >= start:   # The query range has overlap with left half.
            ans = max(ans, self.queryMax(root.left, start, end))
        if (mid+1) <= end:
            ans = max(ans, self.queryMax(root.right, start, end))
        return ans

    def modify(self, root, index, value):
        if root.start == root.end and root.start == index:
            root.max = value
            return
        mid = (root.start + root.end) // 2
        if index <= mid:
            self.modify(root.left, index, value)
            root.max = max(root.right.max, root.left.max)  ## need to modify root's max if its children have updates
        else:
            self.modify(root.right, index, value)
            root.max = max(root.left.max, root.right.max)
        return

if __name__ == "__main__":
    A = [1,4,2,3]
    root = SegmentTreeNode(0,len(A)-1,A[0])
    SMT = SegmentTree(A)
    root = SMT.build(A)
    print(root)
    # Test queryMax
    assert SMT.queryMax(root, 0,2) == 4
    assert SMT.queryMax(root, 2,3) == 3
    assert SMT.queryMax(root, 0,3) == 4
    # Test modify
    SMT.modify(root, 0, 5)
    assert SMT.queryMax(root, 0,2) == 5
    assert SMT.queryMax(root, 2,3) == 3
    assert SMT.queryMax(root, 0,3) == 5
