import React, { useState } from 'react';
import axios from 'axios';

const ApplyForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    phone_number: '',
    job: '',
    gender: '',
    email: '',
    employment_status: '',
    location_id: ''
  });

  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); 
    try {
      const response = await axios.post('http://localhost:5000/apply-form', formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      setResponseMessage(response.data.message);
    } catch (error) {
      setResponseMessage('Error: ' + (error.response ? error.response.data.error : error.message));
    }
  };

  return (
    <div>
      <h2>Apply Form</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </div>
        <div>
          <label>Phone Number:</label>
          <input type="text" name="phone_number" value={formData.phone_number} onChange={handleChange} required />
        </div>
        <div>
          <label>Job:</label>
          <input type="text" name="job" value={formData.job} onChange={handleChange} required />
        </div>
        <div>
          <label>Gender:</label>
          <input type="text" name="gender" value={formData.gender} onChange={handleChange} required />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>
        <div>
          <label>Employment Status:</label>
          <input type="text" name="employment_status" value={formData.employment_status} onChange={handleChange} required />
        </div>
        <div>
          <label>Location ID:</label>
          <input type="number" name="location_id" value={formData.location_id} onChange={handleChange} required />
        </div>
        <button type="submit">Submit</button>
      </form>

      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
};

export default ApplyForm;
