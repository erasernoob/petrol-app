import { createSlice } from "@reduxjs/toolkit"
export const dataSlice = createSlice({
    name: 'data',
    initialState: {
        hydroData: [],
        drillData: [],
        limitData: [],
    },
    reducers: {
        setHydro: (state, actions) => {
            state.hydroData = actions.payload
        },
        setDrill: (state, actions) => {
            state.drillData = actions.payload
        },
        setLimit: (state, actions) => {
            state.limitData = actions.payload
        }
    }
})

export const { setDrill, setHydro, setLimit } = dataSlice.actions
export default dataSlice.reducer