
// export default App;
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AccAndProfManagement from './components/acc_and_prof_management/AccAndProfManagement'; // Ensure this path is correct
import SearchAndDiscovery from './components/search_and_discovery/SearchAndDiscovery';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<AccAndProfManagement />} />
                <Route path="/search_and_discovery" element={<SearchAndDiscovery />} />
                {/* Add other routes here if needed */}
            </Routes>
        </Router>
    );
};

export default App;
