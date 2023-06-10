import React, { useEffect, useState } from "react";
import { Button, Container, Table } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { LineDiagram } from "../utils";
import { useGlobalState, useProtectedRoute } from "./hooks";

export function ApplianceList() {
  useProtectedRoute();
  const { globalState } = useGlobalState();
  const { email, onGrid } = globalState;
  const navigate = useNavigate();
  const [appliances, setAppliances] = useState([]);

  useEffect(() => {
    // Fetch appliances for the user's email address and set the state
    // Replace this with the actual API call
    if (!email) return;
    fetch("/api/appliances/" + email)
      .then((res) => res.json())
      .then((response) => {
        console.log(response.data); // log the response data object
        const { data } = response.data;
        setAppliances(data);
      });
  }, [email]);

  const headings = Object.keys(
    appliances.length > 0 ? appliances[0] : {}
  ).slice(1);

  const handleDelete = (apNumber) => {
    // Call an API to delete the appliance from the SQL table
    // Delete pgNumber and email
    fetch("/api/appliance-delete/" + apNumber + "/" + email, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then((response) => {
        // After deleting, refetch appliances and update the state
        fetch("/api/appliances/" + email)
          .then((res) => res.json())
          .then((response) => {
            const { data } = response.data;
            console.log(data);
            setAppliances(data);
          });
      })
      .catch((error) => console.log(error));

    console.log(apNumber);
  };

  const isTableEmpty = !Array.isArray(appliances) || appliances.length === 0;

  return (
    <Container>
      <LineDiagram currentStep={1} />
      <h1>Appliances</h1>
      <h5>You have added the following appliances to your household:</h5>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Appliance #</th>
            <th>Type</th>
            <th>Manufacturer</th>
            <th>Model</th>
          </tr>
        </thead>
        <tbody>
          {Array.isArray(appliances) && appliances.length > 0 ? (
            appliances.map((appliance, index) => (
              <tr key={index}>
                {/* Orders headings and removes last (btu_rating)*/}
                {["1", "3", "2", "4"].map((heading) => (
                  <td key={heading}>{appliance[heading]}</td>
                ))}
                <td>
                  <Button
                    variant="danger"
                    onClick={() => handleDelete(appliance[headings[0]])}
                  >
                    Delete
                  </Button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={headings.length + 1}>No appliances found</td>
            </tr>
          )}
        </tbody>
      </Table>
      <Button variant="primary" onClick={() => navigate("/NewAppliance")}>
        Add Another Appliance
      </Button>
      {!isTableEmpty && (
        <Button
          variant="success"
          className="ml-2"
          onClick={() => navigate("/NewPowerGeneration")}
        >
          Next
        </Button>
      )}
    </Container>
  );
}

export default ApplianceList;
