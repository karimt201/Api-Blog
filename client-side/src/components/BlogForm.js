    import React, { useState, useEffect } from 'react';
    import axios from 'axios';
    import './BlogForm.css'; // Import your CSS file

    const BlogForm = () => {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        read_time: '',
        date: '',
        keywords: '',
        user_id: '',
        category_id: '', // Single category ID selected from the dropdown
        contents: [
        { title: '', description: '' }, // Initial empty content fields
        ],
        faqs: [
        { question: '', answer: '' }, // Initial empty FAQ fields
        ],
    });

    const [imageFile, setImageFile] = useState(null); // For handling image upload
    const [categories, setCategories] = useState([]); // Categories for dropdown
    const [responseMessage, setResponseMessage] = useState('');

    useEffect(() => {
        // Fetch categories from the backend
        axios.get('http://localhost:5000/categories')
        .then(response => {
            setCategories(response.data.categories);
        })
        .catch(error => {
            console.error('There was an error fetching categories!', error);
        });
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
        ...formData,
        [name]: value
        });
    };

    const handleArrayChange = (e, index, arrayName, fieldName) => {
        const newArray = [...formData[arrayName]];
        newArray[index][fieldName] = e.target.value;
        setFormData({ ...formData, [arrayName]: newArray });
    };

    const handleImageChange = (e) => {
        setImageFile(e.target.files[0]);
    };

    const addField = (arrayName) => {
        setFormData({
        ...formData,
        [arrayName]: [...formData[arrayName], { title: '', description: '' }]
        });
    };

    const addFaqField = () => {
        setFormData({
        ...formData,
        faqs: [...formData.faqs, { question: '', answer: '' }]
        });
    };

        const handleSubmit = async (e) => {
            e.preventDefault();
        
            const postData = new FormData();
            postData.append('title', formData.title);
            postData.append('description', formData.description);
            postData.append('read_time', formData.read_time);
            postData.append('date', formData.date);
            postData.append('keywords', formData.keywords);
            postData.append('user_id', formData.user_id);
            postData.append('category_id', formData.category_id);
        
            // Append image if uploaded
            if (imageFile) {
            postData.append('img', imageFile);
            }
        
            // Convert contents and FAQs arrays to JSON strings
            postData.append('contents', JSON.stringify(formData.contents));
            postData.append('faqs', JSON.stringify(formData.faqs));
        
            try {
            const response = await axios.post('http://localhost:5000/blogs', postData, {
                headers: {
                'Content-Type': 'multipart/form-data',
                },
            });
            setResponseMessage(response.data.message);
            setFormData({
                title: '',
                description: '',
                read_time: '',
                date: '',
                keywords: '',
                user_id: '',
                category_id: '',
                contents: [{ title: '', description: '' }],
                faqs: [{ question: '', answer: '' }],
            });
            setImageFile(null);  // Reset image
            } catch (error) {
            setResponseMessage('Error submitting blog. Please try again.');
            console.error('There was an error!', error);
            }
        };
    
    return (
        <div>
        <h2>Create a New Blog</h2>
        <form onSubmit={handleSubmit}>
            <div>
            <label htmlFor="img">Upload Image:</label>
            <input
                type="file"
                id="img"
                name="img"
                accept="image/*"
                onChange={handleImageChange}
            />
            </div>

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

            <div>
            <label htmlFor="read_time">Read Time:</label>
            <input
                type="text"
                id="read_time"
                name="read_time"
                value={formData.read_time}
                onChange={handleChange}
                required
            />
            </div>

            <div>
            <label htmlFor="date">Date:</label>
            <input
                type="date"
                id="date"
                name="date"
                value={formData.date}
                onChange={handleChange}
                required
            />
            </div>

            <div>
            <label htmlFor="keywords">Keywords (comma-separated):</label>
            <input
                type="text"
                id="keywords"
                name="keywords"
                value={formData.keywords}
                onChange={handleChange}
            />
            </div>

            <div>
            <label htmlFor="category_id">Category:</label>
            <select
                id="category_id"
                name="category_id"
                value={formData.category_id}
                onChange={handleChange}
                required
            >
                <option value="">Select a category</option>
                {categories.map(category => (
                <option key={category.id} value={category.id}>
                    {category.title}
                </option>
                ))}
            </select>
            </div>

            <div>
            <label htmlFor="user_id">User ID:</label>
            <input
                type="text"
                id="user_id"
                name="user_id"
                value={formData.user_id}
                onChange={handleChange}
                required
            />
            </div>

            <h3>Contents</h3>
            {formData.contents.map((content, index) => (
            <div key={index}>
                <label>Content {index + 1} Title:</label>
                <input
                type="text"
                value={content.title}
                onChange={(e) => handleArrayChange(e, index, 'contents', 'title')}
                required
                />
                <label>Content {index + 1} Description:</label>
                <textarea
                value={content.description}
                onChange={(e) => handleArrayChange(e, index, 'contents', 'description')}
                required
                />
            </div>
            ))}
            <button type="button" onClick={() => addField('contents')}>Add More Content</button>

            <h3>FAQs</h3>
            {formData.faqs.map((faq, index) => (
            <div key={index}>
                <label>FAQ {index + 1} Question:</label>
                <input
                type="text"
                value={faq.question}
                onChange={(e) => handleArrayChange(e, index, 'faqs', 'question')}
                required
                />
                <label>FAQ {index + 1} Answer:</label>
                <textarea
                value={faq.answer}
                onChange={(e) => handleArrayChange(e, index, 'faqs', 'answer')}
                required
                />
            </div>
            ))}
            <button type="button" onClick={addFaqField}>Add More FAQs</button>

            <button type="submit">Submit</button>
        </form>

        {responseMessage && <p>{responseMessage}</p>}
        </div>
    );
    };

    export default BlogForm;
