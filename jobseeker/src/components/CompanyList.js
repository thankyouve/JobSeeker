import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './CompanyList.css';

const CompanyList = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const response = await axios.get('http://localhost:5000/companies');
        setCompanies(response.data);
      } catch (error) {
        console.error('Error fetching companies:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCompanies();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/companies/${id}`);
      setCompanies(companies.filter((company) => company._id !== id));
      alert('Career page URL deleted successfully!');
    } catch (error) {
      console.error('Error deleting career page URL:', error);
      alert('Failed to delete career page URL. Please try again.');
    }
  };

  if (loading) {
    return <p>Loading monitored career pages...</p>;
  }

  if (companies.length === 0) {
    return <p>No career pages are being monitored.</p>;
  }

  return (
    <div className="company-list">
      <h2>Monitored Career Pages</h2>
      <ul>
        {companies.map((company) => (
          <li key={company._id} className="company-item">
            <span>{company.url}</span>
            <button onClick={() => handleDelete(company._id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CompanyList;