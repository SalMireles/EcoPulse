import React from "react";
import { Container, Spinner } from "react-bootstrap";
import { useParams } from "react-router-dom";
import { BasicTable, LinkifiedTable } from "../../components/Tables";
import { useFetch } from "../hooks";

export function ManufacturerDrilldown() {
  const { id } = useParams();
  const { data, loading, err } = useFetch(
    "/api/reports/manufacturer-drilldown/" + id
  );
  return (
    <Container>
      <h1>{id} Drilldown</h1>
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

export function Manufacturer() {
  const { data, loading, err } = useFetch("/api/reports/manufacturers");

  return (
    <Container>
      <h1>Top 25 Manufacturers</h1>
      {loading ? (
        <Spinner animation="border" />
      ) : (
        <>
          {err ? (
            <h4>{err}</h4>
          ) : (
            <LinkifiedTable headings={data.headings} data={data.data} />
          )}
        </>
      )}
    </Container>
  );
}

export default Manufacturer;
