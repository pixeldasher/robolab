#!/usr/bin/env python3

import unittest
from planet import Direction, Planet


'''class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        +--+
        |  |
        +-0,3------+
           |       |
          0,2-----2,2 (target)
           |      /
        +-0,1    /
        |  |    /
        +-0,0-1,0
           |
        (start)

        """
        # Initialize your data structure here
        self.planet = Planet()
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)

    @unittest.skip('Example test, should not count in final test results')
    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """
        self.assertIsNone(self.planet.shortest_path((0, 0), (1, 2)))'''


class RoboLabPlanetTests(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """

        # empty planet:
        self.planet_empty = Planet()


        # standard planet:
        self.planet = Planet()

        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 2), Direction.SOUTH), 2)
        self.planet.add_path(((0, 2), Direction.EAST), ((1, 2), Direction.WEST), 1)
        self.planet.add_path(((1, 2), Direction.EAST), ((1, 4), Direction.EAST), 3)
        self.planet.add_path(((1, 4), Direction.NORTH), ((3, 4), Direction.WEST), 3)
        self.planet.add_path(((2, 2), Direction.EAST), ((3, 4), Direction.SOUTH), 3)
        self.planet.add_path(((2, 2), Direction.SOUTH), ((2, 1), Direction.NORTH), 1)
        self.planet.add_path(((2, 1), Direction.EAST), ((3, 1), Direction.WEST), 1)
        self.planet.add_path(((1, 2), Direction.SOUTH), ((2, 1), Direction.WEST), 3)
        self.planet.add_path(((0, 0), Direction.EAST), ((4, 0), Direction.WEST), 4)
        self.planet.add_path(((4, 0), Direction.NORTH), ((3, 4), Direction.EAST), 4)

        # same lenght planet:
        self.planet_same_same = Planet()

        self.planet_same_same.add_path(((0, 0), Direction.NORTH), ((0, 2), Direction.SOUTH), 2)
        self.planet_same_same.add_path(((0, 2), Direction.EAST), ((1, 2), Direction.WEST), 1)
        self.planet_same_same.add_path(((1, 2), Direction.EAST), ((1, 4), Direction.EAST), 3)
        self.planet_same_same.add_path(((1, 4), Direction.NORTH), ((3, 4), Direction.WEST), 2) # weight changed
        self.planet_same_same.add_path(((2, 2), Direction.EAST), ((3, 4), Direction.SOUTH), 3)
        self.planet_same_same.add_path(((2, 2), Direction.SOUTH), ((2, 1), Direction.NORTH), 1)
        self.planet_same_same.add_path(((2, 1), Direction.EAST), ((3, 1), Direction.WEST), 1)
        self.planet_same_same.add_path(((1, 2), Direction.SOUTH), ((2, 1), Direction.WEST), 3)
        self.planet_same_same.add_path(((0, 0), Direction.EAST), ((4, 0), Direction.WEST), 4)
        self.planet_same_same.add_path(((4, 0), Direction.NORTH), ((3, 4), Direction.EAST), 4)

        # same length and loop planet:
        self.planet_loop = Planet()

        self.planet_same_same.add_path(((4, 0), Direction.SOUTH), ((4, 0), Direction.EAST), 1) # loop 1
        self.planet_same_same.add_path(((1, 4), Direction.SOUTH), ((1, 4), Direction.WEST), 1) # loop 2
        self.planet_loop.add_path(((0, 0), Direction.NORTH), ((0, 2), Direction.SOUTH), 2)
        self.planet_loop.add_path(((0, 2), Direction.EAST), ((1, 2), Direction.WEST), 1)
        self.planet_loop.add_path(((1, 2), Direction.EAST), ((1, 4), Direction.EAST), 3)
        self.planet_loop.add_path(((1, 4), Direction.NORTH), ((3, 4), Direction.WEST), 2) # weigth changed
        self.planet_loop.add_path(((2, 2), Direction.EAST), ((3, 4), Direction.SOUTH), 3)
        self.planet_loop.add_path(((2, 2), Direction.SOUTH), ((2, 1), Direction.NORTH), 1)
        self.planet_loop.add_path(((2, 1), Direction.EAST), ((3, 1), Direction.WEST), 1)
        self.planet_loop.add_path(((1, 2), Direction.SOUTH), ((2, 1), Direction.WEST), 3)
        self.planet_loop.add_path(((0, 0), Direction.EAST), ((4, 0), Direction.WEST), 4)
        self.planet_loop.add_path(((4, 0), Direction.NORTH), ((3, 4), Direction.EAST), 4)


    def test_integrity(self):
        """
        This test should check that the dictionary returned by "planet.get_paths()" matches the expected structure
        """
        expect_dict = {
            (0, 0): {Direction.NORTH: ((0, 2), Direction.SOUTH, 2),
                      Direction.EAST: ((4, 0), Direction.WEST, 4)},

            (0, 2): {Direction.SOUTH: ((0, 0), Direction.NORTH, 2),
                     Direction.EAST: ((1, 2), Direction.WEST, 1)},

            (1, 2): {Direction.SOUTH: ((2, 1), Direction.WEST, 3),
                     Direction.EAST: ((1, 4), Direction.EAST, 3),
                     Direction.WEST: ((0, 2), Direction.EAST, 1)},

            (1, 4): {Direction.NORTH: ((3, 4), Direction.WEST, 3),
                     Direction.EAST: ((1, 2), Direction.EAST, 3)},

            (2, 1): {Direction.WEST: ((1, 2), Direction.SOUTH, 3),
                     Direction.EAST: ((3, 1), Direction.WEST, 1),
                     Direction.NORTH: ((2, 2), Direction.SOUTH, 1)},

            (2, 2): {Direction.SOUTH: ((2, 1), Direction.NORTH, 1),
                     Direction.EAST: ((3, 4), Direction.SOUTH, 3)},

            (3, 1): {Direction.WEST: ((2, 1), Direction.EAST, 1)},

            (3, 4): {Direction.SOUTH: ((2, 2), Direction.EAST, 3),
                     Direction.WEST: ((1, 4), Direction.NORTH, 3),
                     Direction.EAST: ((4, 0), Direction.NORTH, 4)},

            (4, 0): {Direction.WEST: ((0, 0), Direction.EAST, 4),
                     Direction.NORTH: ((3, 4), Direction.EAST, 4)}
        }

        import pprint
        pprint.pprint(self.planet.get_paths())

        self.assertEqual(expect_dict, self.planet.get_paths())


    def test_empty_planet(self):
        """
        This test should check that an empty planet really is empty
        """

        self.assertFalse(self.planet_empty.planet_dict)
        self.assertFalse(self.planet_empty.explore_dict)
        self.assertFalse(self.planet_empty.paths)


    def test_target(self):
        """
        This test should check that the shortest-path algorithm implemented works.

        Requirement: Minimum distance is three nodes (two paths in list returned)
        """

        expect_list = [
            ((0, 0), Direction.EAST), ((4, 0), Direction.NORTH)
        ]

        self.assertEqual(expect_list, self.planet.shortest_path((0, 0), (3, 4)))


    def test_target_not_reachable(self):
        """
        This test should check that a target outside the map or at an unexplored node is not reachable
        """

        expect_list = None

        self.assertEqual(expect_list, self.planet.shortest_path((0, 0), (10, 10)))


    def test_same_length(self):
        """
        This test should check that the shortest-path algorithm implemented also can return alternatives with the
        same cost (weights)

        Requirement: Minimum of two paths with same cost exists, only one is returned by the logic implemented
        """
        expect_list_1 = [
            ((0, 0), Direction.EAST),
            ((4, 0), Direction.NORTH)
        ]
        expect_list_2 = [
            ((0, 0), Direction.NORTH),
            ((0, 2), Direction.EAST),
            ((1, 2), Direction.EAST),
            ((1, 4), Direction.NORTH)
        ]

        self.assertEqual(self.planet_same_same.shortest_path((0, 0), (3, 4)), expect_list_1 or expect_list_2)

    def test_target_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target nearby

        Result: Target is reachable
        """
        expect_list = [
            ((0, 0), Direction.EAST), ((4, 0), Direction.NORTH)
        ]

        self.assertEqual(expect_list, self.planet_loop.shortest_path((0, 0), (3, 4)))

    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """

        expect_list = None

        self.assertEqual(expect_list, self.planet_loop.shortest_path((0, 0), (10, 10)))


if __name__ == "__main__":
    unittest.main()
