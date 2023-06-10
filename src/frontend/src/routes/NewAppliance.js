import { useFormik } from "formik";
import React, { useEffect, useState } from "react";
import { Button, Container, Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import * as yup from "yup";
import { formTypes, LineDiagram, optionForEach, postJson } from "../utils";
import { useFetch, useGlobalState, useProtectedRoute } from "./hooks";

const applianceTypes = ["Air Handler", "Water Heater"];
const waterHeaterEnergySources = [
  "Electric",
  "Gas",
  "Thermosolar",
  "Heat Pump",
];
const heaterEnergySources = ["Electric", "Gas", "Fuel Oil"];

const schema = yup.object().shape({
  formError: yup.bool().default(false),
  applianceType: formTypes.requiredString().oneOf(applianceTypes),
  manufacturer: formTypes.requiredString(),
  model: yup.string().default(""),
  btuRating: formTypes.requiredWholeNum(),
  waterHeater: yup.object().when("applianceType", {
    is: (v) => v === "Water Heater",
    then: () =>
      yup.object({
        // freezing and boiling points are reasonable bounds
        temp: formTypes.optionalWholeNumBetween(32, 212),
        capacity: formTypes.requiredSingleDecimalAtLeast(0.0),
        energySource: formTypes
          .requiredString()
          .oneOf(waterHeaterEnergySources),
      }),
  }),
  airHandler: yup.object().when("applianceType", {
    is: (v) => v === "Air Handler",
    then: () =>
      yup.object({
        hasAc: yup.bool().required().default(false),
        hasHeater: yup.bool().required().default(false),
        hasHeatPump: yup.bool().required().default(false),
        atLeastOneMethod: yup
          .bool()
          .default(false)
          .test(
            "method-set",
            "must set at least one heating/cooling method",
            (_, ctx) =>
              ctx.parent.hasAc || ctx.parent.hasHeater || ctx.parent.hasHeatPump
          ),
        ac: yup.object().when("hasAc", {
          is: true,
          then: () =>
            yup.object({
              eer: formTypes.requiredSingleDecimalAtLeast(0.0),
            }),
        }),
        heater: yup.object().when("hasHeater", {
          is: true,
          then: () =>
            yup.object({
              energySource: formTypes
                .requiredString()
                .oneOf(heaterEnergySources),
            }),
        }),
        heatPump: yup.object().when("hasHeatPump", {
          is: true,
          then: () =>
            yup.object({
              seer: formTypes.requiredSingleDecimalAtLeast(0.0),
              hspf: formTypes.requiredSingleDecimalAtLeast(0.0),
            }),
        }),
      }),
  }),
});

const initialVals = {
  formError: false,
  applianceType: "",
  manufacturer: "",
  model: "",
  btuRating: "",
  waterHeater: {
    temp: "",
    capacity: "",
    energySource: "",
  },
  airHandler: {
    hasAc: false,
    hasHeater: false,
    hasHeatPump: false,
    atLeastOneMethod: false,
    ac: {
      eer: "",
    },
    heater: {
      energySource: "",
    },
    heatPump: {
      seer: "",
      hspf: "",
    },
  },
};

export function NewAppliance() {
  useProtectedRoute();
  const navigate = useNavigate();

  // Previously set
  const { globalState, setGlobalState } = useGlobalState();
  const { nextApNum, email } = globalState;

  const {
    values,
    errors,
    getFieldProps,
    handleSubmit,
    touched,
    setFieldError,
  } = useFormik({
    initialValues: initialVals,
    validationSchema: schema,
    validateOnMount: true,
    onSubmit: async (values, helpers) => {
      console.log("SUBMITTING", values, helpers);
      const { airHandler, waterHeater } = values;
      const resp = await postJson("/api/appliances/create", {
        appliance_number: nextApNum,
        email: email,
        type: values.applianceType,
        manufacturer: values.manufacturer,
        btu_rating: values.btuRating,
        model: values.model,
        // Air Handler specific
        // - bool values to check selections
        air_handler_heating_cooling_methods: {
          AC: airHandler.hasAc,
          Heater: airHandler.hasHeater,
          Heatpump: airHandler.hasHeatPump,
        },
        air_handler_ac_eer: airHandler.ac.eer,
        air_handler_heater_energy_source: airHandler.heater.energySource,
        air_handler_heatpump_hspf: airHandler.heatPump.hspf,
        air_handler_heatpump_seer: airHandler.heatPump.seer,
        // Water heater specific
        water_heater_energy_source: waterHeater.energySource,
        water_heater_temperature: waterHeater.temp,
        water_heater_capacity: waterHeater.capacity,
      });

      if (resp.status === 200) {
        setGlobalState((s) => ({ ...s, nextApNum: s.nextApNum + 1 }));
        navigate("/ApplianceList");
      } else {
        setFieldError("formError", resp.data.err);
      }
      helpers.setSubmitting(false);
    },
  });

  // Load manufacturers data.
  const [manufacturers, setManufacturers] = useState([]);
  const { loading, data } = useFetch("/api/manufacturers-names");
  useEffect(() => {
    if (!data) return;
    setManufacturers(data.data.map((i) => i[0]));
  }, [loading]);

  const getApplianceTypeAdditionalFields = () => {
    switch (values.applianceType) {
      case "Air Handler":
        return (
          <>
            <Form.Group className="mb-3" controlId="air-handler-checkbox-views">
              <Form.Label>Heating/Cooling Methods</Form.Label>
              <Form.Check
                type="checkbox"
                name="ac"
                label="Air Conditioner"
                {...getFieldProps("airHandler.hasAc")}
              />
              <Form.Check
                type="checkbox"
                name="heater"
                label="Heater"
                {...getFieldProps("airHandler.hasHeater")}
              />
              <Form.Check
                type="checkbox"
                name="heatpump"
                label="Heat Pump"
                {...getFieldProps("airHandler.hasHeatPump")}
              />
              {(touched.airHandler?.hasAc ||
                touched.airHandler?.hasHeatPump ||
                touched.airHandler?.hasHeater) &&
                errors.airHandler?.atLeastOneMethod && (
                  <div style={{ color: "red" }}>
                    {errors.airHandler?.atLeastOneMethod}
                  </div>
                )}
            </Form.Group>
            {values.airHandler.hasAc && (
              <>
                <Form.Group
                  className="mb-3"
                  controlId="air-handler-checkbox-ac-eer"
                >
                  <Form.Label>Energy Efficiency Ratio</Form.Label>
                  <Form.Control
                    type="number"
                    name="EER"
                    {...getFieldProps("airHandler.ac.eer")}
                    isInvalid={
                      touched.airHandler?.ac?.eer &&
                      !!errors.airHandler?.ac?.eer
                    }
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.airHandler?.ac?.eer}
                  </Form.Control.Feedback>
                </Form.Group>
              </>
            )}
            {values.airHandler.hasHeater && (
              <>
                <Form.Group
                  className="mb-3"
                  controlId="air-handler-checkbox-heater-energy-source"
                >
                  <Form.Label>Energy Source</Form.Label>
                  <Form.Select
                    aria-label="Default select example"
                    {...getFieldProps("airHandler.heater.energySource")}
                    isInvalid={
                      touched.airHandler?.heater?.energySource &&
                      !!errors.airHandler?.heater?.energySource
                    }
                  >
                    <option value="" disabled>
                      Select Energy Source
                    </option>
                    {optionForEach(heaterEnergySources)}
                  </Form.Select>
                  <Form.Control.Feedback type="invalid">
                    {errors.airHandler?.heater?.energySource}
                  </Form.Control.Feedback>
                </Form.Group>
              </>
            )}
            {values.airHandler.hasHeatPump && (
              <>
                <Form.Group
                  className="mb-3"
                  controlId="air-handler-heat-pump-hspf"
                >
                  <Form.Label>Heating Seasonal Performance Factor</Form.Label>
                  <Form.Control
                    type="number"
                    name="HSPF"
                    {...getFieldProps("airHandler.heatPump.hspf")}
                    isInvalid={
                      touched.airHandler?.heatPump?.hspf &&
                      !!errors.airHandler?.heatPump?.hspf
                    }
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.airHandler?.heatPump?.hspf}
                  </Form.Control.Feedback>
                </Form.Group>
                <Form.Group
                  className="mb-3"
                  controlId="air-handler-heat-pump-seer"
                >
                  <Form.Label>Seasonal Energy Efficiency Rating</Form.Label>
                  <Form.Control
                    type="number"
                    name="SEER"
                    {...getFieldProps("airHandler.heatPump.seer")}
                    isInvalid={
                      touched.airHandler?.heatPump?.seer &&
                      !!errors.airHandler?.heatPump?.seer
                    }
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.airHandler?.heatPump?.seer}
                  </Form.Control.Feedback>
                </Form.Group>
              </>
            )}
          </>
        );
      case "Water Heater":
        return (
          <>
            <Form.Group className="mb-3" controlId="water-heater-energy-source">
              <Form.Label>Energy Source</Form.Label>
              <Form.Select
                aria-label="Default select example"
                {...getFieldProps("waterHeater.energySource")}
                isInvalid={
                  touched.waterHeater?.energySource &&
                  !!errors.waterHeater?.energySource
                }
              >
                <option value="" disabled>
                  Select Energy Source
                </option>
                {optionForEach(waterHeaterEnergySources)}
              </Form.Select>
              <Form.Control.Feedback type="invalid">
                {errors.waterHeater?.energySource}
              </Form.Control.Feedback>
            </Form.Group>
            <Form.Group
              className="mb-3"
              controlId="water-heater-current-temperature"
            >
              <Form.Label>Current Temperature</Form.Label>
              <Form.Control
                type="number"
                {...getFieldProps("waterHeater.temp")}
                isInvalid={
                  touched.waterHeater?.temp && !!errors.waterHeater?.temp
                }
              />
              <Form.Control.Feedback type="invalid">
                {errors.waterHeater?.temp}
              </Form.Control.Feedback>
            </Form.Group>
            <Form.Group className="mb-3" controlId="water-heater-capacity">
              <Form.Label>Capacity (gallons)</Form.Label>
              <Form.Control
                type="number"
                {...getFieldProps("waterHeater.capacity")}
                isInvalid={
                  touched.waterHeater?.capacity &&
                  !!errors.waterHeater?.capacity
                }
              />
              <Form.Control.Feedback type="invalid">
                {errors.waterHeater?.capacity}
              </Form.Control.Feedback>
            </Form.Group>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <Container>
      <LineDiagram currentStep={1} />
      <h1>Enter appliance info</h1>
      <Form noValidate onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="appliance-type">
          <Form.Label>Appliance Type</Form.Label>
          <Form.Select
            aria-label="Default select example"
            {...getFieldProps("applianceType")}
          >
            <option value="" disabled>
              Select Appliance Type
            </option>
            {optionForEach(applianceTypes)}
          </Form.Select>
        </Form.Group>
        {values.applianceType && (
          <>
            <Form.Group className="mb-3" controlId="air-handler-manufacturers">
              <Form.Label>Manufacturer</Form.Label>
              <Form.Control
                as="select"
                name="manufacturer"
                {...getFieldProps("manufacturer")}
              >
                <option value="" disabled>
                  Select a manufacturer
                </option>
                {optionForEach(manufacturers)}
              </Form.Control>
            </Form.Group>
            {!errors.manufacturer && (
              <>
                <Form.Group className="mb-3" controlId="air-handler-btu-rating">
                  <Form.Label>BTU Rating</Form.Label>
                  <Form.Control
                    type="text"
                    name="btuRating"
                    isInvalid={touched.btuRating && !!errors.btuRating}
                    {...getFieldProps("btuRating")}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.btuRating}
                  </Form.Control.Feedback>
                </Form.Group>
                <Form.Group className="mb-3" controlId="air-handler-model">
                  <Form.Label>Model Name (Optional)</Form.Label>
                  <Form.Control
                    type="text"
                    name="model"
                    {...getFieldProps("model")}
                  />
                </Form.Group>{" "}
                {getApplianceTypeAdditionalFields()}
              </>
            )}
          </>
        )}
        <Button type="submit">Add</Button>
      </Form>
    </Container>
  );
}

export default NewAppliance;
