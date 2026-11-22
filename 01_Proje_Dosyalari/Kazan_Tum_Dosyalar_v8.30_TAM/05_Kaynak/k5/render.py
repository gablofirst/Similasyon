import sys,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
src,out=sys.argv[1],sys.argv[2]; x0,x1,y0,y1=map(float,sys.argv[3:7]); W=int(sys.argv[7])
d,_=recover.readfile(src); m=d.modelspace()
X=lambda x:8706+(x-48.1)*100; Y=lambda y:11530-(y-6.48)*100
H=W*(y1-y0)/(x1-x0)
fig=plt.figure(figsize=(W/100,H/100)); ax=fig.add_axes([0,0,1,1])
Frontend(RenderContext(d),MatplotlibBackend(ax),config=Configuration(background_policy=BackgroundPolicy.WHITE,min_lineweight=0.3)).draw_layout(m,finalize=False)
ax.set_aspect('equal'); ax.set_xlim(X(x0),X(x1)); ax.set_ylim(Y(y1),Y(y0)); ax.axis('off')
fig.set_size_inches(W/100,H/100); fig.savefig(out,dpi=100,facecolor='white')
