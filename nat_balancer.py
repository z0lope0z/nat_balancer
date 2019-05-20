import random
from collections import defaultdict

class NatBalancer:
    def __init__(self, instances, subnets):
        self.zone_instances = defaultdict(list)
        self.id_instances = defaultdict(str)
        self.id_subnets = defaultdict(str)
        self.instances = instances
        self.subnets = subnets
        self.__build_map()

    def __build_map(self):
        for instance in self.instances:
            self.zone_instances[instance['zone']].append(instance)
            self.id_instances[instance['id']] = instance
        for subnet in self.subnets:
            self.id_subnets[subnet['id']] = subnet

    def __allocate_subnet(self, subnet):
        zone = subnet['zone']
        filtered_instances = self.instances
        if self.zone_instances[zone]:
            filtered_instances = self.zone_instances[zone]
        return random.choice(filtered_instances)

    def __allocate_subnets(self):
        instance_allocations = defaultdict(str)
        for instance in self.instances:
            instance_allocations[instance['id']] = []
        for subnet in self.subnets:
            instance = self.__allocate_subnet(subnet)
            instance_allocations[instance['id']].append(subnet)
        return instance_allocations

    def allocate(self):
        if len(self.instances) == 0 or len(self.subnets) == 0:
            return {}
        return self.__allocate_subnets()

    def print_allocations(self, allocations):
        for instance_id, subnets in allocations.items():
            print("Instance (%s - %s)" % (instance_id, self.id_instances[instance_id]['zone']))
            for subnet in subnets:
                print("  subnet (%s - %s)" % (subnet['id'], self.id_subnets[subnet['id']]['zone']))

