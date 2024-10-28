import React, { useState } from 'react';
import axios from 'axios';
import './AddCompany.css';

const AddCompany = () => {
  const [careerPageUrl, setCareerPageUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/companies', { url: careerPageUrl });
      alert('Career page URL added successfully!');
      setCareerPageUrl('');
    } catch (error) {
      console.error('Error adding career page URL:', error);
      alert('Failed to add career page URL. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-company-form">
      <label htmlFor="careerPageUrl">Career Page URL with Search Criteria:</label>
      <input
        type="url"
        id="careerPageUrl"
        value={careerPageUrl}
        onChange={(e) => setCareerPageUrl(e.target.value)}
        required
      />
      <button type="submit">Add Career Page URL</button>
    </form>
  );
};

export default AddCompany;