import io

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as mpatches

from category import *

# TODO figure out how to draw *directed* multigraph
def draw_cat(C: Category):
    G = nx.MultiGraph()
    for f in C.mors:
        G.add_edge(str(f.src.sym), str(f.tgt.sym), label=str(f.sym))
    pydot_graph = nx.drawing.nx_pydot.to_pydot(G)
    pydot_graph.set_dpi(300)
    # render the `pydot` by calling `dot`, no file saved to disk
    png_str = pydot_graph.create_png(prog='dot')
    # treat the DOT output as an image file
    sio = io.BytesIO()
    sio.write(png_str)
    sio.seek(0)
    img = mpimg.imread(sio)
    # plot the image
    imgplot = plt.imshow(img, aspect='equal')
    plt.legend(['Ayy', 'Lmao'])
    red_patch = mpatches.Patch(color=None, label='1 : X -> X')
    plt.legend(handles=[red_patch])
    plt.show()


