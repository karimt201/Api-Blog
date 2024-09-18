import React from 'react';
import BlogForm from '../components/BlogForm';
import blogService from '../services/blogService';

const CreateBlogPage = () => {
    const handleBlogSubmit = async (formData) => {
        try {
        await blogService.createBlog(formData);
        alert('Blog created successfully!');
        } catch (error) {
        console.error('Error creating blog:', error);
        }
    };

    return (
        <div>
        <h1>Create a New Blog</h1>
        <BlogForm onSubmit={handleBlogSubmit} />
        </div>
    );
};

export default CreateBlogPage;