import pytest

from knowledge.item import KnowledgeItem


@pytest.fixture
def example_item() -> KnowledgeItem:
    return KnowledgeItem("hiragana", "Hiragana", children=[
        KnowledgeItem("hiragana_row_a", "Hiragana a-row", children=[
            KnowledgeItem("hiragana_a", "Hiragana a"),
            KnowledgeItem("hiragana_i", "Hiragana i"),
            KnowledgeItem("hiragana_u", "Hiragana u"),
            KnowledgeItem("hiragana_e", "Hiragana e"),
            KnowledgeItem("hiragana_o", "Hiragana o"),
        ]),
        KnowledgeItem("hiragana_row_ka", "Hiragana ka-row", children=[
            KnowledgeItem("hiragana_ka", "Hiragana ka"),
            KnowledgeItem("hiragana_ki", "Hiragana ki"),
            KnowledgeItem("hiragana_ku", "Hiragana ku"),
            KnowledgeItem("hiragana_ke", "Hiragana ke"),
            KnowledgeItem("hiragana_ko", "Hiragana ko"),
        ]),
    ])


class TestKnowledgeItem:
    def test_all_children(self, example_item):
        assert len(example_item.all_children()) == 13

    def test_leaf_children(self, example_item):
        assert len(example_item.leaf_children()) == 10
