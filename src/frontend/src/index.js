import "bootstrap/dist/css/bootstrap.min.css";
import React from "react";
import { Container } from "react-bootstrap";
import { createRoot } from "react-dom/client";
import {
  createBrowserRouter,
  Link,
  Outlet,
  RouterProvider
} from "react-router-dom";
import { GlobalStateProvider } from "./GlobalState";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import { NewAppliance } from "./routes/NewAppliance";
import { ApplianceList } from "./routes/ApplianceList";
import { NewHousehold } from "./routes/NewHousehold";
import { NewPowerGeneration } from "./routes/NewPowerGeneration";
import { PowerGenerationList } from "./routes/PowerGenerationList";
import { Reports } from "./routes/Reports";
import { HeatingCooling } from "./routes/reports/HeatingCooling";
import {
  Manufacturer,
  ManufacturerDrilldown
} from "./routes/reports/Manufacturer";
import { ModelSearch } from "./routes/reports/ModelSearch";
import { OffGrid } from "./routes/reports/OffGrid";
import { Radius } from "./routes/reports/Radius";
import {
  WaterHeaters,
  WaterHeatersDrilldown
} from "./routes/reports/WaterHeaters";
import { SubmissionComplete } from "./routes/SubmissionComplete";

function Root() {
  return (
    <Container>
      <h1>Welcome To Alternakraft!</h1>
      <h3>Please choose what you'd like to do:</h3>
      <div>
        <div>
          <Link to="/reports">View Reports/query data</Link>
        </div>
        <div>
          <Link to="/newhousehold">Enter My Household Info</Link>
        </div>
      </div>
      <Outlet />
    </Container>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
  },
  {
    path: "/reports",
    element: <Reports />,
  },
  {
    path: "/reports/manufacturers",
    element: <Manufacturer />,
  },
  {
    path: "/reports/manufacturers/:id",
    element: <ManufacturerDrilldown />,
  },
  {
    path: "/reports/modelsearch",
    element: <ModelSearch />,
  },
  {
    path: "/reports/heatingcooling",
    element: <HeatingCooling />,
  },
  {
    path: "/reports/waterheaters",
    element: <WaterHeaters />,
  },
  {
    path: "/reports/waterheaters/:id",
    element: <WaterHeatersDrilldown />,
  },
  {
    path: "/reports/offgrid",
    element: <OffGrid />,
  },
  {
    path: "/reports/radius",
    element: <Radius />,
  },
  {
    path: "/newhousehold",
    element: <NewHousehold />,
  },
  {
    path: "/newappliance",
    element: <NewAppliance />,

  },
  {
    path: "/appliancelist",
    element: <ApplianceList />,

  },
  {
    path: "/newpowergeneration",
    element: <NewPowerGeneration />,
  },
  {
    path: "/submissioncomplete",
    element: <SubmissionComplete />,
  },
  {
    path: "/powergenerationlist",
    element: <PowerGenerationList />,
  },
]);

const App = () => (
  <GlobalStateProvider>
    <RouterProvider router={router} />
  </GlobalStateProvider>
);

const root = createRoot(document.getElementById("root"));
root.render(<App />);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
