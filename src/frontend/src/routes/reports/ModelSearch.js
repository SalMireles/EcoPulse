import React, { useCallback, useState } from "react";
import { Button, Container, Form, Spinner } from "react-bootstrap";
import { SearchTable } from "../../components/Tables";

export function ModelSearch() {
  const [val, setVal] = useState("");
  const [searchedVal, setSearchedVal] = useState("");
  const [state, setState] = useState({ data: null, err: null, loading: false });

  const search = useCallback(
    (e) => {
      e.preventDefault();
      setState({ ...state, loading: true });
      fetch("/api/reports/model-search?q=" + val)
        .then((res) => res.json())
        .then((res) => {
          if (res.status === 200) {
            setState({ ...state, loading: false, data: res.data, err: null });
            setSearchedVal(val);
          } else if (res.status === 400) {
            setState({
              ...state,
              loading: false,
              data: null,
              err: res.data.err,
            });
          }
        });
    },
    [val]
  );

  const { data, err, loading } = state;

  return (
    <Container>
      <h1>ModelSearch</h1>
      <Form onSubmit={search}>
        <Form.Group className="m-0">
          <Form.Control
            required
            as="input"
            placeholder="search"
            value={val}
            onChange={(e) => setVal(e.target.value)}
            type="text"
          />
          <Button type="submit">Search</Button>
        </Form.Group>
      </Form>
      {data && !loading && (
        <SearchTable headings={data.headings} data={data.data} term={searchedVal} />
      )}
      {loading && <Spinner />}
      {err && <h4>{err}</h4>}
    </Container>
  );
}

export default ModelSearch;
