SUCCESS = 1
CONFLICT = 2
AMBIGUOUS = 3
UNKNOWN = 4


class Result(object):
    def __init__(self, status, solution=None, msg=None):
        self.status = status
        self.solution = solution
        self.msg = msg


class JointResult(object):
    def __init__(self, results):
        self.results = results

        joint = self.solve()
        self.status = joint.status
        self.solution = joint.solution
        self.msg = joint.msg

    def solve(self):
        statuses = {}
        for alg_name, r in self.results.items():
            status = r.status
            if status not in statuses:
                statuses[status] = {}
            statuses[status][alg_name] = r

        if SUCCESS in statuses: 
            if len(statuses[SUCCESS]) == 1:
                # Only 1 success, we're good. Just use the only one there
                result = statuses[SUCCESS].values()[0]
            else:
                # See if they are the same result, if not, call it a conflict
                items = statuses[SUCCESS].items()
                names, values = zip(*items)
                msg = "Multiple results from {}.".format(' and '.join(names))
                result = Result(CONFLICT, msg=msg)
        elif AMBIGUOUS in statuses:
            # Definitely ambiguous. If more than one, combine them into a big
            # ambiguous result
            items = statuses[AMBIGUOUS].items()
            names, values = zip(*items)
            msg1 = "Ambiguous result from {}.".format(' and '.join(names))
            msg2 = ' '.join(['"{}": {}.'.format(n, r.msg) for n, r in items])
            result = Result(AMBIGUOUS, msg=(msg1+msg2))
        elif UNKNOWN in statuses:
            # Definitely unknown. If more than one, combine them into one big
            # unknown result
            items = statuses[UNKNOWN].items()
            names, values = zip(*items)
            msg1 = "Unknown result from {}.".format(' and '.join(names))
            msg2 = ' '.join(['"{}": {}.'.format(n, r.msg) for n, r in items])
            result = Result(UNKNOWN, msg=(msg1+msg2))
        else:
            raise ValueError('Unknown status')

        return result
