from angles import calc_angles_complex


class FaceMatch:
    pass


class FaceData:
    def __init__(self, left, right) -> None:
        self.left_face = left
        self.right_face = right

    def __repr__(self):
        return f"FaceData({self.__dict__})"