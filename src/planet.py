#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import List, Tuple, Dict, Union


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
        self.planet_dict = {}

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


        # vorheriger Programmcode: evtl eher für get_path verwenden? und intern mit anderer Speicherform für Pfade arbeiten?
        # if not start[1] in self.planet_dict:
        #    path_dict = {}
        #    self.planet_dict[start[1]] = path_dict
        #self.planet_dict[start[1]] [start[2]] = (target[1], target[2], weight)


    #def close_path(self, start: Tuple[Tuple[int, int], Direction]):
        # eigenständig hinzugefügt
        # wenn eine Flasche auf dem Pfad erscheint und er deshalb nicht mehr passierbar ist...?
        # unnötig, da dieser Pfad einfach das Gewicht -1 erhält

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
            if not path_tuple[1] [1] in self.planet_dict:
                path_dict = {}
                self.planet_dict[path_tuple[1] [1]] = path_dict
            self.planet_dict[path_tuple[1] [1]] [path_tuple[1] [2]] = (path_tuple[2] [1], path_tuple[2] [2], path_tuple[3])



    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Union[None, List[Tuple[Tuple[int, int], Direction]]]:
        """
        Returns a shortest path between two nodes

        Examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: 2-Tuple[List, Direction]
        """

        # Initialisierung für Djikstra:

        dist = {} # Dictionary für Distanz aller Knoten zu Startknoten
        prev = {} # Dictionary für Vorgängerknoten
        q = []# Liste aller Knoten, für die noch kein kürzester Weg vom Startknoten aus gefunden wurde

        for (x, y) in self.planet_dict:
            dist[(x, y)] = float("inf")
            prev[(x, y)] = None
            q.append(x, y)

        dist[start] = 0

        # Dijkstraalgorithmus:

        if not q==():   # wird nur ausgeführt, wenn es noch Knoten gibt, zu denen kein kürzester Weg berechnet wurde

            # Ermittlung von u (=(xu, yu)) - u ist Knoten mit der kleinsten Distanz zu Startknoten
            temp = float("inf")

            for i in range (len(q)):
                if dist[q(i)] <= temp:
                    u = q(i)
                    temp = dist[q(i)]

            # Entfernen des Knoten u aus Liste q (Liste aller Knoten, für die noch kein kürzester Weg vom Startknoten aus gefunden wurde)
            q.remove(u)

            for (x, y) in self.planet_dict.values [u]:








