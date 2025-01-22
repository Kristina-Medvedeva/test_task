from collections import defaultdict
from typing import Any, Dict, Iterable, List


class TreeStore:
    """
    Массив объектов, которые имеют поле идентификатор и родитель, через которые их можно связать в дерево
    и некоторые произвольные поля.
    """

    def __init__(self, items: Iterable[Dict[str, Any]]):
        self._nodes = {}
        self._mapper = defaultdict(list)

        for item in items:
            self._nodes[item["id"]] = item
            self._mapper[item["parent"]].append(item)

    def get_all(self) -> List[Dict[str, Any]]:
        """
         Должен возвращать изначальный массив элементов

        Returns:
            List[Dict[str, Any]]
        """
        return list(self._nodes.values())

    def get_item(self, row_id: int) -> Dict[str, Any]:
        """
        Принимает id элемента и возвращает сам объект элемента

        Args:
            row_id (int): Идентификатор элемента

        Returns:
            Dict[str, Any]
        """
        return self._nodes.get(row_id) or {}

    def get_children(self, row_id: int) -> List[Dict[str, Any]]:
        """
        Принимает id элемента и возвращает массив элементов, являющихся дочерними для того элемента,
        чей id получен в аргументе. Если у элемента нет дочерних, то должен возвращаться пустой массив;

        Args:
            row_id (int): Идентификатор элемента

        Returns:
            List[Dict[str, Any]]
        """
        return self._mapper[row_id]

    def get_all_parents(self, row_id: int) -> List[Dict[str, Any]]:
        """
        Принимает id элемента и возвращает массив из цепочки родительских элементов,
        начиная от самого элемента, чей id был передан в аргументе и до корневого элемента,
        т.е. должен получиться путь элемента наверх дерева через цепочку родителей к корню дерева.
        Порядок элементов важен!

        Args:
            row_id (int): Идентификатор элемента

        Returns:
            List[Dict[str, Any]]
        """
        result: List[Dict[str, Any]] = []

        parent = self.get_parent(row_id)
        result.append(parent)

        while parent:
            if parent := self.get_parent(parent["id"]):
                result.append(parent)

        return result

    def get_parent(self, row_id: int) -> Dict[str, Any]:
        """
        Возвращает родителя для элемента
        Args:
            row_id (int): Идентификатор элемента

        Returns:
            Dict[str, Any]
        """
        if child := self.get_item(row_id):
            return self.get_item(child["parent"])

        return {}


if __name__ == "__main__":
    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None},
    ]

    ts = TreeStore(items)
    assert ts.get_all() == items

    assert ts.get_item(7) == items[6]
    assert ts.get_item(9) == {}

    assert ts.get_children(4) == [
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None},
    ]
    assert ts.get_children(5) == []

    assert ts.get_all_parents(7) == [
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 1, "parent": "root"},
    ]
