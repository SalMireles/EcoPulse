import { useFormik } from "formik";
import React, { useEffect } from "react";
import { Button, Container, Form } from "react-bootstrap";
import { flushSync } from "react-dom";
import { useNavigate } from "react-router-dom";
import * as yup from "yup";
import {
  formTypes,
  postJson,
  validateEmail,
  validatePostal,
  LineDiagram,
} from "../utils";
import { useGlobalState } from "./hooks";

const boolType = () => yup.bool().required().default(false);
const schema = yup.object().shape({
  email: formTypes.requiredString().email(),
  postalCode: formTypes.requiredString(),
  type: formTypes
    .requiredString()
    .oneOf(["house", "townhome", "mobile_home", "condominium", "apartment"])
    .default("house"),
  squareFootage: formTypes.requiredWholeNum(),
  tsHeating: formTypes.optionalWholeNum(),
  noHeating: boolType().when("tsHeating", ([tsHeating], schema) =>
    tsHeating
      ? schema
      : schema.oneOf([true], "must be set if 'no heat' not checked")
  ),
  tsCooling: formTypes.optionalWholeNum(),
  noCooling: boolType().when("tsCooling", ([tsCooling], schema) =>
    tsCooling
      ? schema
      : schema.oneOf([true], "must be set if 'no cooling' not checked")
  ),
  electric: boolType(),
  gas: boolType(),
  steam: boolType(),
  fuelOil: boolType(),
  // Form-level error for unexpected submissions errors at the form level.
  formError: boolType(),
});

export function NewHousehold() {
  const navigate = useNavigate();
  const { setGlobalState, resetGlobalState } = useGlobalState();

  // Reset the global state on load.
  useEffect(() => {
    resetGlobalState();
  }, []);

  const {
    getFieldProps,
    touched,
    isValid,
    errors,
    handleSubmit,
    isSubmitting,
    values,
  } = useFormik({
    initialValues: {
      ...schema.getDefault(),
      // Initialize all numeric types to empty
      tsCooling: "",
      tsHeating: "",
      squareFootage: "",
    },
    validateOnMount: true,
    validationSchema: schema,
    onSubmit: async (values, { setFieldError, setSubmitting }) => {
      let data = {
        ...values,
        tsHeating: values.noHeating ? null : values.tsHeating,
        tsCooling: values.noCooling ? null : values.tsCooling,
        onGrid: values.electric || values.gas || values.fuelOil || values.steam,
      };

      const [isValidPostal, isValidEmail] = await Promise.all([
        validatePostal(values.postalCode),
        validateEmail(values.email),
      ]);

      if (isValidEmail && isValidPostal) {
        const resp = await postJson("/api/household/create", data);
        if (resp.status === 200) {
          // Prevent race with next page's redirect hook by using flushSync
          flushSync(() =>
            setGlobalState((s) => ({
              ...s,
              email: data.email,
              onGrid: data.onGrid,
            }))
          );
          navigate("/newappliance");
        } else {
          console.log("ERROR", resp);
          setFieldError("formError", resp.data.err);
        }
      } else {
        if (!isValidPostal) {
          setFieldError("postalCode", "postal code does not exist");
        }
        if (!isValidEmail) {
          setFieldError("email", "email already taken");
        }
      }

      setSubmitting(false);
    },
  });

  return (
    <Container>
      <LineDiagram currentStep={0} />
      <Form noValidate onSubmit={handleSubmit}>
        <h1>Enter household info</h1>

        <Form.Group className="mb-3" controlId="email">
          <Form.Label>Please enter your email address:</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            {...getFieldProps("email")}
            isInvalid={touched.email && !!errors.email}
          />
          <Form.Control.Feedback type="invalid">
            {errors.email}
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group className="mb-3" controlId="postalCode">
          <Form.Label>Please enter your five digit postal code:</Form.Label>
          <Form.Control
            placeholder="30332"
            {...getFieldProps("postalCode")}
            isInvalid={touched.postalCode && !!errors.postalCode}
          />
          <Form.Control.Feedback type="invalid">
            {errors.postalCode}
          </Form.Control.Feedback>
        </Form.Group>

        <h5>
          <span style={{ fontWeight: "normal", fontSize: "16px" }}>
            Please enter the following details for your household.
          </span>
        </h5>

        <Form.Group className="mb-3" controlId="type">
          <Form.Label>Home type</Form.Label>
          <Form.Select {...getFieldProps("type")}>
            <option value="house">House</option>
            <option value="apartment">Apartment</option>
            <option value="townhome">Townhome</option>
            <option value="condominium">Condominium</option>
            <option value="mobile_home">Mobile Home</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3" controlId="squareFootage">
          <Form.Label>Square footage</Form.Label>
          <Form.Control
            placeholder="2200"
            type="number"
            {...getFieldProps("squareFootage")}
            isInvalid={touched.squareFootage && !!errors.squareFootage}
          />
          <Form.Control.Feedback type="invalid">
            {errors.squareFootage}
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Thermostat setting for heating</Form.Label>
          <Form.Control
            id="tsHeating"
            type="number"
            placeholder="72"
            {...getFieldProps("tsHeating")}
            isInvalid={
              (touched.tsHeating || touched.noHeating) &&
              (!!errors.tsHeating || !!errors.noHeating)
            }
            disabled={values.noHeating}
          />
          <Form.Control.Feedback type="invalid">
            {errors.tsHeating || errors.noHeating}
          </Form.Control.Feedback>
          <Form.Check
            id="noHeating"
            type="checkbox"
            label="No heat"
            {...getFieldProps("noHeating")}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Thermostat setting for cooling</Form.Label>
          <Form.Control
            id="tsCooling"
            placeholder="68"
            type="number"
            {...getFieldProps("tsCooling")}
            disabled={values.noCooling}
            isInvalid={
              (touched.tsCooling || touched.noCooling) &&
              (!!errors.tsCooling || !!errors.noCooling)
            }
          />
          <Form.Control.Feedback type="invalid">
            {errors.tsCooling || errors.noCooling}
          </Form.Control.Feedback>
          <Form.Check
            id="tsCoolingCheck"
            type="checkbox"
            label="No cooling"
            {...getFieldProps("noCooling")}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Public utilities</Form.Label>
          <Form.Check
            id="electric"
            type="checkbox"
            label="Electric"
            {...getFieldProps("electric")}
          />
          <Form.Check
            id="gas"
            type="checkbox"
            label="Gas"
            {...getFieldProps("gas")}
          />
          <Form.Check
            id="steam"
            type="checkbox"
            label="Steam"
            {...getFieldProps("steam")}
          />
          <Form.Check
            id="fuelOil"
            type="checkbox"
            label="Fuel oil"
            {...getFieldProps("fuelOil")}
          />
          <Form.Text className="text-muted">
            If none, leave unchecked.
          </Form.Text>
        </Form.Group>

        <Button
          variant="primary"
          type="submit"
          disabled={!isValid || isSubmitting}
          onClick={handleSubmit}
        >
          Next
        </Button>
        {!!errors.formError && <div>{errors.formError}</div>}
      </Form>
    </Container>
  );
}

export default NewHousehold;
