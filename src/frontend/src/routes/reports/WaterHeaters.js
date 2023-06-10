import React from "react";
import { Container, Spinner } from "react-bootstrap";
import { useParams } from "react-router-dom";
import { BasicTable, LinkifiedTable } from "../../components/Tables";
import { useFetch } from "../hooks";

export function WaterHeatersDrilldown() {
  const { id } = useParams();
  const { data, loading, err } = useFetch("/api/reports/water-heaters/" + id);
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

export function WaterHeaters() {
  const { data, loading, err } = useFetch("/api/reports/water-heaters");

  return (
    <Container>
      <h1>Water Heaters</h1>
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

export default WaterHeaters;
