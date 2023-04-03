import axios from "axios";
import { apiUrl } from "./constants";

export const getDataApi = async (url) => {
    const res = await axios.get(`${apiUrl}${url}`);
    return res;
}

export const postDataApi = async (url, data) => {
    const res = await axios.post(`${apiUrl}${url}`, data);
    return res;
}

export const putDataApi = async (url, data) => {
    const res = await axios.put(`${apiUrl}${url}`, data);
    return res;
}

export const patchDataApi = async (url, data) => {
    const res = await axios.patch(`${apiUrl}${url}`, data);
    return res;
}

export const deleteDataApi = async (url) => {
    const res = await axios.delete(`${apiUrl}${url}`);
    return res;
}