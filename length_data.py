BULGE = object()
HAIRPIN = object()
INTERNAL_LOOP = object()
MULTI_LOOP = object()
STEM = object()
LEGAL_ELEMENTS = [BULGE, HAIRPIN, INTERNAL_LOOP, MULTI_LOOP, STEM]

class UnknownStructuralElement(Exception):
  def __init__(self, elt):
    self.elt = elt
  
  def __str__(self):
    return str(self.elt) + ' is an unknown type. Valid elements are' + \
        ' partition.BULGE, partition.HAIRPIN, partition.INTERNAL_LOOP,' + \
        ' partition.MULTI_LOOP, and partition.STEM'

import length_distribution

_BULGE_DATA = ((425, 0.530666666666667),
              (57, 0.592),
              (178, 0.653333333333333),
              (189, 0.714666666666667),
              (755, 0.776),
              (280, 0.837333333333333),
              (161, 0.898666666666667),
              (39, 0.96),
              (359, 1.02133333333333),
              (26, 1.08266666666667),
              (82, 1.144),
              (10, 1.20533333333333),
              (31, 1.26666666666667),
              (20, 1.328),
              (14, 1.38933333333333))
_BULGE_DISTRIBUTION = length_distribution.LengthDistribution()

_HAIRPIN_DATA = ((53, 1.03533333333333),
                (182, 1.766),
                (9, 2.49666666666667),
                (125, 3.22733333333333),
                (463, 3.958),
                (635, 4.68866666666667),
                (774, 5.41933333333333),
                (422, 6.15),
                (353, 6.88066666666667),
                (411, 7.61133333333334),
                (555, 8.342),
                (108, 9.07266666666667),
                (47, 9.80333333333333),
                (16, 10.534),
                (12, 11.2646666666667))
_HAIRPIN_DISTRIBUTION = length_distribution.LengthDistribution()

_INTERNAL_LOOP_DATA = ((131, 1.11666666666667),
                      (33, 1.35),
                      (124, 1.58333333333333),
                      (125, 1.81666666666667),
                      (273, 2.05),
                      (271, 2.28333333333333),
                      (335, 2.51666666666667),
                      (238, 2.75),
                      (621, 2.98333333333333),
                      (229, 3.21666666666667),
                      (89, 3.45),
                      (52, 3.68333333333333),
                      (55, 3.91666666666667),
                      (32, 4.15),
                      (121, 4.38333333333333))
_INTERNAL_LOOP_DISTRIBUTION = length_distribution.LengthDistribution()

_MULTI_LOOP_DATA = ((74, 0.381333333333333),
                   (344, 1.144),
                   (656, 1.90666666666667),
                   (742, 2.66933333333333),
                   (421, 3.432),
                   (202, 4.19466666666667),
                   (184, 4.95733333333333),
                   (320, 5.72),
                   (286, 6.48266666666667),
                   (98, 7.24533333333333),
                   (44, 8.008),
                   (27, 8.77066666666666),
                   (55, 9.53333333333333),
                   (31, 10.296),
                   (14, 11.0586666666667))
_MULTI_LOOP_DISTRIBUTION = length_distribution.LengthDistribution()

_STEM_DATA = ((36, 2.741),
             (110, 3.023),
             (128, 3.305),
             (225, 3.587),
             (415, 3.869),
             (348, 4.151),
             (770, 4.433),
             (521, 4.715),
             (558, 4.997),
             (587, 5.279),
             (222, 5.561),
             (79, 5.843),
             (158, 6.125),
             (36, 6.407),
             (22, 6.689))
_STEM_DISTRIBUTION = length_distribution.LengthDistribution()

_INFO = ((_BULGE_DISTRIBUTION, _BULGE_DATA),
         (_HAIRPIN_DISTRIBUTION, _HAIRPIN_DATA),
         (_INTERNAL_LOOP_DISTRIBUTION, _INTERNAL_LOOP_DATA),
         (_MULTI_LOOP_DISTRIBUTION, _MULTI_LOOP_DATA),
         (_STEM_DISTRIBUTION, _STEM_DATA))

for (distro, data) in _INFO:
  for datapoint in data:
    distro.UpdateProbability(datapoint[1], num_times=datapoint[0])

_DISTROS = {BULGE: _BULGE_DISTRIBUTION,
            HAIRPIN: _HAIRPIN_DISTRIBUTION,
            INTERNAL_LOOP: _INTERNAL_LOOP_DISTRIBUTION,
            MULTI_LOOP: _MULTI_LOOP_DISTRIBUTION,
            STEM: _STEM_DISTRIBUTION}

"""
Given a member of LEGAL_ELEMENTS, samples the corresponding
probability distribution and returns a length for that element.
"""
def Sample(elt):
  if elt not in LEGAL_ELEMENTS:
    raise UnknownStructuralElement(elt)
  return int(round(_DISTROS[elt].Sample()))
