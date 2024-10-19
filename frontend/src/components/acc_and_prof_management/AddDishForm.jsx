import React, { useState } from 'react';
import axios from 'axios';

const AddDishForm = () => {
    const [formData, setFormData] = useState({
        title_en: '',
        description_en: '',
        price_en: '',
        calories: '',
        dietary: '',
        allergens: '',
        image: null,
    });

    const [errorMessage, setErrorMessage] = useState('');

    // Handle form field changes
    const handleChange = (e) => {
        const { name, value, files } = e.target;
        setFormData({
            ...formData,
            [name]: files ? files[0] : value, // Use files[0] for file inputs
        });
    };

    // Handle form submission for adding a dish
    const handleSubmit = async (e) => {
        e.preventDefault();
        const formDataObj = new FormData();
        Object.keys(formData).forEach((key) => {
            formDataObj.append(key, formData[key]);
        });

        try {
            const token = localStorage.getItem('token'); // Get the token from local storage
            if (!token) {
                setErrorMessage('You must be logged in to add a dish.');
                return;
            }

            await axios.post('http://localhost:8000/api/acc-and-prof-management/dishes/', formDataObj, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Token ${token}`, // Include token in the request
                },
            });

            alert('Dish added successfully!');
            setErrorMessage(''); // Clear error message after successful submission

            // Clear the form
            setFormData({
                title_en: '',
                description_en: '',
                price_en: '',
                calories: '',
                dietary: '',
                allergens: '',
                image: null,
            });
        } catch (error) {
            const message = error.response?.data?.detail || 'Error adding dish.';
            setErrorMessage(message); // Set error message
        }
    };

    // Render the form for adding a dish
    return (
        <form onSubmit={handleSubmit} className="bg-white p-5 rounded-lg shadow-lg mb-5">
            <div className="mb-4">
                <input
                    type="text"
                    name="title_en"
                    placeholder="Title (EN)"
                    value={formData.title_en}
                    onChange={handleChange}
                    required
                    className="border rounded w-full py-2 px-3"
                />
            </div>
            <div className="mb-4">
                <textarea
                    name="description_en"
                    placeholder="Description (EN)"
                    value={formData.description_en}
                    onChange={handleChange}
                    required
                    className="border rounded w-full py-2 px-3"
                />
            </div>
            <div className="mb-4">
                <input
                    type="number"
                    name="price_en"
                    placeholder="Price (EN)"
                    value={formData.price_en}
                    onChange={handleChange}
                    required
                    className="border rounded w-full py-2 px-3"
                />
            </div>

            <div className="mb-4">
                <input
                    type="number"
                    name="calories"
                    placeholder="Calories"
                    value={formData.calories}
                    onChange={handleChange}
                    required
                    className="border rounded w-full py-2 px-3"
                />
            </div>
            <div className="mb-4">
                <input
                    type="text"
                    name="dietary"
                    placeholder="Dietary Info"
                    value={formData.dietary}
                    onChange={handleChange}
                    required
                    className="border rounded w-full py-2 px-3"
                />
            </div>
            <div className="mb-4">
                <input
                    type="text"
                    name="allergens"
                    placeholder="Allergens"
                    value={formData.allergens}
                    onChange={handleChange}
                    required
                    className="border rounded w-full py-2 px-3"
                />
            </div>
            <div className="mb-4">
                <input
                    type="file"
                    name="image"
                    onChange={handleChange}
                    required
                    className="border rounded w-full py-2 px-3"
                />
            </div>
            <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">Add Dish</button>
            {errorMessage && <p className="text-red-500 mt-4">{errorMessage}</p>}
        </form>
    );
};

export default AddDishForm;
