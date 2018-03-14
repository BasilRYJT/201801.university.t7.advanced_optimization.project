from amplpy import AMPL

ap = AMPL()

ap.read("models/part1.mod")
ap.readData("output/part1.dat")

ap.solve()

print(ap.getObjective("X"))