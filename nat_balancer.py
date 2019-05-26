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
        '''
        creates the map structures needed to do fast lookups later on
        precompute the distribution for each instance based on weight
        precompute the distribution for each zone based on weight
        '''
        self.instance_distribution = []
        self.zone_instance_distribution = defaultdict(list)
        for instance in self.instances:
            self.id_instances[instance['id']] = instance
            self.__allocate_distributions(instance)

            # append instance for a given zone
            self.zone_instances[instance['zone']].append(instance)

        # allocate subnets
        for subnet in self.subnets:
            self.id_subnets[subnet['id']] = subnet

    def __allocate_distributions(self, instance):
            # distribution for all instances
            distribution = [instance['id']] * instance.get('weight', 1)
            self.instance_distribution.extend(distribution)

            # distribution for within a zone
            self.zone_instance_distribution[instance['zone']].extend(distribution)

    def __allocate_subnet(self, subnet):
        '''
        Allocates an instance for a given subnet
        Random.choice uses an index lookup O(1) and hash lookups is O(1), therefore subnet allocations take O(1)
        https://stackoverflow.com/questions/40143157/q-what-is-big-o-complexity-of-random-choicelist-in-python3
        '''
        zone = subnet['zone']
        filtered_instances = self.instance_distribution
        if self.zone_instances[zone] and (self.zone_instance_distribution[zone] != []):
            filtered_instances = self.zone_instance_distribution[zone]
        return self.id_instances[random.choice(filtered_instances)]

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

