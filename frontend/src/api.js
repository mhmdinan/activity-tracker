import axios from "axios";

const API = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export const fetchActivities = (skip, limit) =>
    API.get(`/get-daily-activities?skip=${skip}&limit=${limit}`);

export const getActivity = (activity_name) =>
    API.get(`//get-activity/${activity_name}`);

export const createActivity = (activityData) =>
    API.post(`/create-activity`, {
        name: activityData.name.trim(),
        goal: activityData.goal,
        notes: activityData.notes?.trim() || ""
    });

export const logActivity = (activity_name, addition) =>
    API.post(`/add-in-activity`, {activity_name, addition});

export const getActivityData = (activity_name, day_count) =>
    API.get(`/get-activity-data/${activity_name}?day_count=${day_count}`);

export const getActivityPlot = (activity_name, day_count) =>
    API.get(`/get-activity-plot/${activity_name}?day_count=${day_count}`);