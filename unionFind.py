# Use leetcode 684 redundant connection as example:
# 1. easiest way, find O(1), union O(n), totol time complexity is O(m * n).
    def findRedundantConnection(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """
        parents = list(range(1001))
        for edge in edges:
            v1, v2 = edge[0], edge[1]
            if parents[v1] == parents[v2]:
                return edge
            tmp = parents[v2]
            for i in range(len(parents)):
                if parents[i] == tmp:
                    parents[i] = parents[v1]
        return None
        
  # 2. Use path compression to find the parent recursively, so find is O(n), union is O(1)
  class UnionFindSet(object):
    def __init__(self):
        self.parents = list(range(1001))
        
    def find(self, val):
        if self.parents[val] != val:
            return self.find(self.parents[val])
        else:
            # If self.parents[val] == val, means no further parent available, note how we initialize the parents.
            return self.parents[val]

    def union(self, v1, v2):
        p1, p2 = self.find(v1), self.find(v2)
        if p1 == p2:
            return True
        else:
            self.parents[p1] = p2
            return False
            
class Solution(object):
    def findRedundantConnection(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """
        ufs = UnionFindSet()
        for edge in edges:
            if ufs.union(edge[0], edge[1]):
                return edge
 
 
 
 
 
# path compression 指的是在上面的递归的 Find 操作中，将最终得到的结果赋给递归过程中经过的所有点，从而降低连通分量的高度，
# 实际上可以将一个连通分量当做一颗树，树的每个节点都连着其 parent，而 path compression 则相当于将搜寻路径中的所有点直接连到最终的那个 parent 上，因此能够降低树的高度。
# 降低树的高度有什么好处？那就是能够降低查找的时间复杂度，从 O(n)O(n) 降为了 O(logn)O(logn), 因为原来的递归搜索实际上是在一颗每个节点只有一个子节点的树上进行搜索，
# 树的高度即为点的个数，而通过 path compression 则能够有效降低树的高度。
# 另外一个问题就是进行 Union 操作时，需要将高度低的树连接到高度较高的树上，目的是为了减少 Union 后的整棵树的高度，这就是 union by rank, rank 代表的就是树的高度。
# 采用 path compression 和 union by rank 后，Find 的时间复杂度变为了 O(logn)O(logn), Union 的时间复杂度为 O(1)O(1), 
# 因此总体时间复杂度是 O(mlogn)O(mlogn), mm 为边的数目，而 nn 为点的数目。改进后的代码如下

class UnionFindSet(object):
    def __init__(self):
        self.parents = list(range(1001))
        self.rank = [0] * 1001
        
    def find(self, val):
        """find with path compression, reduce recursive times"""
        if self.parents[val] != val:
            self.parents[val] = self.find(self.parents[val])
        return self.parents[val]

    def union(self, v1, v2):
        """union by rank, check whether union two vertics will lead to a cycle"""
        p1, p2 = self.find(v1), self.find(v2)
        if p1 == p2:
            return True
        elif self.rank[p1] > self.rank[p2]:
            self.parents[p2] = p1
        elif self.rank[p1] < self.rank[p2]:
            self.parents[p1] = p2
        else:
            self.rank[p2] += 1
            self.parents[p1] = p2
        return False
            
class Solution(object):
    def findRedundantConnection(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """
        ufs = UnionFindSet()
        for edge in edges:
            if ufs.union(edge[0], edge[1]):
                return edge
