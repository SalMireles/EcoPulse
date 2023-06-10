import React, { useEffect } from "react";
import { Container } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useGlobalState } from "./hooks";
import { LineDiagram } from "../utils";

export function SubmissionComplete() {
  const { resetGlobalState } = useGlobalState();
  // Reset the global state for the next possible household.
  useEffect(() => {
    resetGlobalState();
  }, []);
  return (
    <Container>
      <LineDiagram currentStep={3} />
      <h1>Submission complete!</h1>
      <h3>Thank you for providing your information to Alternakraft!</h3>
      <p>
        <Link to="/">Return to the main menu</Link>
      </p>
    </Container>
  );
}
