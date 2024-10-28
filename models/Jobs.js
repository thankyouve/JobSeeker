// Import Mongoose
const mongoose = require('mongoose');

// Define Job Schema
const JobSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true
    },
    company: {
        type: String,
        required: true
    },
    location: {
        type: String,
        required: true
    },
    experience: {
        type: String,
        required: false
    },
    pay: {
        type: String,
        required: false // Pay may be optional, depending on availability
    },
    jobType: {
        type: String,
        enum: ['Full-Time', 'Part-Time', 'Contract', 'Internship'],
        required: false
    },
    remote: {
        type: Boolean,
        default: false
    },
    link: {
        type: String,
        required: true
    },
    datePosted: {
        type: Date,
        default: Date.now
    },
    criteria: {
        type: String,
        required: false // Criteria like "New Grad" could be an optional field
    }
});

// Export the Job model
module.exports = mongoose.model('Job', JobSchema);
