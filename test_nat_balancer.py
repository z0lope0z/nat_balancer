import unittest
from nat_balancer import NatBalancer

class NatBalancerTestCase(unittest.TestCase):
    """Tests for `nat_balancer.py`."""

    def complete_instances(self):
        return [
            {"id": "1", "zone": "ap-southeast-1a"},
            {"id": "2", "zone": "ap-southeast-1b"},
            {"id": "3", "zone": "ap-southeast-1c"}
        ]

    def complete_subnets(self):
        return [
            {"id": "1", "zone": "ap-southeast-1a"},
            {"id": "2", "zone": "ap-southeast-1b"},
            {"id": "3", "zone": "ap-southeast-1c"}
        ]

    def partial_instances(self):
        return [
            {"id": "1", "zone": "ap-southeast-1a"},
        ]

    def partial_subnets(self):
        return [
            {"id": "2", "zone": "ap-southeast-1b"},
        ]

    def duplicate_subnets(self):
        return [
            {"id": "2", "zone": "ap-southeast-1b"},
            {"id": "3", "zone": "ap-southeast-1b"},
        ]

    def random_subnet(self):
        return [
            {"id": "3", "zone": "ap-southeast-1d"},
        ]

    def empty_instances(self):
        return []

    def empty_subnets(self):
        return []

    def test_complete_instances_and_subnets(self):
        """All zones have instances and subnets to be allocated"""
        balancer = NatBalancer(self.complete_instances(), self.complete_subnets())
        allocations = balancer.allocate()
        balancer.print_allocations(allocations)
        self.assertTrue(self.get_subnet_zones(allocations['1']) == set(['ap-southeast-1a']))
        self.assertTrue(self.get_subnet_zones(allocations['2']) == set(['ap-southeast-1b']))
        self.assertTrue(self.get_subnet_zones(allocations['3']) == set(['ap-southeast-1c']))

    def test_partial_instances(self):
        balancer = NatBalancer(self.partial_instances(), self.complete_subnets())
        allocations = balancer.allocate()
        balancer.print_allocations(allocations)
        self.assertTrue(len(allocations['1']) == 3)

    def test_no_instances(self):
        balancer = NatBalancer(self.empty_instances(), self.complete_subnets())
        allocations = balancer.allocate()
        balancer.print_allocations(allocations)
        self.assertTrue(allocations == {})

    def test_no_subnets(self):
        balancer = NatBalancer(self.complete_instances(), self.empty_subnets())
        allocations = balancer.allocate()
        balancer.print_allocations(allocations)
        self.assertTrue(allocations == {})

    def test_partial_subnets(self):
        balancer = NatBalancer(self.complete_instances(), self.partial_subnets())
        allocations = balancer.allocate()
        balancer.print_allocations(allocations)
        self.assertTrue(allocations['2'][0]['zone'] == 'ap-southeast-1b')
        self.assertTrue(len(allocations['2']) == 1)

    def test_duplicate_subnets(self):
        balancer = NatBalancer(self.complete_instances(), self.duplicate_subnets())
        allocations = balancer.allocate()
        balancer.print_allocations(allocations)
        self.assertTrue(allocations['2'][0]['zone'] == 'ap-southeast-1b')
        self.assertTrue(len(allocations['2']) == 2)

    def test_random_subnet(self):
        balancer = NatBalancer(self.complete_instances(), self.random_subnet())
        allocations = balancer.allocate()
        found_subnet = {}
        for key, value in allocations.items():
            if value:
                found_subnet = value
        balancer.print_allocations(allocations)
        self.assertTrue(found_subnet[0]['zone'] == 'ap-southeast-1d')

    def get_subnet_zones(self, allocation):
        return set(map(lambda subnet: subnet['zone'], allocation))

if __name__ == '__main__':
    unittest.main()
