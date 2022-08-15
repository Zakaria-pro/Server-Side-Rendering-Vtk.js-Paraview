# pv_server.py
# import to process args
import os

# import paraview modules.
from paraview.web import pv_wslink
from paraview.web import protocols as pv_protocols

from paraview import simple
from wslink import server

import argparse

# =============================================================================
# Create custom PVServerProtocol class to handle clients requests
# =============================================================================


class _DemoServer(pv_wslink.PVServerProtocol):
    authKey = "wslink-secret"

    def initialize(self):
        # Bring used components
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebMouseHandler())
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPort())
        self.registerVtkWebProtocol(
            pv_protocols.ParaViewWebPublishImageDelivery(decode=False))
        self.updateSecret(_DemoServer.authKey)

        # tell the C++ web app to use no encoding.
        # ParaViewWebPublishImageDelivery must be set to decode=False to match.
        self.getApplication().SetImageEncoding(0)
        
        colorPalette = simple.GetSettingsProxy('ColorPalette')
        colorPalette.Background = [1.0, 1.0, 1.0]

        # Disable interactor-based render calls
        simple.GetRenderView().EnableRenderOnInteraction = 0
        simple.GetRenderView().Background = [0.5, 0.5, 0]
        # cone = simple.Sphere()
        
        ## STL File
        
        # cone = simple.STLReader(registrationName='40DP-19T-OD12.17.stl', FileNames=['C:\\dev\\voxel-app\\samples\\STL\\40DP-19T-OD12.17.stl'])
        
        ## PartitionedUnstructuredGrid
        # cone = simple.XMLPartitionedUnstructuredGridReader(registrationName='quad-tri.pvtu', FileName=['./examples/vtk/xml/quad-tri/quad-tri.pvtu'])
                

        # cone = simple.PVDReader(registrationName='rectilinearGrid.pvd', FileName=["./examples/rectilinearGridExample/rectilinearGrid.pvd"])

        cone = simple.LegacyVTKReader(registrationName="rectilinear2d.vtk", FileNames="./examples/vtk/legacy/rectilinear2d.vtk")

        # cone = simple.LegacyVTKReader(registrationName="rectilinear9Cell2d.vtk", FileNames="./examples/vtk/legacy/rectilinear9Cell2d.vtk")
        ## Rectilinear Grid
        print("Reading File ....")
        # cone = simple.LegacyVTKReader(registrationName='test.vtk', FileNames=["./examples/vtk/legacy/test.vtk"])
        # cone = simple.LegacyVTKReader(registrationName='extract-clip.vtk', FileNames=["./examples/vtk/legacy/extract-clip.vtk"])
        print("Finish Reading File")


        # ------------------------------------------------------------------------
        vtkFileBinaryvtkDisplay = simple.Show(cone)
        # data_display.Representation = 'Surface With Edges'

        # set scalar coloring
        # simple.ColorBy(vtkFileBinaryvtkDisplay, ('CELLS', 'Mass-Ratio'))

 

        # rescale color and/or opacity maps used to include current data range
        # vtkFileBinaryvtkDisplay.RescaleTransferFunctionToDataRange(True, False)

  
         # show color bar/color legend
        # vtkFileBinaryvtkDisplay.SetScalarBarVisibility()

        # get color transfer function/color map for 'MassRatio'
        # massRatioLUT = simple.GetColorTransferFunction('MassRatio')

        # get opacity transfer function/opacity map for 'MassRatio'
        # massRatioPWF = simple.GetOpacityTransferFunction('MassRatio')

        # massRatioLUT.ApplyPreset("Turbo", True)

        # change representation type
        vtkFileBinaryvtkDisplay.SetRepresentationType('Surface With Edges')

        # ------------------------------------------------------------------------

        # cone.ThetaResolution = 64
        # print(dir(cone))
        # data_display = simple.Show(cone)
        # data_display.Representation = 'Surface With Edges'
        simple.Render()
        
        # Update interaction mode
        pxm = simple.servermanager.ProxyManager()
        interactionProxy = pxm.GetProxy(
            'settings', 'RenderViewInteractionSettings')
        interactionProxy.Camera3DManipulators = [
            'Rotate', 'Pan', 'Zoom', 'Pan', 'Roll', 'Pan', 'Zoom', 'Rotate', 'Zoom']

# =============================================================================
# Main: Parse args and start server
# =============================================================================


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="ParaViewWeb Demo")

    # Add default arguments
    server.add_arguments(parser)

    # Extract arguments
    args = parser.parse_args()

    # Start server
    server.start_webserver(options=args, protocol=_DemoServer)
