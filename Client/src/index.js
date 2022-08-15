import vtkWSLinkClient from "@Kitware/vtk.js/IO/Core/WSLinkClient";
import SmartConnect from "wslink/src/SmartConnect";
import vtkRemoteView from "@Kitware/vtk.js/Rendering/Misc/RemoteView";

vtkWSLinkClient.setSmartConnectClass(SmartConnect);

document.body.style.padding = "0";
document.body.style.margin = "0";

const divRenderer = document.createElement("div");
document.body.appendChild(divRenderer);

const header = document.createElement("h1");
document.body.appendChild(header);
header.textContent = "Hello Zakariae";

divRenderer.style.position = "relative";
divRenderer.style.width = "100vw";
divRenderer.style.height = "100vh";
divRenderer.style.overflow = "hidden";

const clientToConnect = vtkWSLinkClient.newInstance();

// Error
clientToConnect.onConnectionError((httpReq) => {
  const message =
    (httpReq && httpReq.response && httpReq.response.error) ||
    `Connection error`;
  console.error(message);
  console.log(httpReq);
});

// Close
clientToConnect.onConnectionClose((httpReq) => {
  const message =
    (httpReq && httpReq.response && httpReq.response.error) ||
    `Connection close`;
  console.error(message);
  console.log(httpReq);
});

// hint: if you use the launcher.py and ws-proxy just leave out sessionURL
// (it will be provided by the launcher)
const config = {
  application: "cone",
  sessionURL: "ws://localhost:1234/ws",
};
const style = "font-weight: bold; color: green";

// Connect
clientToConnect
  .connect(config)
  .then((validClient) => {
    const viewStream = clientToConnect.getImageStream().createViewStream("-1");
    const view = vtkRemoteView.newInstance({
      rpcWheelEvent: "viewport.mouse.zoom.wheel",
      viewStream,
    });
    const session = validClient.getConnection().getSession();

    view.setSession(session);
    view.setContainer(divRenderer);
    view.setInteractiveRatio(0.7); // the scaled image compared to the clients view resolution
    view.setInteractiveQuality(2000); // jpeg quality
    console.log("%c Connected Successfully to the Server ..", style);

    window.addEventListener("resize", view.resize);
  })
  .catch((error) => {
    console.error(error);
  });
