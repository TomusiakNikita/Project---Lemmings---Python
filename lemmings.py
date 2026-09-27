from pathlib import Path


class Cell:
    """A single cell in the cave map."""

    def __init__(self, terrain: str):
        self.terrain = terrain
        self.lemming = None

    def __str__(self) -> str:
        return str(self.lemming) if self.lemming is not None else self.terrain

    def is_free(self) -> bool:
        return self.terrain != "#" and self.lemming is None

    def remove_lemming(self) -> None:
        self.lemming = None

    def place_lemming(self, lemming: "Lemming") -> bool:
        if not self.is_free() or self.terrain == "O":
            return False
        self.lemming = lemming
        return True


class Lemming:
    """A moving lemming inside the game grid."""

    def __init__(self, row: int, column: int, direction: int, game: "Game"):
        self.row = row
        self.column = column
        self.direction = direction
        self.game = game

    def __str__(self) -> str:
        return ">" if self.direction == 1 else "<"

    def _move_to(self, row: int, column: int) -> bool:
        current = self.game.cave[self.row][self.column]
        target = self.game.cave[row][column]

        current.remove_lemming()
        self.row = row
        self.column = column

        if target.terrain == "O":
            self.game.mark_exited(self)
            return True

        target.place_lemming(self)
        return False

    def act(self) -> None:
        # Fall until supported, blocked, or exited.
        while self.row + 1 < self.game.height:
            below = self.game.cave[self.row + 1][self.column]

            if below.terrain == "O":
                self._move_to(self.row + 1, self.column)
                return

            if not below.is_free():
                break

            if self._move_to(self.row + 1, self.column):
                return

        # Move horizontally when supported.
        next_column = self.column + self.direction
        if not 0 <= next_column < self.game.width:
            self.direction *= -1
            return

        target = self.game.cave[self.row][next_column]

        if target.terrain == "O":
            self._move_to(self.row, next_column)
            return

        if target.is_free():
            self._move_to(self.row, next_column)
        else:
            self.direction *= -1


class Game:
    """Loads a cave map and runs the command-line simulation."""

    def __init__(self, map_path: Path):
        self.cave = self._load_map(map_path)
        self.height = len(self.cave)
        self.width = len(self.cave[0])

        self.lemmings = []
        self.lemmings_total = 0
        self.lemmings_exited = 0
        self.turns = 0

        self.start_row, self.start_column = self._find_start()

    @staticmethod
    def _load_map(map_path: Path):
        lines = map_path.read_text(encoding="utf-8").splitlines()
        if not lines:
            raise ValueError("The map file is empty.")

        width = len(lines[0])
        if any(len(line) != width for line in lines):
            raise ValueError("All map rows must have the same width.")

        return [[Cell(char) for char in line] for line in lines]

    def _find_start(self):
        top_row = self.cave[0]

        try:
            start_column = next(
                index for index, cell in enumerate(top_row) if cell.terrain != "#"
            )
        except StopIteration as exc:
            raise ValueError("No entrance was found in the top row.") from exc

        start_row = 0
        for row in range(self.height):
            if self.cave[row][start_column].terrain == "#":
                break
            start_row = row

        return start_row, start_column

    def display(self) -> None:
        print("\n".join("".join(str(cell) for cell in row) for row in self.cave))

    def add_lemming(self) -> bool:
        start_cell = self.cave[self.start_row][self.start_column]
        if not start_cell.is_free() or start_cell.terrain == "O":
            return False

        lemming = Lemming(
            self.start_row,
            self.start_column,
            direction=1,
            game=self,
        )
        start_cell.place_lemming(lemming)
        self.lemmings.append(lemming)
        self.lemmings_total += 1
        return True

    def mark_exited(self, lemming: Lemming) -> None:
        if lemming in self.lemmings:
            self.lemmings.remove(lemming)
            self.lemmings_exited += 1

    def play_turn(self) -> None:
        for lemming in self.lemmings[:]:
            lemming.act()

        self.turns += 1
        self.display()

    def run(self) -> None:
        self.display()

        while True:
            command = input(
                "\n'l' = add a lemming, Enter = play one turn, 'q' = quit: "
            ).strip().lower()

            if command == "l":
                if not self.add_lemming():
                    print("The starting cell is occupied.")
                self.display()
            elif command == "q":
                print(f"Lemmings created: {self.lemmings_total}")
                print(f"Lemmings exited: {self.lemmings_exited}")
                print(f"Turns played: {self.turns}")
                break
            elif command == "":
                self.play_turn()
            else:
                print("Unknown command.")


if __name__ == "__main__":
    map_file = Path(__file__).with_name("grotte.txt")
    Game(map_file).run()
