import React from "react";
import { Table } from "react-bootstrap";
import { Link } from "react-router-dom";

const TableHead = ({ headings }) => (
  <thead>
    <tr>
      {headings.map((c, i) => (
        <td key={i}>{c}</td>
      ))}
    </tr>
  </thead>
);

export const BasicTable = ({ headings, data }) => {
  return data ? (
    <Table striped bordered hover>
      <TableHead headings={headings} />
      <tbody>
        {data.map((row, i) => {
          return (
            <tr key={i}>
              {row.map((c, j) => (
                <td key={j}>{c}</td>
              ))}
            </tr>
          );
        })}
      </tbody>
    </Table>
  ) : null;
};

export const SearchTable = ({ headings, data, term }) => {
  const termLower = term.toLowerCase();

  return data ? (
    <Table striped bordered hover>
      <TableHead headings={headings} />
      <tbody>
        {data.map((row, i) => {
          return (
            <tr key={i}>
              {row.map((c, j) => {
                const cLower = c.toLowerCase();
                return (
                  <td
                    key={j}
                    style={{
                      backgroundColor: cLower.includes(termLower)
                        ? "#e6ffe6"
                        : "transparent",
                    }}
                  >
                    {c}
                  </td>
                );
              })}
            </tr>
          );
        })}
      </tbody>
    </Table>
  ) : null;
};

export const LinkifiedTable = ({ headings, data }) => {
  return (
    <Table striped bordered hover>
      <TableHead headings={headings} />
      <tbody>
        {data.map((row, i) => (
          <tr key={i}>
            {row.map((c, j) => (
              <td key={j}>{j === 0 ? <Link to={c}>{c}</Link> : c}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};
