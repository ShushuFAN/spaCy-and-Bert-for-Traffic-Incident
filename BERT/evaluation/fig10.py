import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.DataFrame([[0.9323,0.7792],[0.9932,0.7970],[0.9618,0.7880]],
                  index=['R', 'P', 'F1'],
                  columns=['Classification Task', 'Tagging Task'])
print(df)
df.plot(kind='bar',figsize=(6,4))
x=np.arange(len(df.index))
y1=np.array(list(df['Classification Task']))
y2=np.array(list(df['Tagging Task']))
for a,b in zip(x,y1): ##控制标签位置
    plt.text(a-0.12,b,'%.2f'%b,ha = 'center',va = 'bottom',fontsize=12)
for a,b in zip(x,y2):
    plt.text(a+0.12,b,'%.2f'%b,ha = 'center',va = 'bottom',fontsize=12)
plt.ylim((0, 1.2))
plt.legend(loc="upper center",mode="expand",ncol=5)
plt.show()
