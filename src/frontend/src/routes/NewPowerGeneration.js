import { useFormik } from "formik";
import React from "react";
import { Button, Container, Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import * as yup from "yup";
import { formTypes, LineDiagram, optionForEach, postJson } from "../utils";
import { useGlobalState, useProtectedRoute } from "./hooks";

const powerGeneratorTypes = ["Solar-Electric", "Wind"];

const schema = yup.object().shape({
  type: yup.string().required().oneOf(powerGeneratorTypes),
  monthlyKWh: formTypes.requiredWholeNum(),
  storageKWh: formTypes.optionalWholeNum(),
  // This isn't a real field. It's only here as a fallback to allow
  // global form errors on unexpected errors from the server.
  formError: yup.bool().default(false),
});

export function NewPowerGeneration() {
  useProtectedRoute();
  const navigate = useNavigate();

  const { globalState, setGlobalState } = useGlobalState();
  const { email, onGrid, nextPgNum } = globalState;

  const handleAdd = async (
    /*values*/ { type, monthlyKWh, storageKWh },
    /*helpers*/ { setSubmitting, setFieldError }
  ) => {
    const resp = await postJson("/api/power-generation/create", {
      pgNum: nextPgNum,
      email,
      type,
      monthlyKWh,
      storageKWh: storageKWh ? storageKWh : null,
    });
    if (resp.status === 200) {
      setGlobalState((s) => ({ ...s, nextPgNum: s.nextPgNum + 1 }));
      navigate("/PowerGenerationList");
    } else {
      setFieldError("formError", resp.data.err);
    }
    setSubmitting(false);
  };

  const {
    getFieldProps,
    touched,
    isValid,
    errors,
    handleSubmit,
    isSubmitting,
  } = useFormik({
    initialValues: {
      type: "",
      formError: false,
      monthlyKWh: "",
      storageKWh: "",
    },
    validateOnMount: true,
    onSubmit: handleAdd,
    validationSchema: schema,
  });

  return (
    <Container>
      <LineDiagram currentStep={2} />
      <Form noValidate onSubmit={handleSubmit}>
        <h1>Add Power Generation</h1>
        <h5>Please provide power generation details.</h5>
        <Form.Group className="mb-3" controlId="type">
          <Form.Label>Type</Form.Label>
          <Form.Select
            aria-label="Default select example"
            name="type"
            {...getFieldProps("type")}
            isInvalid={touched.type && !!errors.type}
          >
            <option disabled value="">Select a Type</option>
            {optionForEach(powerGeneratorTypes)}
          </Form.Select>
          <Form.Control.Feedback type="invalid">
            {errors.type}
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group className="mb-3" controlId="monthlyKWh">
          <Form.Label>Monthly KWh</Form.Label>
          <Form.Control
            type="number"
            name="monthlyKWh"
            min={0}
            step={1}
            placeholder="500"
            {...getFieldProps("monthlyKWh")}
            isInvalid={touched.monthlyKWh && !!errors.monthlyKWh}
          />
          <Form.Control.Feedback type="invalid">
            {errors.monthlyKWh}
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group className="mb-3" controlId="storageKWh">
          <Form.Label>Storage KWh (optional)</Form.Label>
          <Form.Control
            type="number"
            name="storageKWh"
            placeholder="100"
            {...getFieldProps("storageKWh")}
            isInvalid={touched.storageKWh && !!errors.storageKWh}
          />
          <Form.Control.Feedback type="invalid">
            {errors.storageKWh}
          </Form.Control.Feedback>
        </Form.Group>

        <Button
          variant="primary"
          type="submit"
          disabled={!isValid || isSubmitting}
        >
          Add
        </Button>
        {onGrid && (
          <Button
            variant="secondary"
            onClick={() => navigate("/SubmissionComplete")}
            disabled={isSubmitting}
          >
            Skip
          </Button>
        )}
        {!!errors.formError && <div>{errors.formError}</div>}
      </Form>
    </Container>
  );
}

export default NewPowerGeneration;
