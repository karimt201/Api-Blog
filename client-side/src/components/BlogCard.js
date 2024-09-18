import React from 'react';
import './BlogCard.css';  // Import component-specific styles

const BlogCard = ({ blog }) => {
    return (
        <div className="blog-card">
        <img src={blog.img} alt={blog.title} />
        <h2>{blog.title}</h2>
        <p>{blog.description}</p>
        <p><strong>Read Time:</strong> {blog.read_time} mins</p>
        <p><strong>Categories:</strong> {blog.categories.map(c => c.title).join(', ')}</p>
        </div>
    );
};

export default BlogCard;
