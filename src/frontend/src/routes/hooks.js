import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { GlobalState } from "../GlobalState";

export function useFetch(route, deps = []) {
  const [state, setState] = useState({ loading: true, data: null, err: null });

  useEffect(() => {
    setState({ ...state, loading: true });
    fetch(route)
      .then((res) => res.json())
      .then((res) => {
        if (res.status === 200) {
          setState({ ...state, loading: false, data: res.data, err: null });
        } else if (res.status === 400) {
          setState({ ...state, loading: false, data: null, err: res.data.err });
        } else {
          setState({ ...state, loading: false, data: null, err: res.err });
        }
      });
  }, deps);

  return state;
}

export const useGlobalState = () => useContext(GlobalState);

// Some pages should only be viewed with an active email in the context.
export const useProtectedRoute = () => {
  const navigate = useNavigate();
  const { globalState } = useGlobalState();
  const { email } = globalState;
  useEffect(() => {
    if (!email) {
      console.log("Navigating to NewHousehold, this route is protected");
      navigate("/newhousehold");
    }
  }, [email]);
};
