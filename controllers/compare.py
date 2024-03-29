class CompareController:

    THRESHOLD = 10

    EXCELLENT_THRESHOLD = THRESHOLD * 2
    GREAT_THRESHOLD = THRESHOLD * 3
    GOOD_THRESHOLD = THRESHOLD * 4
    BAD_THRESHOLD = THRESHOLD * 5

    # enum
    PERFECT = 0
    EXCELLENT = 1
    GREAT = 2
    GOOD = 3
    BAD = 4
    MISS = 5

    def __init__(self, threshold=10):
        self.THRESHOLD = threshold

    def score(self, source_pitch, compare_pitch):
        if abs(source_pitch - compare_pitch) < self.THRESHOLD:
            return self.PERFECT
        elif abs(source_pitch - compare_pitch) < self.EXCELLENT_THRESHOLD:
            return self.EXCELLENT
        elif abs(source_pitch - compare_pitch) < self.GREAT_THRESHOLD:
            return self.GREAT
        elif abs(source_pitch - compare_pitch) < self.GOOD_THRESHOLD:
            return self.GOOD
        elif abs(source_pitch - compare_pitch) < self.BAD_THRESHOLD:
            return self.BAD
        else:
            return self.MISS

    def calculate_ratio_score(self, score_array):
        # percentage based, perfect is a 1 to 1
        total = 0
        for i in range(len(score_array)):
            total += score_array[i]
        score = (score_array[self.PERFECT] +
                 round(score_array[self.EXCELLENT] / 2) +
                 round(score_array[self.GREAT] / 3) +
                 round(score_array[self.GOOD] / 4) +
                 round(score_array[self.BAD] / 5)) / total
        return round(score * 100)

    def compare_pitches_direct(self, source, compare):
        # direct comparison between pitch timings
        score_array = [0,0,0,0,0,0]
        # shitty comparison for now dw about it
        source_length = len(source)
        compare_length = len(compare)
        length = source_length if source_length < compare_length else compare_length
        for i in range(length):
            score_array[self.score(source[i], compare[i])] += 1
        score = self.calculate_ratio_score(score_array)
        return (score_array, score)
