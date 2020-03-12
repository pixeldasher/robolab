#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import List, Tuple, Dict, Union, Set


@unique
class Direction(IntEnum):
    """ Directions in shortcut """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


Weight = int
"""
Weight of a given path (received from the server)

Value:  -1 if blocked path
        >0 for all other paths
        never 0
"""


class Planet:
    """
    Contains the representation of the map and provides certain functions to manipulate or extend
    it according to the specifications
    """

    def __init__(self):
        """ Initializes the data structure """
        self.target = None
        self.paths = set()
        self.planet_dict: Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]] = {}
        self.explore_dict: Dict[Tuple[int, int], Set[Direction]] = {}

    # alle neuen Directions bei Ankunft an einem (neuen) Knoten in explore_dict aufnehmen
    def add_vertex(self, vert: Tuple[int, int], directions: Set[Direction]):
            # directions ist ein Set (Menge) aller möglichen neuen(!) directions am neuen Knoten

            if vert not in self.explore_dict:
                self.explore_dict[vert] = directions

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],
                 weight: int):
        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it

        Example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """
        self.paths.add((start, target, weight))
        self.paths.add((target, start, weight))


    def vertex_explored(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction]):
        # Entfernen der Directions, die durchs Abfahren dieses Pfades "erkundet" wurden:
        self.explore_dict[start[0]] = self.explore_dict[start[0]] - {start[1]}
        self.explore_dict[target[0]] = self.explore_dict[target[0]] - {target[1]}

    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        """
        Returns all paths

        Example:
            {
                (0, 3): {
                    Direction.NORTH: ((0, 3), Direction.WEST, 1),
                    Direction.EAST: ((1, 3), Direction.WEST, 2)
                },
                (1, 3): {
                    Direction.WEST: ((0, 3), Direction.EAST, 2),
                    ...
                },
                ...
            }
        :return: Dict
        """

        for path_tuple in self.paths:
            if not path_tuple[0][0] in self.planet_dict:
                path_dict = {}
                self.planet_dict[path_tuple[0][0]] = path_dict
            self.planet_dict[path_tuple[0][0]][path_tuple[0][1]] = (path_tuple[1][0], path_tuple[1][1], path_tuple[2])

        return self.planet_dict

    def shortest_path(self, start: Tuple[int, int], target: Union[None, Tuple[int, int]]) -> Union[None, List[Tuple[Tuple[int, int], Direction]]]:
        """
        Returns a shortest path between two nodes

        Examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: 2-Tuple[List, Direction]
        """

        # wenn Ziel- und Startknoten derselbe sind, wird ein "leerer Weg" zurückgegeben
        if target == start:
            print("shortest path from: ", start, " to: ", target, "? ... well... just stay right here.")
            return []

        # Initialisierung für Djikstra:
        dist = {}  # Dictionary für Distanz aller Knoten zu Startknoten
        prev = {}  # Dictionary für Vorgängerknoten
        to_do = []  # Liste aller Knoten, für die noch kein kürzester Weg vom Startknoten aus gefunden wurde
        output = []

        # Erstellen des Dictionarys mit allen bekannten Knoten und Pfaden
        self.get_paths()

        for v in self.planet_dict:
            dist[v] = float("inf")
            prev[v] = None
            to_do.append(v)

        dist[start] = 0
        u = start

        # Dijkstraalgorithmus:

        while to_do:  # solange es noch Knoten gibt, zu denen kein kürzester Weg berechnet wurde
            to_do.remove(u)

            # alle relevanten Nachbaren v von u finden:
            for path_tuple in self.paths:  # alle Pfade (alle path_tuples, die im paths-set enthalten sind)
                if path_tuple[0][0] == u:  # nur die Pfade, dessen Startknoten u entspricht

                    v = path_tuple[1][0]
                    if v in to_do:  # falls diese Nachbarn noch zu scannen sind (also noch Element der Liste to_do sind)

                        # Berechnung und Vergleich des Alternativwegs: neuer Distanzwert durch Berücksichtigung der jeweiligen Kante zwischen u und v (path_tuple[2])
                        altern = dist[u] + path_tuple[2]

                        if altern < dist[v]:  # falls Alterativweg kürzer ist, als bisheriger, wird Vorgänger von v auf u gesetzt und die Distanz zu v auf altern gesetzt
                            dist[v] = altern
                            prev[v] = u

            # Nachbar von u mit dem kleinsten Abstand zu u finden und als neues u setzen:
            temp_min_dist = float("inf")
            temp_min = None
            for v in self.planet_dict:
                if v in to_do:
                    if dist[v] < temp_min_dist:
                        temp_min_dist = dist[v]
                        temp_min = v

            u = temp_min

            if target is None and u in self.explore_dict:
                target = u

            # Zielknoten expandiert - einzelne Wegknoten des kürzesten Wegs werden in shortest_p zusammengefasst und auf output vorbereitet (Directions hinzufügen)
            if u == target:
                temp = u
                shortest_p = []
                while prev[temp]:
                    shortest_p.append(temp)
                    temp = prev[temp]
                shortest_p.append(start)

                shortest_p.reverse()

                for i in range(len(shortest_p)):
                    for path_tuple in self.paths:
                        if path_tuple[0][0] == shortest_p[i]:
                            if i + 1 < len(shortest_p):
                                if path_tuple[1][0] == shortest_p[i + 1]:
                                    output.append((shortest_p[i], path_tuple[0][1]))

                print("shortest path from: ", start, " to: ", target, "is:", output)
                return output

        # falls nach dem Erstellen des Baumes aller kürzesten Pfade im Planet kein Weg vom Start zum Ziel gefunden wurde:
        print("shortest path from: ", start, " to: ", target, "doesn't exist!")
        return None

    def select_direction(self, start: Tuple[int, int], target: Union[None, Tuple[int, int]]):
        # zur Sicherheit wird nochmal abgefragt, ob wir nicht bereits auf dem Ziel sitzen:
        if self.shortest_path(start, target) == []:
            return None

        #falls wir auf einem Knoten sitzen, der noch nicht komplett explored wurde
        # (also noch unbekannte Pfade von ihm abgehen)

        elif start in self.explore_dict:
            # dann wählen wir das erste Element aus der Menge aller nicht erkundeten Pfade (konkreter: Directions)
            return int(self.explore_dict[start][0])

        else:
            return int(self.shortest_path(start, target)[0][1])


if __name__ == "__main__":
    p = Planet()
    p.add_path(((0, 0), Direction.NORTH), ((0, 2), Direction.SOUTH), 2)
    p.add_path(((0, 2), Direction.EAST), ((1, 2), Direction.WEST), 1)
    p.add_path(((1, 2), Direction.EAST), ((1, 4), Direction.EAST), 3)
    p.add_path(((1, 4), Direction.NORTH), ((3, 4), Direction.WEST), 3)
    p.add_path(((2, 2), Direction.EAST), ((3, 4), Direction.SOUTH), 3)
    p.add_path(((2, 2), Direction.SOUTH), ((2, 1), Direction.NORTH), 1)
    p.add_path(((2, 1), Direction.EAST), ((3, 1), Direction.WEST), 1)
    p.add_path(((1, 2), Direction.SOUTH), ((2, 1), Direction.WEST), 3)
    p.add_path(((0, 0), Direction.EAST), ((4, 0), Direction.WEST), 4)
    p.add_path(((4, 0), Direction.NORTH), ((3, 4), Direction.EAST), 4)
    import pprint

    pprint.pprint(p.get_paths())
    p.shortest_path((0, 0), (10, 10))

    print()
