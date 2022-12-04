from dataclasses import dataclass

class SnapshotEndpoint():
    camera_id: int
    dummy: bool
    image_base_64: str

    def __init__(self, obj):
        self.camera_id = obj.get('camera_id')
        self.dummy = obj.get('dummy')
        self.image_base_64 = obj.get('image_base_64')
        
        