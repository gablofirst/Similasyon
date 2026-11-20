import sys,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
d,_=recover.readfile(sys.argv[1]);m=d.modelspace()
x0,x1,y0,y1=[float(a) for a in sys.argv[3:7]]
fig=plt.figure(figsize=(float(sys.argv[7]) if len(sys.argv)>7 else 30,(float(sys.argv[7]) if len(sys.argv)>7 else 30)*(y1-y0)/(x1-x0)))
ax=fig.add_axes([0,0,1,1])
cfg=Configuration(background_policy=BackgroundPolicy.WHITE)
Frontend(RenderContext(d),MatplotlibBackend(ax),config=cfg).draw_layout(m,finalize=True)
X=lambda x:8706+(x-48.1)*100;Y=lambda y:11530-(y-6.48)*100
ax.set_xlim(X(x0),X(x1));ax.set_ylim(Y(y1),Y(y0))
fig.savefig(sys.argv[2],dpi=100)
