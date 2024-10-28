import React from 'react';
import './JobCard.css';

const JobCard = ({ job, viewMode }) => {
  return (
    <div className={`job-card ${viewMode}`}> {/* Adjust card layout based on viewMode */}
      <h3>{job.title}</h3>
      <p><strong>Company:</strong> {job.company}</p>
      <p><strong>Location:</strong> {job.location}</p>
      <p><strong>Experience:</strong> {job.experience}</p>
      <p><strong>Type:</strong> {job.jobType}</p>
      <a href={job.link} target="_blank" rel="noopener noreferrer">
        View Job Posting
      </a>
    </div>
  );
};

export default JobCard;