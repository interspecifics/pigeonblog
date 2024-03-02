from math import log10

# https://ai.thestempedia.com/docs/evive-iot-kit/interfacing-mq-3-gas-sensor-with-evive/
# https://www.jaycon.com/understanding-a-gas-sensor/

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

GAS_DATA = {
  "h2": [Point(1, 1.66), Point(3.1, 3), Point(31, 10), Point(100, 18.5)],
  "co": [Point(1, 1.2), Point(10, 2), Point(60, 3), Point(600, 5), Point(2000, 6.55)],
  "methane": [Point(90, 1), Point(700, 2), Point(2000, 2.85)],
}

class Gas:
  def __init__(self, points, R0=None):
    self.R0 = R0
    self.min = points[0].x
    self.max = points[0].x
    ms = []
    bs = []

    for p0 in points:
      self.min = min(self.min, p0.x)
      self.max = max(self.max, p0.x)
      for p1 in points:
        if p0 != p1:
          m = log10(p1.y / p0.y) / log10(p1.x / p0.x)
          ms.append(m)
    self.slope = sum(ms) / len(ms)

    for p in points:
      b = log10(p.y) - self.slope * log10(p.x)
      bs.append(b)
    self.intercept = sum(bs) / len(bs)

  def get_ppm(self, Rs, R0=None):
    R0 = self.R0 if R0 is None else R0
    if R0 is None:
      raise Exception("R0 can't be None")
    y = log10(R0 / Rs)
    ppm = 10 ** ((y - self.intercept) / self.slope)
    return min(max(ppm, self.min), self.max)
