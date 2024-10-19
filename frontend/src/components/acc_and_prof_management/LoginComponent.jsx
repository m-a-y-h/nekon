import React, { useState } from 'react';
import axios from 'axios';

const LoginForm = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        // console.log(document.cookie);  // Log all cookies for debugging
    
        // const csrftokenRow = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        // if (!csrftokenRow) {
        //     console.error('CSRF token not found');
        //     setErrorMessage('CSRF token not found');
        //     return;
        // }
    
        // const token = csrftokenRow.split('=')[1];
        // console.log('CSRF Token:', token);  // Log the token for verification
    
        try {
            const response = await axios.post('http://localhost:8000/api/acc-and-prof-management/login/', {
                username: username,
                password: password,
            });
    
            const tokenFromResponse = response.data.token;
            localStorage.setItem('token', tokenFromResponse);
            alert('Login successful');
            setErrorMessage('');
        } catch (error) {
            console.error(error);
            setErrorMessage('Invalid credentials');
        }
    };    
    return (
        
        <form onSubmit={handleSubmit} className="bg-white p-5 rounded-lg shadow-lg mb-5">
            <div className="mb-4">
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    className="border rounded w-full py-2 px-3"
                />
            </div>
                <input
                   type="password" // Change from "text" to "password"
                   name="password"
                   placeholder="Password"
                   value={password}
                   onChange={(e) => setPassword(e.target.value)}
                   required
                   className="border rounded w-full py-2 px-3"
                />
            <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Login</button>
            {errorMessage && <p className="text-red-500 mt-4">{errorMessage}</p>}
        </form>
    );
};

export default LoginForm;
