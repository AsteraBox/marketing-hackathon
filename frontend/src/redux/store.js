import { configureStore } from "@reduxjs/toolkit";
import { setupListeners } from "@reduxjs/toolkit/query/react";

import { api } from "./reducers/api";
import { auth } from "./reducers/auth";

export const store = configureStore({
    reducer: {
        [api.reducerPath]: api.reducer,
        auth: auth.reducer,
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(api.middleware),
});

setupListeners(store.dispatch);
