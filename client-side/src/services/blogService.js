const API_URL = 'http://localhost:5000/blogs';  // Adjust the URL as needed

const getBlogs = async () => {
    const response = await fetch(API_URL);
    return response.json();
};

const createBlog = async (blogData) => {
    const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json'
    },
    body: JSON.stringify(blogData)
});
return response.json();
};

export default {
    getBlogs,
    createBlog
};    