import React from "react";
import { Container, Spinner } from "react-bootstrap";
import { BasicTable } from "../../components/Tables";
import { useFetch } from "../hooks";

export function HeatingCooling() {
  const { data, loading, err } = useFetch("/api/reports/hcm");

  return (
    <Container>
      <h1>Heating/Cooling Methods</h1>
      {loading ? (
        <Spinner animation="border" />
      ) : (
        <>
          {err ? (
            <h4>{err}</h4>
          ) : (
            <BasicTable headings={data.headings} data={data.data} />
          )}
        </>
      )}
    </Container>
  );
}
