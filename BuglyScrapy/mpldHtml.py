# -*- coding: utf-8 -*-
import matplotlib
import datetime
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
# np.random.seed(19680801)


plt.rcdefaults()
fig, ax = plt.subplots()

# Example data
people = ('/friendshop/36/category/catelist.do', '/friendshop/42/promotion/querystardamondgoodslist.do', 'Harry', 'Slim', 'Jim')
print(type(people))
y_pos = np.arange(len(people))
performance = 3 + 10 * np.random.rand(len(people))
error = np.random.rand(len(people))

print(performance)
ax.barh(y_pos, performance, align='center',
        color='green', ecolor='black')
ax.set_yticks(y_pos)
ax.set_yticklabels(['/friendshop/36/category/catelist.do', '/friendshop/42/promotion/querystardamondgoodslist.do', 'Harry', 'Slim', 'Jim'])
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xticklabels(['10', '20', '30', '40', '50', '60', '70'])
# ax.set_xlabel('Performance')
# ax.set_title('How fast do you want to go today?')

plt.show()