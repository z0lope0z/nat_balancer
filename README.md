# Overview

Given a list of nat instances, and subnets, the NatBalancer will allocate a subnet to a NAT instance in the same availability zone. If no NAT instance in the same availability zone exists, then it randomly selects from existing NAT instances.

For now, this is more of a helper object

# Usage

```python
nat_instances = [
    {"id": "1", "zone": "ap-southeast-1a"},
    {"id": "2", "zone": "ap-southeast-1b"},
    {"id": "3", "zone": "ap-southeast-1c"}
]
        
subnets = [
    {"id": "1", "zone": "ap-southeast-1a"},
    {"id": "2", "zone": "ap-southeast-1b"},
    {"id": "3", "zone": "ap-southeast-1c"}
]

balancer = NatBalancer(nat_instances, subnets)
allocations = balancer.allocate()
balancer.print_allocations(allocations)
```

## Sample output
```
Instance (1 - ap-southeast-1a)
  subnet (1 - ap-southeast-1a)
Instance (2 - ap-southeast-1b)
  subnet (2 - ap-southeast-1b)
Instance (3 - ap-southeast-1c)
  subnet (3 - ap-southeast-1c)
```

# Running the tests

Simply run the command to execute the test

```
python test_nat_balancer.py
```
