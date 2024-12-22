import React, { useEffect, useState } from 'react';

function JobList() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/jobs/')
      .then((response) => response.json())
      .then((data) => setJobs(data));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Job Listings</h1>
      <div className="space-y-4">
        {jobs.map((job) => (
          <div key={job.id} className="p-4 border rounded">
            <h2 className="text-lg font-bold">{job.title}</h2>
            <p>{job.company_name}</p>
            <p>{job.location}</p>
            <a href={job.job_url} className="text-blue-500">
              View Details
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default JobList;
