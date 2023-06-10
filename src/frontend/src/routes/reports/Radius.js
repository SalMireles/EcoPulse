import { useFormik } from "formik";
import React, { useState } from "react";
import { Button, Col, Container, Form, Row, Spinner } from "react-bootstrap";
import * as yup from "yup";
import { BasicTable } from "../../components/Tables";
import { optionForEach, validatePostal } from "../../utils";

const validRadiusOptions = [0, 5, 10, 25, 50, 100, 250];

const schema = yup.object().shape({
  radius: yup.number().oneOf(validRadiusOptions).default(50).required(),
  zip: yup.string().required().default(""),
  formError: yup.bool().default(false),
});

export function Radius() {
  const [data, setData] = useState(null);

  const { getFieldProps, touched, errors, isSubmitting, handleSubmit } =
    useFormik({
      initialValues: schema.getDefault(),
      validateOnMount: true,
      validationSchema: schema,
      onSubmit: async ({ zip, radius }, { setFieldError, setSubmitting }) => {
        if (!(await validatePostal(zip))) {
          setFieldError("zip", "not a valid zip code");
        } else {
          const resp = await fetch(
            "/api/reports/radius?r=" + radius + "&zip=" + zip
          ).then((r) => r.json());
          if (resp.status === 200) {
            setData(resp.data);
          } else {
            setFieldError("formError", resp.data.err);
          }
        }
        setSubmitting(false);
      },
    });

  return (
    <Container fluid>
      <h1>Radius</h1>
      <Form onSubmit={handleSubmit}>
        <Row className="mb-3">
          <Form.Group as={Col} md="4" controlId="validationCustom01">
            <Form.Label>Zip Code</Form.Label>
            <Form.Control
              placeholder="Zip Code"
              {...getFieldProps("zip")}
              isInvalid={touched.zip && !!errors.zip}
            />
            <Form.Control.Feedback type="invalid">
              {errors.zip}
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group as={Col} md="2" controlId="validationCustom02">
            <Form.Label>Radius (miles)</Form.Label>
            <Form.Select {...getFieldProps("radius")}>
              {optionForEach(validRadiusOptions)}
            </Form.Select>
          </Form.Group>
        </Row>
        <Button type="submit">Search</Button>
      </Form>
      {data && !isSubmitting && (
        <BasicTable headings={data.headings} data={data.data} />
      )}
      {isSubmitting && <Spinner />}
      {errors.formError && <h4>{errors.formError}</h4>}
    </Container>
  );
}

export default Radius;
