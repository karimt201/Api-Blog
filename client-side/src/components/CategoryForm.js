import React, { useState } from 'react';
import axios from 'axios';
import './CategoryForm.css'; // Import the CSS file

const CategoryForm = () => {
    const [formData, setFormData] = useState({
        title: '',
        description: ''
    });
    const [responseMessage, setResponseMessage] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
        ...formData,
        [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
        const response = await axios.post('http://localhost:5000/categories', formData);
        setResponseMessage(response.data.message);
        setFormData({ title: '', description: '' }); // Reset form after successful submission
        } catch (error) {
        setResponseMessage('Error submitting category. Please try again.');
        console.error('There was an error!', error);
        }
    };

    return (
        <div>
        <h2>Create a New Category</h2>
        <form onSubmit={handleSubmit}>
            <div>
            <label htmlFor="title">Title:</label>
            <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
            />
            </div>

            <div>
            <label htmlFor="description">Description:</label>
            <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                required
            />
            </div>

            <button type="submit">Submit</button>
        </form>

        {responseMessage && <p>{responseMessage}</p>}
        </div>
    );
};

export default CategoryForm;
