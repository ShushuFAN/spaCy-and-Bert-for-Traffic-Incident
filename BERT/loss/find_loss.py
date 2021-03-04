import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def find_loss(file_path,legent_name):
    match="INFO:tensorflow:loss = ([0-9]*.[0-9]*)"
    results=[]
    with open(file_path,"r") as f:
        lines=f.readlines()
        for line in lines:
            result=re.search(match, line)
            if result:
                results.append(float(result.group(1)))
    df=pd.DataFrame(results,columns=[legent_name])
    df.index=df.index+1
    return df
if __name__ == '__main__':
    fig, axes = plt.subplots(2, 1)
    plt.xlabel("Steps")
    plt.ylabel("Losses")
    file_path1 = "record1.txt"
    legent_name = "Classification Task"
    df1 = find_loss(file_path1, legent_name)
    df1.plot(ax=axes[0])
    plt.xlim((1, 145))
    plt.ylim((0, 7))
    my_x_ticks = np.append([1],np.arange(20, 145, 20))
    my_y_ticks = np.arange(0, 7, 1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    file_path2="record2.txt"
    legent_name="Tagging Task"
    df2=find_loss(file_path2,legent_name)
    df2.plot(ax=axes[1])
    # plt.xlabel("Steps")
    # plt.ylabel("Losses")
    plt.xlim((1, 1000))
    plt.ylim((-500, 10800))
    my_x_ticks = np.append([1],np.arange(200, 1100, 200))
    my_y_ticks = np.arange(0, 10800, 2000)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.show()