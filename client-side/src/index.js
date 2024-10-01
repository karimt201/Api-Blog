import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import { CreatePost } from "./components/createpost";
import App from "./components/test";
import CategoryForm from "./components/CategoryForm"
import BlogForm from "./components/BlogForm"

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BlogForm />
  </React.StrictMode>
);

reportWebVitals();
