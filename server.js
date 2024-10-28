const mongoose = require('mongoose');
const express = require('express');
const cors = require('cors');
const cron = require('node-cron');
const axios = require('axios');
const Job = require('./models/Jobs');

const app = express();
const PORT = process.env.PORT || 5000;

// Connect to MongoDB
mongoose.connect('mongodb+srv://thankyouve:Zyf009720!@jobseeker.9exep.mongodb.net/?retryWrites=true&w=majority&appName=JobSeeker', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log("MongoDB Connected...");
}).catch(err => {
    console.error("MongoDB connection error:", err);
});

// Middleware
app.use(express.json());
app.use(cors());

// Schedule Python scraper to run twice a day
cron.schedule('0 0,12 * * *', () => {
    console.log('Running scheduled scraping task...');
    exec('python scraper/job_scraper.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing scraper: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Scraper stderr: ${stderr}`);
            return;
        }
        console.log(`Scraper output: ${stdout}`);
    });
});

// Create a new job posting
app.post('/jobs', async (req, res) => {
    const { title, company, location, experience, link } = req.body;

    try {
        const newJob = new Job({
            title,
            company,
            location,
            experience,
            link,
        });

        const savedJob = await newJob.save();
        res.status(201).json(savedJob);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// Get all job postings
app.get('/jobs', async (req, res) => {
    try {
        const jobs = await Job.find();
        res.status(200).json(jobs);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Get a single job by ID
app.get('/jobs/:id', async (req, res) => {
    try {
        const job = await Job.findById(req.params.id);
        if (!job) return res.status(404).json({ message: 'Job not found' });

        res.status(200).json(job);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Update a job by ID
app.put('/jobs/:id', async (req, res) => {
    try {
        const updatedJob = await Job.findByIdAndUpdate(req.params.id, req.body, { new: true });
        if (!updatedJob) return res.status(404).json({ message: 'Job not found' });

        res.status(200).json(updatedJob);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// Delete a job by ID
app.delete('/jobs', async (req, res) => {
    try {
        await Job.deleteMany({}); // Deletes all job documents in the Job collection
        res.status(200).send({ message: 'All jobs deleted successfully.' });
    } catch (error) {
        res.status(500).send({ error: 'Failed to delete jobs.' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});