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


# Divides a set on a specific column. Can handle numeric or nominal values
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


# Create counts of possible results (the last column of each row is the result)
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

# Entropy is the sum of p(x)log(p(x)) across all
# the different possible results


def entropy(rows):
        log2 = lambda x: log(x) / log(2)
        results = uniquecounts(rows)
        # Now calculate the entropy
        ent = 0.0
        for r in results.keys():
                p = float(results[r])/len(rows)
                ent = ent - p * log2(p)
        return ent


class DecisionNode:
        '''
                @param col: column index of the criteria to be tested
                @param value: value that the column must match to get a true result
                @param result: store a dictionary of results fot this branch
        '''
        def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
            self.col = col
            self.value = value
            self.results = results
            self.tb = tb
            self.fb = fb


def buildtree(rows, scoref=entropy):  # rows is the set, either whole dataset or part of it in the recursive call,
    if len(rows) == 0:
            return DecisionNode()
    current_score = scoref(rows)

    # Set up some variables to track the best criteria
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1

    for col in range(0, column_count):
        #  Generate the list of all possible different values in the considered column
        global column_values
        column_values = {}
    for row in rows:
        column_values[row[col]] = 1
    for value in column_values.keys():
        (set1, set2) = divideset(rows, col, value)

    #  Information gain
    p = float(len(set1)) / len(rows)  # p is the size of a child set relative to its parent
    gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)  # cf. formula information gain
    if gain > best_gain and len(set1) > 0 and len(set2) > 0:  # set must not be empty
        best_gain = gain
        best_criteria = (col, value)
        best_sets = (set1, set2)

    # Create the sub branches
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return DecisionNode(col=best_criteria[0], value=best_criteria[1], tb=trueBranch, fb=falseBranch)
    else:
        return DecisionNode(results=uniquecounts(rows))

tree = buildtree(my_data)

# print(tree.col)
# print(tree.value)
# print(tree.results)
# print("")
# print(tree.tb.col)
# print(tree.tb.value)
# print(tree.tb.results)
# print("")
# print(tree.tb.tb.col)
# print(tree.tb.tb.value)
# print(tree.tb.tb.results)
# print("")
# print(tree.tb.fb.col)
# print(tree.tb.fb.value)
# print(tree.tb.fb.results)


def printtree(tree, indent= ' '):
    # is this leaf node?
    if tree.results is not None:
        print (str(tree.results))
    else:
        print (str(tree.col) + ' : ' + str(tree.value) + '? ')
        # print the branches
        print (indent + 'T ->',)
        printtree(tree.tb, indent + '   ')
        print (indent + 'F ->',)
        printtree(tree.fb, indent + '   ')

printtree(tree)
