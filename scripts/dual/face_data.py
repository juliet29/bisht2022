class FaceData:
    def __init__(self) -> None:
        self.left_face = None
        self.right_face = None

    def __repr__(self):
        return f"FaceData({self.__dict__})"
    
    # def update_faces(self, left, right):
    #     self.left_face = left
    #     self.right_face = right

    def update_left_face(self, left):
        # ic("left", left)
        self.left_face = left

    def update_right_face(self, right):
        # ic("right", right)
        self.right_face = right
