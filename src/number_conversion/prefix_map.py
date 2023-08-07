from .digits import AbstractKV



# PrefixMap objects represent a mapping from numeral prefixes to their bases
class PrefixMap(AbstractKV):
    def __init__(self, prefix_to_base: dict[str,int]|None = None) -> None:
        if prefix_to_base is None:
            super().__init__(frozenset(), tuple(), dict())
            return

        _prefix_to_base: dict[str,int] = dict()
        _prefixes: set[str] = set()
        _prefix_lengths: set[int] = set()

        for prefix, base in prefix_to_base.items():
            _prefix_to_base[prefix] = base
            _prefixes.add(prefix)
            _prefix_lengths.add(len(prefix))

        super().__init__(frozenset(_prefixes), tuple(sorted(_prefix_lengths)), _prefix_to_base)

    def get_base(self, prefix:str) -> int:
        return self._key_to_value[prefix]
    
    @property
    def prefixes(self):
        return self._keys
    
    @property
    def prefix_lengths(self):
        return self._key_lengths


DEFAULT_PREFIXES = PrefixMap({
    '0b': 2,
    '0o': 8,
    '0x': 16,
})
