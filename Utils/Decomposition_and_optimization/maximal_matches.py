
"""
它存储来自模板匹配算法获得的给定匹配的所有最大匹配。
"""


class Match:
    """
    cLass Match是一个对象，用于存储与它的量子比特和clbits配置匹配的列表。
    """

    def __init__(self, match, qubit, clbit):
        """
        Create a Match with necessary arguments.
        Args:
            match (list): list of a match.
            qubit (list): list of qubits configuration.
            clbit (list): list of clbits configuration.
        """

        self.match = match
        self.qubit = qubit
        self.clbit = clbit


class MaximalMatches:
    """
    最大匹配类允许从模板匹配算法得到的匹配列表中排序并存储最大匹配。
    """

    def __init__(self, template_matches):
        """
        Initialize MaximalMatches with the necessary arguments.
        Args:
            template_matches (list): list of matches obtained from running the algorithm.
        """
        self.template_matches = template_matches

        self.max_match_list = []

    def run_maximal_matches(self):
        """
        方法，该方法按递减的长度顺序提取和存储最大匹配。
        """

        self.max_match_list = [
            Match(
                sorted(self.template_matches[0].match),
                self.template_matches[0].qubit,
                self.template_matches[0].clbit,
            )
        ]

        for matches in self.template_matches[1::]:
            present = False
            for max_match in self.max_match_list:
                for elem in matches.match:
                    if elem in max_match.match and len(matches.match) <= len(max_match.match):
                        present = True
            if not present:
                self.max_match_list.append(
                    Match(sorted(matches.match), matches.qubit, matches.clbit)
                )