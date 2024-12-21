"""
Statlib by upio
very simple library for generating graphs
"""

#import numpy as np
from tinynumpy import tinynumpy as np
import matplotlib.pyplot as plt
import PIL as pil
import enum
#import pandas as pd
import lightpandas as pd

class StatVisualEnum(enum.Enum):
    line_chart = "line"
    pie_chart = "pie"

class Layout(enum.Enum):
    grid = "grid"
    default = "default"

class StatLib:
    def __init__(self, themename="rose-pine", layout:Layout=Layout.default,compact=True) -> None:
        self.themename = themename
        self.compact = compact
        self.layout = layout
        #plt.style.use(self.themename) this thing broke idk

    def generate(self, data: list, savedirectory: str, size:int) -> None:
        right_charts = sum(1 for d in data if isinstance(d, StatVisualType) and d.right == True)
        left_charts = sum(1 for d in data if isinstance(d, StatVisualType) and d.right == False)

        fig = plt.figure(figsize=(size or 5, size or 5))
        spec = fig.add_gridspec(ncols=(right_charts >= 1 and 2 or 1), nrows=max(right_charts, left_charts))

        right_index = 0
        left_index = 0

        for i in range(len(data)):
            if not isinstance(data[i], StatVisualType):
                continue

            if data[i].type == StatVisualEnum.line_chart:
                if data[i].right:
                    ax = fig.add_subplot(spec[right_index, 1])
                else:
                    ax = fig.add_subplot(spec[left_index, 0])
                ax.set_title(data[i].title)
                ax.set_xlabel(data[i].data["x"]["label"])
                ax.set_ylabel(data[i].data["y"]["label"])

                x = np.array(data[i].data["x"]["data"])
                y = np.array(data[i].data["y"]["data"])
                ax.plot(x, y, color=data[i].color)

                right_index += data[i].right and 1 or 0
                left_index += data[i].right and 0 or 1

            if data[i].type == StatVisualEnum.pie_chart:
                if data[i].right:
                    ax = fig.add_subplot(spec[right_index, 1])
                else:
                    ax = fig.add_subplot(spec[left_index, 0])

                if data[i].explode != None:
                    ax.set_title(data[i].title)
                    ax.pie(data[i].data["data"], labels=data[i].data["labels"],
                        colors=data[i].data["colors"], autopct='%1.1f%%', shadow=True,
                        startangle=90, explode=data[i].explode)
                else:
                    ax.set_title(data[i].title)
                    ax.pie(data[i].data["data"], labels=data[i].data["labels"],
                        colors=data[i].data["colors"], autopct='%1.1f%%', shadow=True,
                        startangle=90)
                if data[i].legend["on"] == True:
                    df = pd.DataFrame(data={"col1": data[i].data["labels"], "col2": data[i].data["data"]})
                    percent = 100.*df.col2/df.col2.sum()
                    labels = ['{0} - {1:1.1f}%'.format(i,j) for i,j in zip(df.col1, percent)]
                    ax.legend(title=data[i].legend["title"], bbox_to_anchor=(0.85, 1), loc='upper left', labels=labels)

                right_index += data[i].right and 1 or 0
                left_index += data[i].right and 0 or 1
        if self.compact:
            fig.tight_layout()

        plt.savefig(savedirectory)
        return True, pil.Image.open(savedirectory)
        
class StatVisualType:
    def __init__(self, type, right: bool, data: dict, title: str, color:str="#ff5555", explode=None, legend:dict={"on":False}) -> None:
        self.type = type
        self.right = right
        self.explode = explode
        self.legend = legend
        self.data = data
        self.title = title
        self.color = color
