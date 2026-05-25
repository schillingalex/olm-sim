import json

from knowledge.item import KnowledgeItem


class KnowledgeManager:
    """
    Holds all available learning content in a hierarchical form (KnowledgeItem with children and so on) and
    as a flat index to retrieve a KnowledgeItem directly given its identifier.

    The knowledge is built using JSON files, which can be added sequentially after initialization.
    The file paths can also be handed in directly to init.
    """

    def __init__(self, src_files: list[str] = None):
        self.knowledge_index = {}
        self.knowledge_trees = []

        if src_files is not None:
            for src_file in src_files:
                self.add_from_json_file(src_file)

    def add_from_object(self, obj):
        if isinstance(obj, list):
            for item in obj:
                self.add_from_object(item)
        elif isinstance(obj, dict):
            item = KnowledgeItem.from_dict(obj)
            self.knowledge_trees.append(item)

            # Add each node given in the object to the index such that they can be accessed later in O(1).
            for child in item.all_children():
                if child.identifier in self.knowledge_index:
                    raise ValueError(f"Duplicate identifier {child.identifier}")

                self.knowledge_index[child.identifier] = child

    def add_from_json_string(self, json_string):
        self.add_from_object(json.loads(json_string))

    def add_from_json_file(self, json_path: str):
        with open(json_path, "r") as f:
            self.add_from_object(json.load(f))
