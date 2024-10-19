import React, { useState } from 'react';
import axios from 'axios';
import { FaStar } from 'react-icons/fa'; // Import star icon

const SearchComponent = () => {
    const [query, setQuery] = useState('');
    const [uploads, setUploads] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [dishes, setDishes] = useState([]);

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        const token = localStorage.getItem('token');
        if (!token) {
            setError('You must be logged in to search for dishes.');
            setLoading(false);
            return;
        }

        try {
            const response = await axios.get(`http://localhost:8000/api/search/?q=${query}`, {
                headers: {
                    'Authorization': `Token ${token}`,
                },
            });

            if (Array.isArray(response.data)) {
                setUploads(response.data);
            } else {
                setError('Unexpected response format.');
            }
        } catch (err) {
            console.error(err);
            setError('Error fetching data');
        } finally {
            setLoading(false);
        }
    };

    const handleRating = (dishId, rating) => {
        // Handle the rating logic here (e.g., update the dish rating)
        console.log(`Rating for dish ${dishId}: ${rating}`);
    };

    return (
        <div className="container mt-4">
            
            <form onSubmit={handleSearch} className="flex mb-4">
                <input
                    type="text"
                    placeholder="Search for dishes..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="flex-grow border rounded-l-lg py-2 px-4 focus:bg-black text-yellow-400"  
                    required
                />
                <button
                    type="submit"
                    className="bg-blue-500 text-white rounded-r-lg px-4 py-2 hover:bg-blue-600"
                >
                    Search
                </button>
            </form>

            {loading && <p>Loading...</p>}
            {error && <p className="text-red-500">{error}</p>}

            <h2>Search Results:</h2>
            <div className="flex overflow-x-auto no-scrollbar p-4 mt-5">
                {uploads.length > 0 ? (
                    uploads.map((dish) => (
                        <div
                            key={dish.id}
                            className="bg-white text-gray-800 rounded-lg shadow-lg p-4 transition-transform duration-300 transform hover:scale-105 hover:shadow-xl mx-2"
                            style={{ width: '300px' }} // Fixed width for consistent card size
                        >
                            <img
                src={`http://localhost:8000${dish.image}`} // Adjusted URL
                alt={dish.title_en}
                className="w-auto h-auto object-cover rounded-t-lg"
            />
                            <h3 className="text-xl font-semibold mt-2">{dish.title_en}</h3>
                            <p className="text-sm text-gray-600">{dish.description_en}</p>
                            <p className="font-bold mt-1">${(parseFloat(dish.price_en) || 0).toFixed(2)}</p>
                            <p className="text-sm">Calories: {dish.calories}</p>
                            <p className="text-sm">Dietary Info: {dish.dietary}</p>
                            <p className="text-sm">Allergens: {dish.allergens}</p>

                            {/* Star Rating */}
                            <div className="flex mt-2">
                                {Array.from({ length: 5 }, (_, index) => (
                                    <FaStar
                                        key={index}
                                        className="cursor-pointer"
                                        color={dish.userRating && index < dish.userRating ? 'yellow' : '#e4e5e9'}
                                        onClick={() => handleRating(dish.id, index + 1)}
                                    />
                                ))}
                            </div>

                            {/* Action Buttons */}
                            <div className="flex justify-between mt-4">
                                <button className="bg-orange-600 text-white px-4 py-2 rounded-full shadow hover:bg-orange-700 transition duration-200 mr-2">Order Now</button>
                                <button className="bg-blue-600 text-white px-4 py-2 rounded-full shadow hover:bg-blue-700 transition duration-200 ml-2">Learn More</button>
                            </div>
                        </div>
                    ))
                ) : (
                    <h3>No results found.</h3>
                )}
            </div>
        </div>
    );
};

export default SearchComponent;
