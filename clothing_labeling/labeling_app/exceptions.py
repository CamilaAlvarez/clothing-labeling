

class InvalidImageCategory(Exception):
    def __init__(self, description=""):
        self.value = description

    def __str__(self):
        return self.value

class InvalidBoundingBox(Exception):
    def __init__(self, description=""):
        self.value = description

    def __str__(self):
        return self.value