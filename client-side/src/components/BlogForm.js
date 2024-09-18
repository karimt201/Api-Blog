import React, { useState } from 'react';

const BlogForm = ({ onSubmit }) => {
const [formData, setFormData] = useState({
    img: '',
    title: '',
    description: '',
    read_time: '',
    keywords: '',
    categories: [],
    contents: [],
    faqs: [],
    user_id: 1
});

const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
};

const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
};

return (
    <form onSubmit={handleSubmit}>
        <label>Image URL:</label>
        <input type="text" name="img" value={formData.img} onChange={handleChange} />
        <label>Title:</label>
        <input type="text" name="title" value={formData.title} onChange={handleChange} />
        <label>Description:</label>
        <textarea name="description" value={formData.description} onChange={handleChange}></textarea>
        <label>Read Time:</label>
        <input type="number" name="read_time" value={formData.read_time} onChange={handleChange} />
        <label>Keywords:</label>
        <input type="text" name="keywords" value={formData.keywords} onChange={handleChange} />
        <button type="submit">Submit</button>
    </form>
    );
};

export default BlogForm;
