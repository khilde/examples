
from orbit.teapot.teapot import NodeTEAPOT

class Print_Node(NodeTEAPOT):
    """
    Generates the Histograms for distribution in x,y, and x=y directions.
    The z direction from the original WS_Node is repurposed for the diagonal x=y.
    It is not parallel !!!!
    """
    def __init__(self,name = "PrintNode",toFile=False,fileName="output.txt"):
        NodeTEAPOT.__init__(self,name)
        self.toFile=toFile
        self.fileName=fileName

    def track(self, paramsDict):
        """
        The WS_AccNode class implementation of the AccNode class track(probe) method.
        """
        bunch = paramsDict["bunch"]
        path_length = paramsDict["path_length"] 	
        if (self.toFile==False):
            for i in range(bunch.getSize()):        
                print "%d (x,px,y,py,z,pz)= (%f,%f,%f,%f,%f,%f) " %(i,bunch.x(i),bunch.px(i),bunch.y(i),bunch.py(i),bunch.z(i),bunch.pz(i))
        else:
            fileOut=open(self.fileName,'a')
            for i in range(bunch.getSize()):   
                #print self.getName()
                fileOut.write("%d (x,px,y,py,z,pz,s)= (%f,%f,%f,%f,%f,%f,%f)\n" %(i,bunch.x(i),bunch.px(i),bunch.y(i),bunch.py(i),bunch.z(i),bunch.pz(i),path_length))
            fileOut.close()