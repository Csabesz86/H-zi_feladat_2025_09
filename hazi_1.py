from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class Motor:
    teljesítmény: int
    típus: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Személygépkocsi:
    szín: str
    év: int
    motor: Motor
    ajtók_szam: int

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["típus"] = "Személygépkocsi"
        return d

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Személygépkocsi":
        return Személygépkocsi(
            szín=data["szín"],
            év=data["év"],
            motor=Motor(**data["motor"]),
            ajtók_szam=data.get("ajtók_szam", 0),
        )


@dataclass
class Teherautó:
    szín: str
    év: int
    motor: Motor
    teherbiras: int

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["típus"] = "Teherautó"
        return d

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Teherautó":
        return Teherautó(
            szín=data["szín"],
            év=data["év"],
            motor=Motor(**data["motor"]),
            teherbiras=data.get("teherbiras", 0),
        )


class Autópark:
    def __init__(self, json_path: str | Path | None = None) -> None:
        self._json_path = Path(json_path) if json_path else None
        self._járművek: List[Any] = []
        if self._json_path and self._json_path.exists():
            self._load_from_json()

    def _load_from_json(self) -> None:
        adat = json.loads(self._json_path.read_text(encoding="utf-8"))
        for r in adat:
            t = r["típus"]
            if t == "Személygépkocsi":
                self._járművek.append(Személygépkocsi.from_dict(r))
            elif t == "Teherautó":
                self._járművek.append(Teherautó.from_dict(r))

    def _save_to_json(self) -> None:
        if not self._json_path:
            return
        with self._json_path.open("w", encoding="utf-8") as f:
            json.dump(
                [j.to_dict() for j in self._járművek],
                f,
                indent=2,
                ensure_ascii=False,
            )

    def add_jármű(self, j: Any) -> None:
        self._járművek.append(j)
        self._save_to_json()

    def remove_jármű(self, j: Any) -> None:
        self._járművek.remove(j)
        self._save_to_json()

    def list_járművek(self) -> List[Dict[str, Any]]:
        return [j.to_dict() for j in self._járművek]


def run() -> None:
    park = Autópark("park.json")

    seg = Személygépkocsi(
        szín="kék",
        év=2020,
        motor=Motor(teljesítmény=120, típus="benzin"),
        ajtók_szam=4,
    )
    park.add_jármű(seg)

    teher = Teherautó(
        szín="piros",
        év=2019,
        motor=Motor(teljesítmény=200, típus="dizel"),
        teherbiras=1500,
    )
    park.add_jármű(teher)

    print("\nPark állapota:")
    for rek in park.list_járművek():
        print(rek)

    park.remove_jármű(seg)

    print("\nTörlés után:")
    for rek in park.list_járművek():
        print(rek)


if __name__ == "__main__":
    run()