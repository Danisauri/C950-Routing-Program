# Daniela Vidal Canas, Student ID: 001172091
class EmptyBucket:
    pass


# Class to create a hash table of linear probing to avoid collision
class LinearProbingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        self.EMPTY_SINCE_START = EmptyBucket()
        self.EMPTY_AFTER_REMOVAL = EmptyBucket()
        self.table = [self.EMPTY_SINCE_START] * initial_capacity

    # Function to insert element in to the table, avoiding collisions
    def insert(self, item):
        bucket = hash(item) % len(self.table)
        buckets_probed = 0
        while buckets_probed < len(self.table):
            if type(self.table[bucket]) is EmptyBucket:
                self.table[bucket] = item
                return True
            bucket = (bucket + 1) % len(self.table)
            buckets_probed = buckets_probed + 1
        return False

    # Function to search in the hash table, runs until an "Empty since start" bucket is reached or the end of the table
    def search(self, key):
        bucket = hash(key) % len(self.table)
        buckets_probed = 0
        while self.table[bucket] is not self.EMPTY_SINCE_START and buckets_probed < len(self.table):
            if self.table[bucket] == key:
                return self.table[bucket]
            # the bucket was occupied (now or previously), so continue probing.
            bucket = (bucket + 1) % len(self.table)
            buckets_probed = buckets_probed + 1
        # the entire table was probed or an empty cell was found.
        return None

    # Function to remove an element from the Hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        buckets_probed = 0
        while self.table[bucket] is not self.EMPTY_SINCE_START and buckets_probed < len(self.table):
            if self.table[bucket] == key:
                self.table[bucket] = self.EMPTY_AFTER_REMOVAL
            bucket = (bucket + 1) % len(self.table)
            buckets_probed = buckets_probed + 1
