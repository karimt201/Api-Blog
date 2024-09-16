import "./create-post.css";

export const CreatePost = () => {
    return (
        <section className="create-post">
            <h1 className="create-post-title">
                Create New Post
            </h1>
            <form className="create-post-form">
                <input type="text" 
                placeholder="Post Title" 
                className="create-post-input" />
                <select className="create-post-input">
                    <option disabled value="">
                        Select A Catagory
                    </option>
                    <option value="music">music</option>
                    <option value="coffee">coffee</option>
                </select>
                <textarea 
                    className="create-post-texterea"
                    rows="5"
                    placeholder="Post Description"
                >
                </textarea>
                <input type="file" name="file" id="file" className="create-post-upload" />
                <button type="submit" className="create-post-btn">
                    Create
                </button>
                
            </form>
        </section>
    )
}  