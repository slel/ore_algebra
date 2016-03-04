# -*- coding: utf-8 - vim: tw=80
"""
Utilities

(some of which could perhaps be upstreamed at some point)
"""

from sage.misc.cachefunc import cached_function
from sage.misc.misc import cputime
from sage.rings.all import QQ, QQbar, CIF
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing

######################################################################
# Timing
######################################################################

class Clock(object):
    def __init__(self, name="time"):
        self.name = name
        self._sum = 0.
        self._tic = None
    def __repr__(self):
        return "{} = {}".format(self.name, self.total())
    def since_tic(self):
        return 0. if self._tic is None else cputime(self._tic)
    def total(self):
        return self._sum + self.since_tic()
    def tic(self, t=None):
        assert self._tic is None
        self._tic = cputime() if t is None else t
    def toc(self):
        self._sum += cputime(self._tic)
        self._tic = None

class Stats(object):
    def __init__(self):
        self.time_total = Clock("total")
        self.time_total.tic()
    def __repr__(self):
        return ", ".join(str(clock) for clock in self.__dict__.values()
                                    if isinstance(clock, Clock))

######################################################################
# Differential operators
######################################################################

# These functions should probably become methods of suitable subclasses of
# OreOperator, or of a custom wrapper.

@cached_function
def dop_singularities(dop, dom=QQbar):
    return [descr[0] for descr in dop.leading_coefficient().roots(dom)]

def sing_as_alg(dop, iv):
    pol = dop.leading_coefficient().radical()
    return QQbar.polynomial_root(pol, CIF(iv))

######################################################################
# Miscellaneous stuff
######################################################################

def prec_from_eps(eps):
    return -eps.lower().log2().floor()

def jets(base, var_name, order):
    # Polynomial quotient ring elements are faster than power series
    Pols = PolynomialRing(base, var_name)
    return Pols.quo(Pols.one() << order)

def split(cond, objs):
    matching, not_matching = [], []
    for x in objs:
        (matching if cond(x) else not_matching).append(x)
    return matching, not_matching

def as_embedded_number_field_element(alg):
    from sage.rings.number_field.number_field import NumberField
    nf, elt, emb = alg.as_number_field_element()
    if nf is QQ:
        res = elt
    else:
        embnf = NumberField(nf.polynomial(), nf.variable_name(),
                    embedding=emb(nf.gen()))
        res = elt.polynomial()(embnf.gen())
    assert QQbar.coerce(res) == alg
    return res
