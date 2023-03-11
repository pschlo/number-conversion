from typing import overload


# PrefixMap objects represent a mapping from numeral prefixes to their bases
class PrefixMap:
    prefix_to_base: dict[str,int]
    prefix_list: list[str]  # sorted by length in descending order

    def __init__(self, prefix_to_base: dict[str,int]|None = None) -> None:
        self.prefix_to_base = dict()
        self.prefix_list = []
        if prefix_to_base is not None:
            self.add(prefix_to_base)

    @overload
    def add(self, prefix:str, base:int, /): ...

    @overload
    def add(self, dict: dict[str,int], /): ...

    def add(self, *args:str|int|dict[str,int]):
        if isinstance(args[0], dict):
            self._add_prefix_dict(args[0])
        else:
            assert isinstance(args[0], str) and isinstance(args[1], int)
            self._add_prefix_single(args[0], args[1])
        self.prefix_list.sort(key=len, reverse=True)

    def _add_prefix_dict(self, dict: dict[str,int]):
        for prefix, base in dict.items():
            self._add_prefix_single(prefix, base)

    def _add_prefix_single(self, prefix:str, base:int):
        if prefix in self.prefix_to_base:
            raise ValueError(f"Prefix '{prefix}' already exists")
        self.prefix_list.append(prefix)
        self.prefix_to_base[prefix] = base



DEFAULT_PREFIXES = PrefixMap({
    '0b': 2,
    '0o': 8,
    '0x': 16,
})