import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/accounts/sign_in';
import Register from './components/accounts/sign_up.js';
import Dashboard from './components/accounts/dashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/sign_in" element={<Login />} />
        <Route path="/sign_up" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<h1>Welcome to Nekon</h1>} />
      </Routes>
    </Router>
  );
}

export default App;