import { createSlice } from "@reduxjs/toolkit";

export const auth = createSlice({
    name: "auth",
    initialState: {
        credentials: JSON.parse(sessionStorage.getItem("credentials")) || null,
        authorized: false
    },
    reducers: {
        setCredentials: (state, action) => {
            sessionStorage.setItem("credentials", JSON.stringify(action.payload));
            state.credentials = action.payload;
        },
        setAuthorized: (state, action) => {
            state.authorized = action.payload;
        },
    },
});

export const { setCredentials, setAuthorized } = auth.actions;
