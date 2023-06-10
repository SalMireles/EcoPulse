import React from "react";
import { Container, Spinner } from "react-bootstrap";
import { BasicTable } from "../../components/Tables";
import { useFetch } from "../hooks";

export function OffGrid() {
  const { data, loading, err } = useFetch("/api/reports/off-grid");
  console.log("DATA", data);

  return (
    <Container>
      <h1>Off Grid Dashboard</h1>
      {err && <h4>{err}</h4>}

      {loading && <Spinner animation="border" />}

      {!loading && data && (
        <>
          <h2>State with Most Off-Grid Households</h2>
          <BasicTable
            headings={data.state_records.headings}
            data={data.state_records.data}
          />

          <h2>Average Power Generator Capacity</h2>
          <BasicTable
            headings={data.pg_records.headings}
            data={data.pg_records.data}
          />

          <h2>Power Generators - Percentage by Type</h2>
          <BasicTable
            headings={data.pg_type_records.headings}
            data={data.pg_type_records.data}
          />

          <h2>Water Heater Capacity - On Grid vs Off Grid</h2>
          <BasicTable
            headings={data.average_records.headings}
            data={data.average_records.data}
          />

          <h2>BTU Rating by Appliance Type</h2>
          <BasicTable
            headings={data.btu_records.headings}
            data={data.btu_records.data}
          />
        </>
      )}
    </Container>
  );
}
