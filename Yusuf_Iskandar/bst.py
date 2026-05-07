class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, value):
        if root is None:
            return Node(value)
        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)
        return root

    def preorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            result.append(root.value)
            self.preorder(root.left, result)
            self.preorder(root.right, result)
        return result

    def inorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.inorder(root.left, result)
            result.append(root.value)
            self.inorder(root.right, result)
        return result

    def postorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.value)
        return result


if __name__ == "__main__":
    # --- BST Awal ---
    tree = BST()
    data_awal = [50, 30, 70, 20, 40, 60, 80]
    for item in data_awal:
        tree.root = tree.insert(tree.root, item)

    print("=== BST Awal: [50, 30, 70, 20, 40, 60, 80] ===")
    print("Preorder :", tree.preorder(tree.root))
    print("Inorder  :", tree.inorder(tree.root))
    print("Postorder:", tree.postorder(tree.root))

    # --- Tambah Node Baru ---
    new_nodes = [10, 90, 65]
    for item in new_nodes:
        tree.root = tree.insert(tree.root, item)

    print("\n=== Setelah Penambahan Node: [10, 90, 65] ===")
    print("Preorder :", tree.preorder(tree.root))
    print("Inorder  :", tree.inorder(tree.root))
    print("Postorder:", tree.postorder(tree.root))

    print("\n=== Analisis Perubahan ===")
    print("- Node 10: disisipkan sebagai anak kiri dari node 20 (10 < 50 < 30 < 20)")
    print("- Node 90: disisipkan sebagai anak kanan dari node 80 (90 > 50 > 70 > 80)")
    print("- Node 65: disisipkan sebagai anak kanan dari node 60 (65 > 50 > 70 < 60 > 65)")
    print("- Inorder tetap terurut ascending karena properti BST terjaga.")
