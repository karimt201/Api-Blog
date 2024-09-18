import React, { useState, useEffect } from "react";
import "./create-post.css";

export const CreatePost = () => {
    const [postTitle, setPostTitle] = useState("");
    const [description, setDescription] = useState("");
    const [readTime, setReadTime] = useState("");
    const [keywords, setKeywords] = useState("");
    const [categoryIds, setCategoryIds] = useState([]); // Holds selected category ids
    const [availableCategories, setAvailableCategories] = useState([]); // Holds fetched categories
    const [contents, setContents] = useState([{ title: "", description: "" }]);
    const [faqs, setFaqs] = useState([{ question: "", answer: "" }]);
    const [file, setFile] = useState(null);
    const [successMessage, setSuccessMessage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    // Fetch categories from the backend when the component mounts
    useEffect(() => {
        fetch("http://localhost:5000//categorys")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch categories");
                }
                return response.json();
            })
            .then((data) => {
                console.log("Fetched categories:", data.categories); // Log and access the correct property
                setAvailableCategories(data.categories); // Adjust if categories are inside another object
            })            
            .catch((error) => {
                console.error("Error fetching categories:", error);
                setErrorMessage("Error fetching categories. Please try again.");
            });
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append("img", file);
        formData.append("title", postTitle);
        formData.append("description", description);
        formData.append("read_time", readTime);
        formData.append("keywords", keywords.split(","));
        formData.append("category_ids", JSON.stringify(categoryIds)); // Array of selected category ids
        formData.append("contents", JSON.stringify(contents));
        formData.append("faqs", JSON.stringify(faqs));
        formData.append("user_id", 1); // Hardcoded user_id for this example

        fetch("http://localhost:5000/blogs", {
            method: "POST",
            body: formData,
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Error creating blog post");
                }
                return response.json();
            })
            .then((data) => {
                setSuccessMessage("Blog post created successfully!");
                resetForm();
            })
            .catch((error) => {
                setErrorMessage("Failed to create blog post. Please try again.");
            });
    };

    const resetForm = () => {
        setPostTitle("");
        setDescription("");
        setReadTime("");
        setKeywords("");
        setCategoryIds([]);
        setContents([{ title: "", description: "" }]);
        setFaqs([{ question: "", answer: "" }]);
        setFile(null);
    };

    const handleCategoryChange = (e) => {
        const selectedIds = Array.from(e.target.selectedOptions, (option) => parseInt(option.value));
        setCategoryIds(selectedIds); // Update category IDs array
    };

    const handleContentChange = (index, field, value) => {
        const newContents = [...contents];
        newContents[index][field] = value;
        setContents(newContents);
    };

    const handleFaqChange = (index, field, value) => {
        const newFaqs = [...faqs];
        newFaqs[index][field] = value;
        setFaqs(newFaqs);
    };

    return (
        <section className="create-post">
            <h1 className="create-post-title">Create New Post</h1>
            {successMessage && <p className="success-message">{successMessage}</p>}
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            <form className="create-post-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Post Title"
                    className="create-post-input"
                    value={postTitle}
                    onChange={(e) => setPostTitle(e.target.value)}
                />
                <textarea
                    className="create-post-textarea"
                    rows="5"
                    placeholder="Post Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                ></textarea>
                <input
                    type="text"
                    placeholder="Read Time (e.g., '5 MIN READ')"
                    className="create-post-input"
                    value={readTime}
                    onChange={(e) => setReadTime(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Keywords (comma separated)"
                    className="create-post-input"
                    value={keywords}
                    onChange={(e) => setKeywords(e.target.value)}
                />

                {/* Category Selection */}
                <div>
                    <h3>Select Categories:</h3>
                    <select
                        multiple
                        value={categoryIds}
                        onChange={handleCategoryChange}
                        className="create-post-select"
                    >
                        {availableCategories.map((category) => (
                            <option key={category.id} value={category.id}>
                                {category.name}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <h3>Contents:</h3>
                    {contents.map((content, index) => (
                        <div key={index}>
                            <input
                                type="text"
                                placeholder={`Content Title ${index + 1}`}
                                className="create-post-input"
                                value={content.title}
                                onChange={(e) => handleContentChange(index, "title", e.target.value)}
                            />
                            <textarea
                                className="create-post-textarea"
                                rows="3"
                                placeholder={`Content Description ${index + 1}`}
                                value={content.description}
                                onChange={(e) => handleContentChange(index, "description", e.target.value)}
                            ></textarea>
                        </div>
                    ))}
                </div>

                <div>
                    <h3>FAQs:</h3>
                    {faqs.map((faq, index) => (
                        <div key={index}>
                            <input
                                type="text"
                                placeholder={`FAQ Question ${index + 1}`}
                                className="create-post-input"
                                value={faq.question}
                                onChange={(e) => handleFaqChange(index, "question", e.target.value)}
                            />
                            <input
                                type="text"
                                placeholder={`FAQ Answer ${index + 1}`}
                                className="create-post-input"
                                value={faq.answer}
                                onChange={(e) => handleFaqChange(index, "answer", e.target.value)}
                            />
                        </div>
                    ))}
                </div>

                <input
                    type="file"
                    name="file"
                    id="file"
                    className="create-post-upload"
                    onChange={(e) => setFile(e.target.files[0])}
                />
                <button type="submit" className="create-post-btn">
                    Create
                </button>
            </form>
        </section>
    );
};
