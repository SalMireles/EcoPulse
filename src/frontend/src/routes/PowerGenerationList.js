import React, { useEffect, useState } from "react";
import { Button, Container, Table } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useGlobalState, useProtectedRoute } from "./hooks";
import { LineDiagram } from "../utils";

export function PowerGenerationList() {
  useProtectedRoute();
  const { globalState } = useGlobalState();
  const { email, onGrid } = globalState;
  const navigate = useNavigate();
  const [powerGenerations, setPowerGenerations] = useState([]);

  useEffect(() => {
    // Fetch power generations for the user's email address and set the state
    // Replace this with the actual API call
    if (!email) return;
    fetch("/api/power-generation-methods-list/" + email)
      .then((res) => res.json())
      .then((response) => {
        console.log(response.data); // log the response data object
        const { data } = response.data;
        setPowerGenerations(data);
      });
  }, [email]);

  const headings = Object.keys(
    powerGenerations.length > 0 ? powerGenerations[0] : {}
  ).slice(1);

  const handleDelete = (pgNumber) => {
    // Call an API to delete the power generation method from the SQL table
    // Delete pgNumber and email
    fetch("/api/power-generation-delete/" + pgNumber + "/" + email, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then((response) => {
        // After deleting, refetch the power generation methods and update the state
        fetch("/api/power-generation-methods-list/" + email)
          .then((res) => res.json())
          .then((response) => {
            const { data } = response.data;
            console.log(data);
            setPowerGenerations(data);
          });
      })
      .catch((error) => console.log(error));

    console.log(pgNumber);
  };

  const isTableEmpty =
    !Array.isArray(powerGenerations) || powerGenerations.length === 0;

  return (
    <Container>
      <LineDiagram currentStep={2} />
      <h1>Power Generation</h1>
      <h5>You have added these to your household:</h5>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Num</th>
            <th>Type</th>
            <th>Monthly KWh</th>
            <th>Battery KWh</th>
          </tr>
        </thead>
        <tbody>
          {Array.isArray(powerGenerations) && powerGenerations.length > 0 ? (
            powerGenerations.map((powerGeneration, index) => (
              <tr key={index}>
                {/* Use the attribute values to generate the table cells */}
                {headings.map((heading) => (
                  <td key={heading}>{powerGeneration[heading]}</td>
                ))}
                <td>
                  <Button
                    variant="danger"
                    onClick={() => handleDelete(powerGeneration[headings[0]])}
                  >
                    Delete
                  </Button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={headings.length + 1}>No power generations found</td>
            </tr>
          )}
        </tbody>
      </Table>
      <Button variant="primary" onClick={() => navigate("/newpowergeneration")}>
        Add Another Power Generator
      </Button>
      {(onGrid || !isTableEmpty) && (
        <Button
          variant="success"
          className="ml-2"
          onClick={() => navigate("/submissioncomplete")}
        >
          Finish
        </Button>
      )}
    </Container>
  );
}

export default PowerGenerationList;
