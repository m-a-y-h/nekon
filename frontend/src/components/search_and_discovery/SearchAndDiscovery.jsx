import React from 'react';
import SearchComponent from './SearchComponent';

const SearchAndDiscovery = ({ onClose }) => {
    return (
        <div className="bg-red-300 min-h-screen p-6">
            <h1 className="text-3xl font-bold text-center mb-6 bf">Search and Discovery</h1>
            <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-lg p-6">
                
                <p className="text-white mb-4 bg-yellow-400">
                    Use the search feature below to find your favorite dishes and explore new culinary delights!
                </p>
                <SearchComponent />
            </div>
        </div>
    );
};

export default SearchAndDiscovery;
