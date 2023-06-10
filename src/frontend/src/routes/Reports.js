import React from "react";
import { Container } from "react-bootstrap";
import { Link } from "react-router-dom";

export function Reports() {
  return (
    <Container>
      <h1>Reports</h1>
      <div>
        <ul>
          <li>
            <Link to="manufacturers">Top Manufacturers</Link>
          </li>
          <li>
            <Link to="modelsearch">Manufacturer/Model Search</Link>
          </li>
          <li>
            <Link to="heatingcooling">Heating/Cooling Methods</Link>
          </li>
          <li>
            <Link to="waterheaters">Water Heater Statistics</Link>
          </li>
          <li>
            <Link to="offgrid">Off Grid Households</Link>
          </li>
          <li>
            <Link to="radius">Household Averages by Radius</Link>
          </li>
        </ul>
      </div>
    </Container>
  );
}

export default Reports;
