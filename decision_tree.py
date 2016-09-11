from math import log

my_data = [
        ['slashdot', 'USA', 'yes', 18, 'None'],
        ['google', 'France', 'yes', 23, 'Premium'],
        ['digg', 'USA', 'yes', 24, 'Basic'],
        ['kiwitobes', 'France', 'yes', 23, 'Basic'],
        ['google', 'UK', 'no', 21, 'Premium'],
        ['(direct)', 'New Zealand', 'no', 12, 'None'],
        ['(direct)', 'UK', 'no', 21, 'Basic'],
        ['google', 'USA', 'no', 24, 'Premium'],
        ['slashdot', 'France', 'yes', 19, 'None'],
        ['digg', 'USA', 'no', 18, 'None'],
        ['google', 'UK', 'no', 18, 'None'],
        ['kiwitobes', 'UK', 'no', 19, 'None'],
        ['digg', 'New Zealand', 'yes', 12, 'Basic'],
        ['slashdot', 'UK', 'no', 21, 'None'],
        ['google', 'UK', 'yes', 18, 'Basic'],
        ['kiwitobes', 'France', 'yes', 19, 'Basic']
]


def divideset(rows, column, value):
        '''
                Divides a set on specific column. Can handle numeric or nominal values
        '''
        split_function = None
        if isinstance(value, int) or isinstance(value, float):  # check if value is a number int or float
                split_function = lambda row: row[column] >= value
        else:
                split_function = lambda row: row[column] == value
        #  Divide the rowsinto two sets and return them
        set1 = [row for row in rows if split_function(row)]
        set2 = [row for row in rows if not split_function(row)]
        return (set1, set2)


def uniquecounts(rows):
        '''
                Create a counts of possible results (the last column of each row is the result)
        '''
        results = {}
        for row in rows:
                # the result is the last column
                r = row[len(row)-1]
                if r not in results:
                        results[r] = 0
                results[r] += 1
        return results


# Entropy is the sum of p(x)log(p(x)) across all the different possible results
def entropy(rows):
        log2 = lambda x: log(x) / log(2)
        results = uniquecounts(rows)
        # Now calculate the entropy
        ent = 0.0
        for r in results.keys():
                p = float(results[r])/len(rows)
                ent = ent - p * log2(p)
        return ent
