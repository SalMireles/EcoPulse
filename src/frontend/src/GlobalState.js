import React, { createContext, useCallback, useState } from "react";

export const GlobalState = createContext();

const defaultState = {
  email: null,
  onGrid: null,
  nextApNum: 1,
  nextPgNum: 1,
};

export const GlobalStateProvider = ({ children }) => {
  const [globalState, setGlobalState] = useState(defaultState);
  const resetGlobalState = useCallback(() => {
    setGlobalState(defaultState);
    console.log("RESET GLOBAL STATE");
  });
  return (
    <GlobalState.Provider
      value={{
        globalState,
        setGlobalState,
        resetGlobalState,
      }}
    >
      {children}
    </GlobalState.Provider>
  );
};
