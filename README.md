# Server Side Rendering using VTK.js & Paraview

## Running the Client code (Vtk.js)

1. cd to `vtk-project/Client`

2. install Node dependencies: `npm install`

3. Start project: `npm start`

## Running the Server code (Paraview)

### Add pvpython to the system environment variables

1. Open file explorer

2. Cd to Paraview Binaries folder

3. Copy the Folder path

4. Edit environemnt variables with the new path

### Run the server

5. Cd to `vtk-project/Server`

6. Run the command `pvpython pv_server.py --port 1234`
