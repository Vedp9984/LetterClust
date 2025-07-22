import numpy as np

def Apriori(input_list, min_support, min_confidence):
    num_transactions = len(input_list)
    rules = []  # Will store rules to return

    # Count individual items
    item_counts = {}
    for transaction in input_list:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1

    # Find frequent 1-itemsets
    frequent_items = {
        frozenset([item]): count
        for item, count in item_counts.items()
        if count / num_transactions >= min_support
    }

    # Dictionary to store all frequent itemsets
    all_frequent_itemsets = {}
    if frequent_items:
        all_frequent_itemsets.update(frequent_items)

    # Current set of frequent itemsets
    L = frequent_items
    k = 2  # Size of current itemsets

    # Iteratively find frequent itemsets of size k
    while L and k <= len(item_counts):
        # Generate candidate itemsets of size k
        Ck = generate_candidates(L, k)

        # Count support for candidates
        itemset_counts = {}
        for transaction in input_list:
            transaction_set = frozenset(transaction)
            for candidate in Ck:
                if candidate.issubset(transaction_set):
                    if candidate in itemset_counts:
                        itemset_counts[candidate] += 1
                    else:
                        itemset_counts[candidate] = 1

        # Filter candidates based on minimum support
        L = {
            itemset: count
            for itemset, count in itemset_counts.items()
            if count / num_transactions >= min_support
        }

        # Add new frequent itemsets to the collection
        if L:
            all_frequent_itemsets.update(L)

        k += 1

    # Generate all possible association rules
    for itemset, count in all_frequent_itemsets.items():
        if len(itemset) > 1:  # Rules can only be generated from itemsets of size > 1
            # Generate all non-empty proper subsets of the itemset
            for i in range(1, len(itemset)):
                for premise in get_subsets(itemset, i):
                    conclusion = itemset - premise
                    if premise and conclusion:  # Ensure neither is empty
                        # Calculate confidence
                        premise_support = all_frequent_itemsets.get(premise, 0)
                        if premise_support > 0:  # Avoid division by zero
                            confidence = count / premise_support
                            if confidence >= min_confidence:
                                # Format and add the rule
                                premise_str = ", ".join(sorted(list(premise)))
                                conclusion_str = ", ".join(sorted(list(conclusion)))
                                rule = f"{premise_str} -> {conclusion_str}"
                                rules.append(rule)
                                print(rule)

    return rules

def generate_candidates(L, k):
    candidates = set()
    frequent_itemsets = list(L.keys())

    for i in range(len(frequent_itemsets)):
        for j in range(i + 1, len(frequent_itemsets)):
            itemset1 = list(frequent_itemsets[i])
            itemset2 = list(frequent_itemsets[j])

            # Sort to ensure consistent ordering
            itemset1.sort()
            itemset2.sort()

            if itemset1[:k - 2] == itemset2[:k - 2]:
                # Create a new candidate
                new_candidate = frozenset(itemset1) | frozenset(itemset2)

                
                if len(new_candidate) == k:
                    
                    all_subsets_frequent = True
                    for item in new_candidate:
                        subset = frozenset(new_candidate - frozenset([item]))
                        if subset not in L:
                            all_subsets_frequent = False
                            break

                    if all_subsets_frequent:
                        candidates.add(new_candidate)

    return candidates

def get_subsets(itemset, length):
    """Generate all subsets of specified length from the given itemset"""
    if length == 0:
        return [frozenset()]

    if length > len(itemset):
        return []

    result = []
    item_list = list(itemset)

    # Helper function to generate combinations
    def backtrack(start, current):
        if len(current) == length:
            result.append(frozenset(current))
            return

        for i in range(start, len(item_list)):
            current.append(item_list[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
