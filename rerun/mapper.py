__author__ = 'lane'

class mapper:

    def partializer(self, limit):
        return iter(xrange(0, limit))

    def reducer(self, partial_results):
        pass

