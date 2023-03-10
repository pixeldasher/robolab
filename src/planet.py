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
        self.planet_dict: Dict[Tuple[int, int], Dict[Direction,
                                                     Tuple[Tuple[int, int], Direction, Weight]]] = {}
        self.explore_dict: Dict[Tuple[int, int], Set[Direction]] = {}

    # alle neuen Directions bei Ankunft an einem (neuen) Knoten in explore_dict aufnehmen
    def add_vertex(self, vert: Tuple[int, int], directions: Set[Direction]):
        # directions ist ein Set (Menge) aller möglichen neuen(!) directions am neuen Knoten
        directions = {Direction(d) for d in directions}
        print("add_vertex(", vert,",", directions, ")")

        if vert not in self.explore_dict:
            self.explore_dict[vert] = directions
            print("added:", self.explore_dict)

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

        target = (target[0],Direction(target[1]))
        start = (start[0],Direction(start[1]))
        print("add_path(", start,",", target,",", weight, ")")

        self.paths.add((start, target, weight))
        self.paths.add((target, start, weight))

    def vertex_explored(self, start: Union[None, Tuple[Tuple[int, int], Direction]], target: Tuple[Tuple[int, int], Direction]):
        # Entfernen der Directions, die durchs Abfahren dieses Pfades "erkundet" wurden
        target = target and (target[0],Direction(target[1]))
        start = start and (start[0],Direction(start[1]))
        print("vertex_explored(", start,",", target, ")")
        # für den ersten Knoten des Planeten ist der Startknoten des "Herkunftspfads" nicht vorhanden, also Start=None
        if start == None:
            self.explore_dict[target[0]].remove(target[1])
            #print("hallo", self.explore_dict)

        # Normalfall: Start- und Zielknoten des "Herkunftspfads" sind vorhanden:
        else:
            if start[0] in self.explore_dict:
                self.explore_dict[start[0]
                                  ] = self.explore_dict[start[0]] - {start[1]}
            if target[0] in self.explore_dict:
                self.explore_dict[target[0]
                                  ] = self.explore_dict[target[0]] - {target[1]}

    # Directions der durch Mutterschiff hinzugefügten Pfade werden aus explore_dict herausgelöscht: 
    def set_added_paths_expl(self):
        #print("set1")
        #print("expl_dict:", self.explore_dict)
        for path_tuple in self.paths:
            #print("set2, path_tuple[0][1]:", path_tuple[0][0])
            if path_tuple[0][0] in self.explore_dict:
                #print("set3:", path_tuple[0][0])
                if self.explore_dict[path_tuple[0][0]]:
                    #print("remove:", path_tuple[0][1])
                    self.explore_dict[path_tuple[0][0]] = self.explore_dict[path_tuple[0][0]] - {path_tuple[0][1]}
                    #print("explore_dict geändert", self.explore_dict)

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
            self.planet_dict[path_tuple[0][0]][path_tuple[0][1]] = (
                path_tuple[1][0], path_tuple[1][1], path_tuple[2])

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
        
        print("shortest_path(", start, ",", target, ")")

        # wenn Ziel- und Startknoten derselbe sind, wird ein "leerer Weg" zurückgegeben
        if target == start:
            # print("shortest path from: ", start, " to: ", target, "? ... well... just stay right here.")
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
            # alle Pfade (alle path_tuples, die im paths-set enthalten sind)
            for path_tuple in self.paths:
                if path_tuple[0][0] == u:  # nur die Pfade, dessen Startknoten u entspricht

                    # Pfade mit weight -1 sind irrelevant, da diese Sackgassen sind
                    if not path_tuple[2] == -1:

                        v = path_tuple[1][0]
                        # falls diese Nachbarn noch zu scannen sind (also noch Element der Liste to_do sind)
                        if v in to_do:

                            # Berechnung und Vergleich des Alternativwegs: neuer Distanzwert durch Berücksichtigung der jeweiligen Kante zwischen u und v (path_tuple[2])
                            altern = dist[u] + path_tuple[2]

                            # falls Alterativweg kürzer ist, als bisheriger, wird Vorgänger von v auf u gesetzt und die Distanz zu v auf altern gesetzt
                            if altern < dist[v]:
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
                                    output.append(
                                        (shortest_p[i], path_tuple[0][1]))

                # print("shortest path from: ", start, " to: ", target, "is:", output)
                return output

        # falls nach dem Erstellen des Baumes aller kürzesten Pfade im Planet kein Weg vom Start zum Ziel gefunden wurde:
        # print("shortest path from: ", start, " to: ", target, "doesn't exist!")
        return None

    def select_direction(self, start: Tuple[int, int], target: Union[None, Tuple[int, int]]):
        # zur Sicherheit wird nochmal abgefragt, ob wir nicht bereits auf dem Ziel sitzen:
        # if target is not None:
        #    if start[0] == target[0]:
        #        return None

        # falls wir auf einem Knoten sitzen, der noch nicht komplett explored wurde
        # (also noch unbekannte Pfade von ihm abgehen)

        print("select_direction(", start, ",", target, ")")
        print("Explored Dict:", self.explore_dict)

        if start in self.explore_dict:
            if self.explore_dict[start]:
                print("if value an stelle start existiert:", self.explore_dict[start])
                # dann wählen wir das erste Element aus der Menge aller nicht erkundeten Pfade (konkreter: Directions)
                temp: Direction
                for d in self.explore_dict[start]:
                    temp = d
                print(temp)
                return temp

        return int(self.shortest_path(start, target)[0][1])


"""
if __name__ == "__main__":
    intelligent_planet = Planet()

    intelligent_planet.add_vertex((1, 1), {Direction.SOUTH, Direction.EAST, Direction.NORTH})
    intelligent_planet.vertex_explored(None, ((1, 1), Direction.SOUTH))

    intelligent_planet.add_vertex((1, 2), {Direction.SOUTH, Direction.EAST})
    intelligent_planet.add_path(((1, 1), Direction.NORTH), ((1, 2), Direction.SOUTH), 1)
    intelligent_planet.vertex_explored(((1, 1), Direction.NORTH), ((1, 2), Direction.SOUTH))

    intelligent_planet.add_vertex((2, 1), {Direction.EAST, Direction.WEST})
    intelligent_planet.add_path(((1, 1), Direction.EAST), ((2, 1), Direction.WEST), 1)
    intelligent_planet.vertex_explored(((1, 1), Direction.EAST), ((2, 1), Direction.WEST))

    intelligent_planet.add_vertex((2, 3), {Direction.SOUTH, Direction.WEST})
    intelligent_planet.add_path(((1, 2), Direction.EAST), ((2, 3), Direction.SOUTH), 2)
    intelligent_planet.vertex_explored(((1, 2), Direction.EAST), ((2, 3), Direction.SOUTH))

    #import pprint

    #pprint.pprint(p.get_paths())
    #p.shortest_path((0, 0), (10, 10))
"""
