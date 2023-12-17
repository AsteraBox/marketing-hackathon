import { createSlice } from "@reduxjs/toolkit";

export const auth = createSlice({
    name: "auth",
    initialState: {
        credentials: null,
        authorized: false
    },
    reducers: {
        setCredentials: (state, action) => {
            state.credentials = action.payload;
        },
        setAuthorized: (state, action) => {
            state.authorized = action.payload;
        },
    },
});

export const { setCredentials, setAuthorized } = auth.actions;
