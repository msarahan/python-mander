from os import path, getcwd
import json
import copy

from unittest import TestCase

#import geopandas
from mander.districts import District
from mander.metrics import calculatePolsby, calculateConvexHull, calculateReock, calculateSchwartzberg

base_dir = path.dirname(path.realpath(__file__))

metricFunctions = {
  'polsbypopper': calculatePolsby,
  'convexhull': calculateConvexHull,
  'reock': calculateReock,
  'schwartzberg': calculateSchwartzberg
}

test_districts = ['CD_CA_9', 'CD_IL_4', 'CD_PA_7', 'CD_CA_24', 'CD_MA_9']

metrics = {}
for m in metricFunctions:
    metrics[m] = []

test_expected = copy.deepcopy(metrics)
test_returned = copy.deepcopy(metrics)

def collectTestValues(method, district):
  test_expected[method].append('%.4f' % district_scores[method])
  test_returned[method].append('%.4f' % metricFunctions[method](district))

for d in test_districts:

  district_boundaries_file = path.join(base_dir, 'data', d + '.geojson')
  district_scores_file = path.join(base_dir, 'data', d + '_scores.json')

  with open(district_boundaries_file) as district_boundary_data:
    with open(district_scores_file) as district_scores_data:

      district_boundary = json.load(district_boundary_data)
      district_scores = json.load(district_scores_data)

      test_district = District(district_boundaries_file) # TODO use python object instead of file path parameter

      # Collect expected and returned values
      for m in metricFunctions:
          collectTestValues(m, test_district)


class TestMetrics(TestCase):

    def test_polsbypopper(self):
      self.assertEqual(test_expected['polsbypopper'], test_returned['polsbypopper'])

    def test_convexhull(self):
      self.assertEqual(test_expected['convexhull'], test_returned['convexhull'])

    def test_reock(self):
      self.assertEqual(test_expected['reock'], test_returned['reock'])

    def test_schwartzberg(self):
      self.assertEqual(test_expected['schwartzberg'], test_returned['schwartzberg'])
