""" Modularize ScoreList object. """


class ScoreList(object):
    """ Score List object keeps a list of 2-tuples, (str name, int score),
       and print_scores, entry_to_str(index), get_length(), get_min(),
       get_max(), should_add(), add_score(entry), to_file(), clear_file() """

    def __init__(self, filename):
        self.filename = filename
        self.scores = []
        with open(filename) as to_file:
            filelist = list(to_file)
            for index in filelist:
                if (index.rstrip() != ''):
                    index = index.rstrip('\n')
                    space = len(index) - index[::-1].index(' ') - 1
                    name = index[:space]
                    index = (name, int(index[space + 1:]))
                    self.scores.append(index)

    def print_scores(self):
        """ Print (name, score) 2-tuples. """
        for score in self.scores:
            print score

    def entry_to_str(self, index):
        """ Return the string representation of the score at index index. """
        if index > len(self.scores) - 1:
            return None  # Failed to print score entry: invalid index."
        return "%s  %d" % (self.scores[index][0], int(self.scores[index][1]))

    def get_length(self):
        """ Return the number of scores. """
        return len(self.scores)

    def get_min(self):
        """ Get the minimum score, 0 if score list not full.
            Assumed ordering of greatest to least. """
        if (len(self.scores) < 10):
            return 0
        return self.scores[len(self.scores) - 1][1]

    def get_max(self):
        """ Get the minimum score, 0 if score list not full.
            Assumed ordering of greatest to least. """
        if (len(self.scores) == 0):
            return 0
        return self.scores[0][1]

    def should_add(self, score):
        """ Determines whether a score makes it onto the highscore list. """
        if (len(self.scores) < 10 or score > self.get_min()):
            if score != 0:
                return True
        return False

    def add_score(self, entry):
        """ Adds a score to the list.
            @param 2-tuple entry (str name, int score) """

        score = entry[1]
        i = 0

        while (i < len(self.scores) and score <= self.scores[i][1]):
            i += 1
        self.scores.insert(i, entry)
        if (len(self.scores) > 10):
            self.scores = self.scores[:10]

        self.to_file()  # save the change

    def to_file(self, filename=None):
        """ Write the scores to file. """
        if filename is None:
            filename = self.filename
        with open(filename, 'w') as to_file:
            for index in self.scores:
                name, score = index
                to_file.write("%s %d\n" % (name, int(score)))

    def clear_file(self):
        """ Clear the file (reset high score list). """
        self.scores = []
        self.to_file()
