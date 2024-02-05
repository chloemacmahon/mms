class TO_DO_List:
    def __init__(self, id, name, description, items):
        self.id = id
        self.name = name
        self.description = description
        self.items = items

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'items': [item.to_dict() if hasattr(item, 'to_dict') else item for item in self.items] if self.items else []
        }
