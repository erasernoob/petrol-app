import { createSlice } from "@reduxjs/toolkit"
export const dataSlice = createSlice({
    name: 'data',
    initialState: {
        hydroData: [],
        drillData: [],
        limitData: [],
        useTheInitialValue: false,
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
        },
        setUseInitialOrNot: (state, actions) => {
            state.useTheInitialValue = actions.payload
        }
    }
})

export const { setDrill, setHydro, setLimit, setUseInitialOrNot } = dataSlice.actions
export default dataSlice.reducer