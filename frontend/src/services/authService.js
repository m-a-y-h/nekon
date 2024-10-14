import axios from 'axios';

// Base URL for your API
const API_URL = 'http://localhost:8000/apis/';

// Register a new user
const register = async (firstName, lastName, email, password, confirmPassword) => {
    try {
        const response = await axios.post(`${API_URL}sign_up/`, {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            confirm_password: confirmPassword
        });
        return response.data;
    } catch (error) {
        console.error("Registration error:", error.response.data);
        throw error;
    }
};

// Login user
const login = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}sign_in/`, {
            username,
            password
        });
        if (response.data.access) {
            localStorage.setItem("accessToken", response.data.access);
            localStorage.setItem("refreshToken", response.data.refresh);
        }
        return response.data;
    } catch (error) {
        console.error("Login error:", error.response.data);
        throw error;
    }
};

// Logout user
const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
};

export { register, login, logout };
