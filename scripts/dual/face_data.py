class FaceData:
    def __init__(self, left=None, right=None) -> None:
        self.left_face = left
        self.right_face = right

    def __repr__(self):
        return f"FaceData({self.__dict__})"

    def update_left_face(self, face):
        self.left_face = face

    def update_right_face(self, face):
        self.right_face = face
