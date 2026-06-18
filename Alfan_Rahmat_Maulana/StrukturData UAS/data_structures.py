# ═══════════════════════════════════════════════════════════════════
#  data_structures.py  —  Implementasi Array, BST, Hash Table, AVL
# ═══════════════════════════════════════════════════════════════════


# ─── 1. ARRAY / LIST ────────────────────────────────────────────────────────
class Array:
    """Array linear dengan linear search, O(n) untuk semua operasi."""

    def __init__(self):
        self.data = []

    def insert(self, value):
        if value not in self.data:
            self.data.append(value)

    def search(self, value):
        """Linear search — O(n)."""
        for i, v in enumerate(self.data):
            if v == value:
                return i
        return -1

    def delete(self, value):
        """O(n) — harus cari dulu lalu shift."""
        try:
            self.data.remove(value)
            return True
        except ValueError:
            return False


# ─── 2. BINARY SEARCH TREE ──────────────────────────────────────────────────
class _BSTNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = self.right = None


class _BST:
    def __init__(self):
        self.root = None

    # Insert ITERATIF — tidak ada rekursi, aman untuk dataset besar
    def insert(self, val):
        if self.root is None:
            self.root = _BSTNode(val)
            return
        node = self.root
        while True:
            if val < node.val:
                if node.left is None:
                    node.left = _BSTNode(val)
                    return
                node = node.left
            elif val > node.val:
                if node.right is None:
                    node.right = _BSTNode(val)
                    return
                node = node.right
            else:
                return  # duplikat, abaikan

    # Search ITERATIF — O(log n) rata‑rata
    def search(self, val):
        node = self.root
        while node:
            if val == node.val:
                return True
            node = node.left if val < node.val else node.right
        return False

    # Delete ITERATIF — tidak ada rekursi
    def delete(self, val):
        parent = None
        node = self.root
        while node and node.val != val:
            parent = node
            node = node.left if val < node.val else node.right
        if node is None:
            return
        if node.left and node.right:
            succ_parent = node
            succ = node.right
            while succ.left:
                succ_parent = succ
                succ = succ.left
            node.val = succ.val
            parent = succ_parent
            node = succ
        child = node.left if node.left else node.right
        if parent is None:
            self.root = child
        elif parent.left == node:
            parent.left = child
        else:
            parent.right = child


class BSTWrapper:
    def __init__(self):
        self._bst = _BST()

    def insert(self, value):
        self._bst.insert(value)

    def search(self, value):
        return self._bst.search(value)

    def delete(self, value):
        self._bst.delete(value)


# ─── 3. HASH TABLE ──────────────────────────────────────────────────────────
class _HashTable:
    """
    Hash table dengan separate chaining.
    Average O(1) untuk insert / search / delete.
    """

    def __init__(self, capacity=2048):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def _hash(self, val):
        return hash(val) % self.capacity

    def insert(self, val):
        idx = self._hash(val)
        bucket = self.buckets[idx]
        if val not in bucket:
            bucket.append(val)
            self.size += 1
            # Resize jika load factor > 0.75
            if self.size / self.capacity > 0.75:
                self._resize()

    def search(self, val):
        idx = self._hash(val)
        return val in self.buckets[idx]

    def delete(self, val):
        idx = self._hash(val)
        bucket = self.buckets[idx]
        try:
            bucket.remove(val)
            self.size -= 1
            return True
        except ValueError:
            return False

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_buckets:
            for val in bucket:
                self.insert(val)


class HashTableWrapper:
    def __init__(self):
        self._ht = _HashTable()

    def insert(self, value):
        self._ht.insert(value)

    def search(self, value):
        return self._ht.search(value)

    def delete(self, value):
        self._ht.delete(value)


# ─── 4. AVL TREE ────────────────────────────────────────────────────────────
class _AVLNode:
    __slots__ = ("val", "left", "right", "height")

    def __init__(self, val):
        self.val = val
        self.left = self.right = None
        self.height = 1


class _AVLTree:
    """
    Self‑balancing BST — selalu O(log n) untuk semua operasi
    karena balance factor dijaga antara ‑1 dan +1.
    """

    def __init__(self):
        self.root = None

    # ── helpers ──────────────────────────────────────────────────
    @staticmethod
    def _h(n):
        return n.height if n else 0

    @staticmethod
    def _bf(n):
        return (_AVLTree._h(n.left) - _AVLTree._h(n.right)) if n else 0

    @staticmethod
    def _update_h(n):
        n.height = 1 + max(_AVLTree._h(n.left), _AVLTree._h(n.right))

    # ── rotations ────────────────────────────────────────────────
    @staticmethod
    def _rotate_right(y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        _AVLTree._update_h(y)
        _AVLTree._update_h(x)
        return x

    @staticmethod
    def _rotate_left(x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        _AVLTree._update_h(x)
        _AVLTree._update_h(y)
        return y

    def _balance(self, node, val=None):
        _AVLTree._update_h(node)
        bf = _AVLTree._bf(node)
        # LL
        if bf > 1 and (val is None or val < node.left.val):
            return _AVLTree._rotate_right(node)
        # RR
        if bf < -1 and (val is None or val > node.right.val):
            return _AVLTree._rotate_left(node)
        # LR
        if bf > 1 and (val is None or val > node.left.val):
            node.left = _AVLTree._rotate_left(node.left)
            return _AVLTree._rotate_right(node)
        # RL
        if bf < -1 and (val is None or val < node.right.val):
            node.right = _AVLTree._rotate_right(node.right)
            return _AVLTree._rotate_left(node)
        return node

    # ── public API ───────────────────────────────────────────────
    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if not node:
            return _AVLNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        else:
            return node
        return self._balance(node, val)

    def search(self, val):
        node = self.root
        while node:
            if val == node.val:
                return True
            node = node.left if val < node.val else node.right
        return False

    def delete(self, val):
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if not node:
            return None
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            if not node.left or not node.right:
                node = node.left or node.right
            else:
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.val = succ.val
                node.right = self._delete(node.right, succ.val)
        if not node:
            return None
        return self._balance(node)


class AVLWrapper:
    def __init__(self):
        self._avl = _AVLTree()

    def insert(self, value):
        self._avl.insert(value)

    def search(self, value):
        return self._avl.search(value)

    def delete(self, value):
        self._avl.delete(value)
