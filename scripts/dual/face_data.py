class FaceData:
    def __init__(self) -> None:
        self.left_face = []
        self.right_face = []

    def __repr__(self):
        return f"FaceData({self.__dict__})"

    def update_left_face(self, face):
        self.left_face = face

    def update_right_face(self, face):
        self.right_face = face
