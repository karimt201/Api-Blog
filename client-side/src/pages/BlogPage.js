import React, { useEffect, useState } from 'react';
import BlogCard from '../components/BlogCard';
import blogService from '../services/blogService';

const BlogPage = () => {
const [blogs, setBlogs] = useState([]);

useEffect(() => {
    blogService.getBlogs()
    .then(data => setBlogs(data.blogs))
    .catch(error => console.error('Error fetching blogs:', error));
}, []);

return (
    <div>
    <h1>Blogs</h1>
    <div className="blog-list">
        {blogs.map(blog => (
        <BlogCard key={blog.id} blog={blog} />
        ))}
    </div>
    </div>
);
};

export default BlogPage;
