import matplotlib.pyplot as plt
from collections import Counter

num_friends = [100, 49, 41, 40, 25]

friend_counts = Counter(num_friends)
xs = range(101)  # largest value is 100
ys = [friend_counts[x] for x in xs]  # height is just # of friends
plt.bar(xs, ys)
plt.axis([0, 101, 0, 25])
plt.title("Histogram of Friend Counts")
plt.xlabel("# of friends")
plt.ylabel("# of people")
plt.show()
