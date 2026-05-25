from dataclasses import dataclass, field

from knowledge.skill import KnowledgeSkill


@dataclass
class KnowledgeItem:
    identifier: str
    name: str
    skills: list[KnowledgeSkill] = field(default_factory=list)
    children: list["KnowledgeItem"] = field(default_factory=list)
    prerequisites: list["KnowledgePrerequisite"] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def all_children(self, include_self: bool = True) -> list["KnowledgeItem"]:
        c = [self] if include_self else []
        for child in self.children:
            c.extend(child.all_children(include_self=True))
        return c

    def all_leaf_children(self) -> list["KnowledgeItem"]:
        c = [self] if self.is_leaf() else []
        for child in self.children:
            c.extend(child.all_leaf_children())
        return c

    @staticmethod
    def from_dict(obj: dict) -> "KnowledgeItem":
        item_type = "KnowledgeItem"
        if "type" in obj:
            item_type = obj["type"]
        if item_type not in globals():
            raise ValueError(f"Unknown item type {item_type}")

        item_class = globals()[item_type]

        # Filter obj for the parts that are actually used in the target class's init.
        init_arg_names = item_class.__init__.__code__.co_varnames
        init_args = {k: v for k, v in obj.items() if k in init_arg_names}

        if "prerequisites" in init_args:
            prereqs = [KnowledgePrerequisite(p["item"], p["mastery"]) for p in init_args["prerequisites"]]
            init_args["prerequisites"] = prereqs

        if "children" in init_args:
            children = [KnowledgeItem.from_dict(d) for d in init_args["children"]]
            init_args["children"] = children

        item = item_class(**init_args)
        return item


@dataclass
class KanaItem(KnowledgeItem):
    kana: str = ""
    romaji: str = ""
    skills: list[KnowledgeSkill] = field(default_factory=lambda: [KnowledgeSkill.RECOGNITION, KnowledgeSkill.RECALL])


@dataclass
class KnowledgePrerequisite:
    item: str
    # Required mastery of the prerequisite item
    mastery: float
