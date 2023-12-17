import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
    reducerPath: "api",
    baseQuery: fetchBaseQuery({
        baseUrl: process.env.REACT_APP_API_URL,
        prepareHeaders: (headers, { getState }) => {
            const { auth: { credentials } } = getState();
            if (credentials) {
                const { username, password } = credentials;
                const token = username + ":" + password;
                headers.set("Authorization", "Basic " + btoa(unescape(encodeURIComponent(token))));
            }
            return headers;
        },
    }),
    endpoints: (builder) => ({
        getTexts: builder.query({
            query: (page = 1) => ({
                url: "/texts",
                params: {
                    page
                },
            }),
        }),
        confirmText: builder.mutation({
            query: (id) => ({
                url: "/texts/" + id,
                method: "PUT"
            }),
        })
    }),
});

export const { useGetTextsQuery, useConfirmTextMutation } = api;