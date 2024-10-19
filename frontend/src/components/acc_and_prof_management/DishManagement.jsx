import React, { useEffect, useState } from 'react';
import axios from 'axios';
import LoginComponent from './LoginComponent';
import { FaStar } from 'react-icons/fa';

const DishManagement = () => {
    const [dishes, setDishes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));

    useEffect(() => {
        const fetchDishes = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get('http://localhost:8000/api/acc-and-prof-management/dishes/', {
                    headers: { Authorization: `Token ${token}` },
                });
                setDishes(response.data);
            } catch (err) {
                setError(err.response ? err.response.data : { message: 'Network error' });
            } finally {
                setLoading(false);
            }
        };

        if (isAuthenticated) {
            fetchDishes();
        }
    }, [isAuthenticated]);

    const handleLoginSuccess = () => {
        setIsAuthenticated(true);
    };

    if (!isAuthenticated) {
        return <LoginComponent onLoginSuccess={handleLoginSuccess} />;
    }

    if (loading) return <p className="text-center">Loading...</p>;
    if (error) return <p className="text-center text-red-500">Error: {error.message}</p>;

    return (
        <div className="flex overflow-x-auto no-scrollbar p-4 mt-5 ">
            {dishes.map((dish) => (
                <div
                    key={dish.id}
                    className="bg-white text-gray-800 rounded-lg shadow-lg p-4 transition-transform duration-300 transform hover:scale-105 hover:shadow-xl mx-2"
                    style={{ width: '300px' }} // Fixed width for consistent card size
                >
                    <img
                        src={dish.image}
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
                        <button className="bg-orange-600 text-white px-4 py-4 rounded-full shadow hover:bg-orange-700 transition duration-200 mr-2">Order Now</button>
                        <button className="bg-blue-600 text-white px-4 py-4 rounded-full shadow hover:bg-blue-700 transition duration-200 ml-2">Learn More</button>
                    </div>
                </div>
            ))}
        </div>
    );
};

// Function to handle rating
const handleRating = (dishId, rating) => {
    // Logic to handle rating submission and update average rating
    console.log(`Rated dish ${dishId} with ${rating} stars`);
};

export default DishManagement;
