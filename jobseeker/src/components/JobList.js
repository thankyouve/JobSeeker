import React, { useEffect, useState } from 'react';
import axios from 'axios';
import JobCard from './JobCard';
import './JobList.css';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('list'); // 'list' or 'grid'

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get('http://localhost:5000/jobs');
        setJobs(response.data);
      } catch (error) {
        console.error('Error fetching jobs:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

  if (loading) {
    return <p>Loading jobs...</p>;
  }

  if (jobs.length === 0) {
    return <p>No jobs available.</p>;
  }

  return (
    <div>
      <div className="view-toggle">
        <button onClick={() => setViewMode('list')}>List View</button>
        <button onClick={() => setViewMode('grid')}>Grid View</button>
      </div>
      <div className={viewMode === 'grid' ? 'job-list-grid' : 'job-list'}>
        {jobs.map((job) => (
          <JobCard key={job._id} job={job} viewMode={viewMode} />
        ))}
      </div>
    </div>
  );
};

export default JobList;
