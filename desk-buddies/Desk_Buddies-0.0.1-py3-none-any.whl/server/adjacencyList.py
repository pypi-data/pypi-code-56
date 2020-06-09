import csv


class AdjacencyList:
    # this class stores adjacencies in the format: {Jen: {Conor:1}, {Aliyah:1}}, {Conor: {Jen:1}, {Justin:1}}
    def __init__(self, directory):
        self.directory = directory
        self.matrix = {}
        with open(directory, "r", encoding="utf-8-sig") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
            for row in spamreader:
                adjacencies = {}
                for uid in row:
                    if uid != row[0] and uid != '':
                        adjacencies[uid] = 1

                self.matrix[row[0]] = adjacencies

    def write_to_csv(self, directory):
        with open(directory, "w", encoding="utf-8-sig") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', skipinitialspace=True)
            for uid in self.matrix.keys():
                row = [uid]
                for adj in self.matrix[uid]:
                    row.append(adj)

                spamwriter.writerow(row)

    def is_adjacent(self, a, b) -> bool:
        return self._is_adjacent(a, b) or self._is_adjacent(b, a)

    def _is_adjacent(self, a, b) -> bool:
        is_adj = 0
        is_adj = self.matrix[a][b]
        return is_adj
