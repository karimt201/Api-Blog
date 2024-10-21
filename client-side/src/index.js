import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import { CreatePost } from "./components/createpost";
import App from "./components/test";
import CategoryForm from "./components/CategoryForm"
import ApplyForm from "./components/ApplyForm"

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <ApplyForm />
  </React.StrictMode>
);

reportWebVitals();
