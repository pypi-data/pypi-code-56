import numpy as np
from scipy import interpolate
from skimage import measure

from genepy3d.util import plot as pl

from mpl_toolkits import mplot3d

from pyevtk.hl import unstructuredGridToVTK
from pyevtk.vtk import VtkTriangle
import vtk

class Surface:
    """Surface in 3D.
    
    Attributes:
        vertices (2d numpy array (float)): vertices coordinates.
        simplices (2d numpy array (float)): index of the vertices of each of the simplices.
    
    """
    def __init__(self, _vertices, _simplices):
        self.vertices = _vertices
        self.simplices = _simplices
   
    @classmethod
    def from_points_qhull(cls,points):
        """Create surface object from point cloud via the convex hull algorithms.
      
        Args:
            points (nx3 array of float): coordinates of point cloud
            alpha (float): value of alpha
        
        Returns:
            a Surface object
        """               

        from scipy.spatial import ConvexHull
        hull = ConvexHull(points)
        #becasue hull.simplices are in the context of the full point list, not just Qhull vertexes
        simplices=np.reshape(np.stack([np.where(hull.vertices==i)[0] for i in hull.simplices.flat]),hull.simplices.shape) 
        return cls(hull.points[hull.vertices,:], simplices)
    
    @classmethod
    def from_points_alpha_shape(cls,points,alpha=None):
        """Create surface object from point cloud via CGAL alpha-shape algorithms. if 'alpha is none, it id estimated as the smallest alpha that gives a single connected component. the estimated surface is formes by the triangles of the regularised alpha-complex facing outward.
      
        Args:
            points (nx3 array of float): coordinates of point cloud
            alpha (float): value of alpha
        
        Returns:
            a Surface object
        """
        
        from CGAL import CGAL_genepy3d
        from CGAL.CGAL_Kernel import Point_3
        from CGAL import CGAL_Point_set_processing_3 as psp

               
        pointsCGAL= []
        pointsCGALas= []
        pointsCGALastri= []
        for i in range(points.shape[0]):
            pointsCGAL.append(Point_3(points[i,0],points[i,1],points[i,2]))
        
        psp.jet_smooth_point_set(pointsCGAL,24)
        if alpha is not None:
            CGAL_genepy3d.getAlphaShape(pointsCGAL,pointsCGALas,pointsCGALastri,alpha)
        else :
            alpha=CGAL_genepy3d.getOptimalAlphaShape(pointsCGAL,pointsCGALas,pointsCGALastri)
        # print('alpha:'+str(alpha))
        simplicesc=np.array([tuple([p.x(),p.y(),p.z()]) for t in pointsCGALastri for p in [t.vertex(0),t.vertex(1),t.vertex(2)] ])
        vertices=list({tuple(x) for x in [simplicesc[i,:] for i in range(len(simplicesc))]})
        simplices=[vertices.index(tuple(simplicesc[i])) for i in range(len(simplicesc))]
        simplices=np.reshape(np.array(simplices),(-1,3))
        
        return cls(np.array(vertices), simplices)
    
    @staticmethod
    def get_optimal_alpha_shape(points):
        """Return optimal alpha shape parameter from point cloud.
        
        Args:
            points (nx3 array of float): coordinates of point cloud.
        
        Returns:
            alpha value.
        
        """
        
        from CGAL import CGAL_genepy3d
        from CGAL.CGAL_Kernel import Point_3
        from CGAL import CGAL_Point_set_processing_3 as psp
        
        pointsCGAL= []
        pointsCGALas= []
        pointsCGALastri= []
        for i in range(points.shape[0]):
            pointsCGAL.append(Point_3(points[i,0],points[i,1],points[i,2]))
            
        psp.jet_smooth_point_set(pointsCGAL,24)
        
        return CGAL_genepy3d.getOptimalAlphaShape(pointsCGAL,pointsCGALas,pointsCGALastri)
        
    
    @classmethod
    def from_points_surface_reconstruction(cls,points): #TODO
        """Create surface object from point cloud via CGAL surface reconstruction algorithms.
        
        TODO
        
        Args:
            afile (string): path to load
        
        Returns:
            a Surface object
        """       
        return
    
    @classmethod
    def from_OFF(cls,afile): #TODO
        """Create surface object from OFF file. Does no check on the loaded mesh.
        
       TODO
       
        Args:
            afile (string): path to load
        
        Returns:
            a Surface object
        """       
        return
    
    @classmethod
    def from_STL(cls,afile,xy2zratio=None,center=False): 
        """Create surface object from STL file. Does no check on the loaded mesh.
        
        Args:
            afile (string): path to load
            xy2zratio (float): in case of anisotromic measurement, ratio to apply to z coordinates w.r.t. x and y 
            center (bool): center the mesh
        
        Returns:
            a Surface object
        """
         
        from stl import mesh
        
        your_mesh = mesh.Mesh.from_file(afile)
        points=np.reshape(your_mesh.data['vectors'],[3*your_mesh.data['vectors'].shape[0],3])
        points=np.unique(points,axis=0)
 
        inds=[]
        for i in range(your_mesh.data['vectors'].shape[0]):
            for j in range(your_mesh.data['vectors'].shape[1]):
                inds.append(np.where([(points[k,:]==your_mesh.data['vectors'][i][j]).all() for k in range(len(points))])[0])
        inds=np.reshape(np.stack(inds),your_mesh.data['vectors'].shape[0:2])  
        #points_centered=preprocessing.scale(points,with_std=False)    
        if center:
            points[:,0]=points[:,0]-np.mean(points[:,0])
            points[:,1]=points[:,1]-np.mean(points[:,1])
            points[:,2]=points[:,2]-np.mean(points[:,2])
        if xy2zratio:
            points[:,2]=points[:,2]*xy2zratio
            
        
        return cls(points,inds)

    @classmethod
    def from_volume(cls,vol,level,spacing=(1.,1.,1.),step_size=1):
        """Create isosurface from 3D volume.
        """
        
        # extend volume shape to avoid missing faces at border
        ext = step_size + 5
        extvol = np.zeros((vol.shape[0]+2*ext,vol.shape[1]+2*ext,vol.shape[2]+2*ext))
        extvol[ext:ext+vol.shape[0],ext:ext+vol.shape[1],ext:ext+vol.shape[2]] = vol
        
        if isinstance(level,int):
            extvol[extvol!=level]=0.
        else:
            for lev in level:
                extvol[extvol!=lev] = 0.
        extvol[extvol!=0] = 1.
        
        # get isosurface by lewiner algorithm
        verts, faces, _, _ = measure.marching_cubes_lewiner(extvol, level=0., spacing=spacing, step_size=step_size)
        
        # get vertice coordinates back to the origin
        verts = verts - ext
        
        return cls(verts[:,[2,1,0]],faces)
        
    
    def export_to_VTK(self,filepath,kind='PolyData'):
        """export surface as unstructured mesh in VTK fileformat
        
        Args:
            filepath (string): path to export the file to, *with no extention*
        
        """
        
        if kind == 'PolyData':
            
            Points = vtk.vtkPoints()
            Triangles = vtk.vtkCellArray()
            
            for p in self.vertices:
                Points.InsertNextPoint(p[0],p[1],p[2])

            for s in self.simplices:            
                Triangle = vtk.vtkTriangle()
            
                Triangle.GetPointIds().SetId(0, s[0])
                Triangle.GetPointIds().SetId(1, s[1])
                Triangle.GetPointIds().SetId(2, s[2])
                Triangles.InsertNextCell(Triangle)
        
            polydata = vtk.vtkPolyData()
            polydata.SetPoints(Points)
            polydata.SetPolys(Triangles)
            polydata.Modified()
        
            writer = vtk.vtkPolyDataWriter()
            writer.SetFileName(filepath)
            writer.SetInputData(polydata)
            writer.Write()

        if kind== 'UnstructuredGrid':
            offset=[]
            conn=[]
            for s in self.simplices:
                    conn.extend(s)
                    offset.append(3)
            offset=np.array(offset)
            conn=np.array(conn)
    
            celltype=np.ones(len(self.simplices))*VtkTriangle.tid      
    
            unstructuredGridToVTK(filepath, np.ascontiguousarray(self.vertices[:,0]),  np.ascontiguousarray(self.vertices[:,1]),  np.ascontiguousarray(self.vertices[:,2]), connectivity = conn, offsets = offset, cell_types = celltype, cellData = None, pointData = None)
    
    def plot(self,ax,**kwds):
        """Plot outline in 3d or 2d (xy, xz and yz).
        
        Args
            ax: axis to be plotted.
            projection (str): support '3d'|'xy'|'xz'|'yz'.
            scales: (tuples [float]): scales in x y and z.
            args_3d (dic): matplotlib arguments to plot 3d boundary (set of 3d polygons). 
            args_2d (dic): matplotlib arguments to plot 2d boundary.
            equal_aspect (bool): make equal aspect for both axes.

        """
        if 'projection' in kwds.keys():
            projection = kwds['projection']
        else:
            projection = '3d'

        if 'scales' in kwds.keys():
            scales=kwds['scales']
        else:
            scales=(1.,1.,1.)
            
        if 'args_2d' in kwds.keys():
            args_2d = kwds['args_2d']
        else:
            args_2d = {'edgecolor':'yellow','edgewidth':1,'facecolor':None,'alpha':0.5,'divby':'row','ndiv':1}
            
        if 'args_3d' in kwds.keys():
            args_3d = kwds['args_3d']
        else:
            args_3d = {'edgecolor':'yellow','facecolor':'yellow','alpha':0.3}
            
        if 'equal_aspect' in kwds.keys():
            equal_aspect = kwds['equal_aspect']
        else:
            equal_aspect = True
            
        vertices_scale = np.zeros(self.vertices.shape)            
        vertices_scale[:,0] = 1.*self.vertices[:,0]/scales[0]
        vertices_scale[:,1] = 1.*self.vertices[:,1]/scales[1]
        vertices_scale[:,2] = 1.*self.vertices[:,2]/scales[2]

        
        if projection=='3d':
            self._plot3d(ax,vertices_scale,args_3d)
            if equal_aspect == True:
                param = pl.fix_equal_axis(self.vertices)
                ax.set_xlim(param['xmin'],param['xmax'])
                ax.set_ylim(param['ymin'],param['ymax'])
                ax.set_zlim(param['zmin'],param['zmax'])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            
        else:
            if projection=='xy':
                coors2d = vertices_scale[:,[0,1]]
            elif projection=='xz':
                coors2d = vertices_scale[:,[0,2]]
            else:
                coors2d = vertices_scale[:,[1,2]]
            
            self._plot2d(ax,coors2d,**args_2d)
            
            if equal_aspect==True:
                ax.axis('equal')
                
    def _plot3d(self,ax,coors,args_3d={"edgecolor":'yellow',"facecolor":'yellow',"alpha":"0.3"}):
        """Support 3d plot outline.
        
        Args:
            ax: axis to be plotted.
            coors (2d numpy array [float]): 3d coordinates of outline.
            edgecolor (str): edge color.
            facecolor (str): face color.
            alpha (float): transparent.
        
        """
        
        ax.plot_trisurf(coors[:, 0], coors[:,1], self.simplices, coors[:, 2],**args_3d)
        
        #for simplex in self.simplices:
        #    tri = mplot3d.art3d.Poly3DCollection([coors[simplex,:].tolist()],**args_3d)
        #    # tri.set_color(facecolor)
        #    # tri.set_edgecolor(edgecolor)
        #    ax.add_collection3d(tri)
                
    
    def _plot2d(self,ax,coors,edgecolor='yellow',edgewidth=1,facecolor=None,alpha=0.5,divby='row',ndiv=1):
        """Support 2d plot of outline.
        
        Allow plotting outline in different divisions along a specific axis.
        
        Args:
            ax: axis to be plotted.
            coors (2d numpy array [float]): 2d coordinates of outline.
            edgecolor (str): edge color.
            edgewidth (float): edge width.
            facecolor (str|list|matplotlib_colormap): face color.
            alpha (float): transparent.
            divby (str): axis of division, support 'row'|'col'.
            ndiv (int): number of division along specific axis.
        
        """
        
        boundary = np.array(self.vertices.tolist()+[self.vertices[0]])
        xbound, ybound = coors[boundary,0], coors[boundary,1]
        
        if ndiv==1:
            if facecolor is None:
                ax.plot(xbound,ybound,c=edgecolor,lw=edgewidth,alpha=alpha)
            else:
                ax.fill(xbound,ybound,ec=edgecolor,lw=edgewidth,fc=facecolor,alpha=alpha)
        else:
            coef, t = interpolate.splprep([xbound, ybound], k=1)
            tnew = np.linspace(0,1,500)
            xnew, ynew = interpolate.splev(tnew,coef) # generate xnew, ynew which fill inside of outline
            if divby=='row':
                slices = np.linspace(ynew.min(),ynew.max(),ndiv+1)
                vals = ynew
            else:
                slices = np.linspace(xnew.min(),xnew.max(),ndiv+1)
                vals = xnew
            
            for i in range(len(slices)-1):
                idx = np.argwhere((vals>=slices[i])&(vals<=slices[i+1])).flatten()
                if facecolor is not None:
                    
                    if type(facecolor) is list:
                        _fc = facecolor[i]
                    elif type(facecolor) is str:
                        _fc = facecolor
                    else: # color map
                        _fc = facecolor(i*1.0/(len(slices)-1))

                    ax.fill(xnew[idx],ynew[idx],fc=_fc,ec=edgecolor,lw=edgewidth,alpha=alpha)
                else:
                    ax.plot(xnew[idx],ynew[idx],c=edgecolor,lw=edgewidth,alpha=alpha)
        

        
