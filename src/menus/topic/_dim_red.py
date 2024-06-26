from src.menus._menu import Menu
from util._session import Session


class DimensionalityReductionMenu(Menu):
    def __init__(self, session: Session, parent: Menu = None):
        is_root = False
        is_leaf = True
        options = [
            "UMAP",
            "PCA",
            "Truncated SVD",
            "Independent Component Analysis",
        ]

        self.name = "Dimensionality Reduction"

        super().__init__(session, options, is_leaf, is_root, name=self.name)
