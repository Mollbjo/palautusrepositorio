class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False

        return True


class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value

class All:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False
                
        return True
        
class Not:
    def __init__(self, matcher):
        self._matcher = matcher

    def test(self, player):
        return not self._matcher.test(player)
    
class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value < self._value
    
class Or:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if matcher.test(player):
                return True

        return False

class QueryBuilder:
    def __init__(self, matchers=None):
        self._matchers = list(matchers) if matchers is not None else []

    def _with(self, matcher):
        return QueryBuilder(self._matchers + [matcher])

    def plays_in(self, team):
        return self._with(PlaysIn(team))

    def has_at_least(self, value, attr):
        return self._with(HasAtLeast(value, attr))

    def has_fewer_than(self, value, attr):
        return self._with(HasFewerThan(value, attr))

    def one_of(self, *branches):
        built_branches = []
        for branch in branches:
            if isinstance(branch, QueryBuilder):
                built_branches.append(branch.build())
            else:
                built_branches.append(branch)
        return self._with(Or(*built_branches))

    def build(self):
        if not self._matchers:
            return All()
        if len(self._matchers) == 1:
            return self._matchers[0]
        return And(*self._matchers)