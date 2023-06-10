export function invalidFieldsReducer(state, action) {
  // console.log('action', action.type)
  // console.log('old state', state)

  switch (action.type) {
    case "email":
      return { ...state, email: !action.valid };
    case "postalCode":
      return { ...state, postalCode: !action.valid };
    case "squareFootage":
      return { ...state, squareFootage: isNaN(action.squareFootage) };
    case "tsHeatingCheck":
      return {
        ...state,
        tsHeatingCheck:
          (action.tsHeating === "" && !action.noHeating) ||
          (action.tsHeating !== "" && isNaN(action.tsHeating)),
      };
    case "tsCoolingCheck":
      return {
        ...state,
        tsCoolingCheck:
          (action.tsCooling === "" && !action.noCooling) ||
          (action.tsCooling !== "" && isNaN(action.tsCooling)),
      };
    default: {
      return state;
    }
  }
}

export function formCompleteReducer(state, action) {
  switch (action.type) {
    case "validate":
      let formValid = Object.values(action.invalidFields).every(
        (item) => item === false
      );

      let formCompleted =
        action.email !== "" &&
        action.postalCode !== "" &&
        action.type !== "" &&
        action.squareFootage !== "" &&
        (action.tsHeating !== "" || action.noHeating) &&
        (action.tsCooling !== "" || action.noCooling);

      if (formCompleted && formValid) {
        return true;
      } else {
        return false;
      }
    default:
      return false;
  }
}
