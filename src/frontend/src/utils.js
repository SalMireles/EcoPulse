import React from "react";
import { Container } from "react-bootstrap";
import * as yup from "yup";
import "./LineDiagram.css";

export const postJson = async (route, data) => {
  const rawResponse = await fetch(route, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return await rawResponse.json();
};

export const formTypes = {
  // Define custom versions of our types as a silly workaround for undesirable
  // default behaviour with empty numeric fields:
  // https://github.com/jquense/yup/issues/298#issuecomment-850380270
  requiredWholeNum: () =>
    yup.lazy((v) =>
      v === ""
        ? yup.string().required()
        : yup.number().integer().min(0).required()
    ),
  optionalWholeNum: () =>
    yup.lazy((v) => (v === "" ? yup.string() : yup.number().integer().min(0))),
  optionalWholeNumBetween: (a, b) =>
    yup.lazy((v) => {
      const numberValidation = yup
        .number()
        .integer("Value must be a whole number")
        .min(a, `Number must be greater than or equal to ${a}`)
        .max(b, `Number must be less than or equal to ${b}`)
        .typeError("Value must be a number");
      return v === ""
        ? yup.string().required("Value is required")
        : numberValidation;
    }),
  requiredDecimalBetween: (a, b) =>
    yup.lazy((v) =>
      v === "" ? yup.string().required() : yup.number().min(a).max(b).required()
    ),
  requiredString: () => yup.string().required().default(""),
  requiredSingleDecimalAtLeast: (a) =>
    yup.lazy((v) => {
      const numberValidation = yup
        .number()
        .min(a, `Number must be greater than or equal to ${a}`)
        .required("Number is required")
        .typeError("Value must be a number")
        .test(
          "is-decimal",
          "Please round to single decimal number",
          (value) => (value + "").match(/^(\d+\.\d{1}|\d+)$/) // 5, and 5.0 valid not 5.12
        );
      return v === ""
        ? yup.string().required("Value is required")
        : numberValidation;
    }),
  requiredSingleDecimalBetween: (a, b) =>
    yup.lazy((v) => {
      const numberValidation = yup
        .number()
        .min(a, `Number must be greater than or equal to ${a}`)
        .max(b, `Number must be less than or equal to ${b}`)
        .required("Number is required")
        .typeError("Value must be a number")
        .test(
          "is-decimal",
          "Please round to single decimal number",
          (value) => (value + "").match(/^(\d+\.\d{1}|\d+)$/) // 5, and 5.0 valid not 5.12
        );
      return v === ""
        ? yup.string().required("Value is required")
        : numberValidation;
    }),
  requiredWholeNumBetween: (a, b) =>
    yup.lazy((v) => {
      const numberValidation = yup
        .number()
        .integer("Value must be a whole number")
        .min(a, `Number must be greater than or equal to ${a}`)
        .max(b, `Number must be less than or equal to ${b}`)
        .required("Number is required")
        .typeError("Value must be a number");
      return v === ""
        ? yup.string().required("Value is required")
        : numberValidation;
    }),
};

const isValid = async (path) => {
  const resp = await fetch(path).then((r) => r.json());
  return resp.data.data.valid;
};

// Returns false if the email already exists in the DB, true otherwise.
export const validateEmail = async (email) => {
  return await isValid("/api/validations/email?email=" + email);
};

// Returns true if the zip exists, false otherwise.
export const validatePostal = async (code) => {
  return await isValid("/api/validations/postal-code?postalCode=" + code);
};

export const LineDiagram = ({ currentStep }) => {
  const steps = ["Household info", "Appliances", "Power Generation", "Done"];
  const circles = steps.map((step, index) => (
    <div
      key={index}
      className={`circle ${index === currentStep ? "filled" : ""}`}
    >
      <div className="step-text">{step}</div>
    </div>
  ));

  return (
    <Container fluid className="line-diagram">
      <div className="circles">
        <div className="line"></div>
        {circles}
      </div>
    </Container>
  );
};

export const optionForEach = (els) =>
  els.map((e, i) => (
    <option key={i} value={e}>
      {e}
    </option>
  ));
